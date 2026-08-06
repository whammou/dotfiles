# tabcss.py - per-tab user stylesheet toggle + per-site css modules.
#
# `xs` flips the CURRENT TAB between the global stylesheet state and plain css:
#   styled tab -> xs -> plain css (stylesheet stripped for this tab only)
#   plain tab  -> xs -> styled again (stylesheet restored immediately)
#
# qutebrowser applies content.user_stylesheets per-document via
# window._qutebrowser.stylesheet.set_css() in the ApplicationWorld (see
# webenginetab.py _init_stylesheet/_update_stylesheet). We use the same API:
# set_css('') strips the current tab's stylesheet, and re-stripping on
# load_finished keeps it plain across navigations.
#
# Site css: qutebrowser's content.user_stylesheets has no per-domain
# supports_pattern, so modules for matching hosts are appended after the
# base bundle on load_finished/currentChanged. The host->file map arrives
# via os.environ["SITE_CSS"] (sites.py) because sys.modules entries are
# purged after each sourced config file.

import json
import os
import threading
import time
import weakref

from lib.minicss import strip_comments
from qutebrowser.api import cmdutils, apitypes
from qutebrowser.misc import objects
from qutebrowser.qt.core import QMetaObject, QObject, Qt, pyqtSlot
from qutebrowser.utils import log, objreg

# Tabs currently forced to plain css. WeakSet: closed tabs vanish
# automatically, no manual cleanup needed.
_plain = weakref.WeakSet()
# Tabs whose load_finished signal is already connected (also weak).
_connected = weakref.WeakSet()


def _set_css_js(css: str) -> str:
    """Build JS calling the qutebrowser stylesheet API with the given CSS."""
    return (
        "(window._qutebrowser && window._qutebrowser.stylesheet) && "
        "window._qutebrowser.stylesheet.set_css(" + json.dumps(css) + ");"
    )


def _strip(tab: apitypes.Tab) -> None:
    """Remove the stylesheet from the tab's current document."""
    tab.run_js_async(_set_css_js(""))


def _restore(tab: apitypes.Tab) -> None:
    """Re-apply the stylesheet to the tab's current document.

    Uses the same source as qutebrowser (shared.get_user_stylesheet), so the
    restored CSS matches what a fresh page load would get, including the
    scrolling.bar rule.
    """
    from qutebrowser.browser import shared
    tab.run_js_async(_set_css_js(shared.get_user_stylesheet()))


def _on_load_finished(tab: apitypes.Tab, ok: bool) -> None:
    """Re-strip after navigation, while the tab is in plain mode."""
    if ok and tab in _plain:
        _strip(tab)


def _ensure_connected(tab: apitypes.Tab) -> None:
    """Connect load_finished for the tab once, so plain css survives navigation."""  # noqa: E501
    if tab in _connected:
        return
    tab.load_finished.connect(lambda ok: _on_load_finished(tab, ok))
    _connected.add(tab)


try:
    @cmdutils.register()
    @cmdutils.argument("tab", value=cmdutils.Value.cur_tab)
    def toggle_tab_css(tab: apitypes.Tab) -> None:
        """Toggle the user stylesheet on the current tab (styled <-> plain css)."""  # noqa: E501
        if tab in _plain:
            _plain.discard(tab)
            _restore(tab)
        else:
            _plain.add(tab)
            _ensure_connected(tab)
            _strip(tab)
except ValueError:
    pass  # already registered on config re-source

# per-site css: {{{

_wired: set[int] = set()
_site_connected = weakref.WeakSet()


def _site_css_for(host: str) -> str | None:
    """Return the css module for a host, or None when unmapped."""
    try:
        mapping = json.loads(os.environ.get("SITE_CSS", "{}"))
    except json.JSONDecodeError:
        return None
    for domain, path in mapping.items():
        if host == domain or host.endswith("." + domain):
            full = os.path.expanduser(path)
            if os.path.exists(full):
                with open(full, encoding="utf-8") as f:
                    return strip_comments(f.read())
    return None


def _inject_site_css(tab: apitypes.Tab) -> None:
    """Re-apply the base bundle plus the site module, if the host maps one."""
    if tab in _plain:
        return
    site = _site_css_for(tab.url().host())
    if site is None:
        return
    from qutebrowser.browser import shared
    css = shared.get_user_stylesheet() + "\n" + site
    tab.run_js_async(_set_css_js(css))
    log.misc.debug("tabcss: site module applied on %s", tab.url().host())


def _on_site_load_finished(tab: apitypes.Tab, ok: bool) -> None:
    if ok:
        _inject_site_css(tab)


def _apply_window(window) -> None:
    try:
        for i in range(window.tabbed_browser.widget.count()):
            tab = window.tabbed_browser.widget.widget(i)
            if tab is None:
                continue
            if tab not in _site_connected:
                tab.load_finished.connect(
                    lambda ok, t=tab: _on_site_load_finished(t, ok)
                )
                _site_connected.add(tab)
            _inject_site_css(tab)
    except Exception:
        log.misc.exception("tabcss: site css apply failed")


def _wire_window(window) -> None:
    try:
        wid = id(window.tabbed_browser.widget)
        if wid in _wired:
            return
        _wired.add(wid)
        window.tabbed_browser.widget.currentChanged.connect(
            lambda _i: _apply_window(window)
        )
        window.tabbed_browser.new_tab.connect(lambda _t, _i: _apply_window(window))
        window.tabbed_browser.widget.destroyed.connect(lambda: _wired.discard(wid))
        _apply_window(window)
    except Exception:
        log.misc.exception("tabcss: site css wire failed")


class _Scheduler(QObject):

    @pyqtSlot()
    def arm(self) -> None:
        try:
            objects.qapp.new_window.connect(_wire_window)
            for window in objreg.window_registry.values():
                _wire_window(window)
        except Exception:
            log.misc.exception("tabcss: site css arm failed")


def _wait_for_app() -> None:
    # Daemon thread: objects.qapp is torn down before daemon threads stop at
    # interpreter shutdown; any failure there is irrelevant, just exit.
    try:
        while objects.qapp is None:
            time.sleep(0.1)
        QMetaObject.invokeMethod(_scheduler, "arm", Qt.ConnectionType.QueuedConnection)
    except Exception:
        pass


_scheduler = _Scheduler()
threading.Thread(target=_wait_for_app, daemon=True).start()
# }}}
