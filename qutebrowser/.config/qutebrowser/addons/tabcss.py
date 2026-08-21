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
#
#HACK: Qt WebEngine 6.11 regression (qutebrowser #8925, milestone v3.7.1,
# open): on some navigations (notably back/forward), the QWebEngineScripts
# in page.scripts() are skipped entirely - window._qutebrowser and its
# webelem/scroll/caret/stylesheet modules never get created. Symptoms:
# unstyled pages and "Unknown error while getting elements" when hinting.
# Every page gets two restore scripts (DocumentCreation and DocumentReady,
# since either batch may be the one skipped) that re-create the missing
# engine modules and apply the stylesheet via the restored API; the
# load_finished ensure below is a last-resort backstop.
#HACK: REMOVE every #HACK: section in this file when #8925 is fixed upstream.

#HACK: lru_cache + resources imports serve the #8925 restore machinery; drop with it.
import json
import os
import threading
import time
import weakref
from functools import lru_cache

from lib.minicss import strip_comments
from qutebrowser.api import cmdutils, apitypes
from qutebrowser.misc import objects
from qutebrowser.qt.core import QMetaObject, QObject, Qt, pyqtSlot
from qutebrowser.qt.webenginecore import QWebEngineScript
from qutebrowser.utils import log, objreg, resources

# Cached combined user stylesheet; invalidated on config change so the
# per-navigation re-apply does not re-read the css files on every load.
_css_cache: str | None = None


#HACK: DOM <style> fallback in the `else` branches of _ensure_css_js/_strip_js
# - only needed while window._qutebrowser can be missing (#8925). When fixed,
# _strip/_restore call window._qutebrowser.stylesheet.set_css() directly.


def _ensure_css_js(css: str) -> str:
    """Build JS applying the given CSS, with a DOM fallback.

    On Qt 6.11 the DocumentCreation scripts sometimes fail to run after
    navigation, leaving window._qutebrowser undefined. In that case append a
    plain <style> element instead of silently doing nothing.
    """
    css_json = json.dumps(css)
    return (
        "(function(){"
        "var w = window._qutebrowser, s = w && w.stylesheet;"
        "if (s) { s.set_css(" + css_json + "); return; }"
        "var el = document.getElementById('qutebrowser-user-stylesheet');"
        "if (!el) {"
        "el = document.createElement('style');"
        "el.id = 'qutebrowser-user-stylesheet';"
        "(document.head || document.documentElement).appendChild(el);"
        "}"
        "el.textContent = " + css_json + ";"
        "})();"
    )


def _strip_js() -> str:
    """Build JS removing the user stylesheet from the current document."""
    return (
        "(function(){"
        "var w = window._qutebrowser, s = w && w.stylesheet;"
        "if (s) { s.set_css(''); return; }"
        "var el = document.getElementById('qutebrowser-user-stylesheet');"
        "if (el) el.remove();"
        "})();"
    )


#HACK: css cache only exists because _inject_site_css re-applies on every
# load_finished/currentChanged while #8925 is unfixed; when fixed, call
# shared.get_user_stylesheet() directly at the call sites.


def _get_css() -> str:
    """Return the cached combined user stylesheet."""
    global _css_cache
    if _css_cache is None:
        from qutebrowser.browser import shared
        _css_cache = shared.get_user_stylesheet()
    return _css_cache


#HACK: restore machinery - re-creates the engine's webelem/scroll/caret/
# stylesheet modules when the DocumentCreation script batch is skipped
# (#8925). Remove entirely (_RESTORE_DC/DR, _restore_done, _module_source,
# _restore_api_js, _install_restore) when fixed upstream.
_RESTORE_DC = "_qute_tabcss_restore_dc"
_RESTORE_DR = "_qute_tabcss_restore_dr"
# Pages that already have the restore scripts installed (weak).
_restore_done = weakref.WeakSet()


@lru_cache(maxsize=None)
def _module_source(name: str) -> str:
    return resources.read_file(f"javascript/{name}.js")


def _restore_api_js(css: str) -> str:
    """JS re-creating missing engine modules and applying the stylesheet.

    Runs after the engine's own DocumentCreation batch (setTimeout), so on
    healthy pages every module already exists and nothing happens; on pages
    where the batch was skipped, the modules are re-created from their own
    sources so both styling and hinting keep working.
    """
    modules = "\n".join(
        "if (!w.{n}) {{\n{src}\n}}".format(n=name, src=_module_source(name))
        for name in ("scroll", "webelem", "caret", "stylesheet")
    )
    css_json = json.dumps(css)
    return (
        "(function(){\n"
        "setTimeout(function(){\n"
        "var w = window._qutebrowser || (window._qutebrowser = {initialized: {}});\n"
        + modules + "\n"
        "if (w.stylesheet && w.stylesheet.set_css) w.stylesheet.set_css(" + css_json + ");\n"  # noqa: E501
        "else {\n"
        "var el = document.getElementById('qutebrowser-user-stylesheet');\n"
        "if (!el){el = document.createElement('style'); el.id = 'qutebrowser-user-stylesheet';}\n"  # noqa: E501
        "el.textContent = " + css_json + ";\n"
        "if (!el.parentNode) (document.head || document.documentElement).appendChild(el);\n"  # noqa: E501
        "}\n"
        "}, 0);\n"
        "})();"
    )


def _install_restore(tab: apitypes.Tab) -> None:
    """Insert restore scripts at DocumentCreation and DocumentReady."""
    try:
        page = tab._widget.page()
        scripts = page.scripts()
        js = _restore_api_js(_get_css())
        for name, point in (
            (_RESTORE_DC, QWebEngineScript.InjectionPoint.DocumentCreation),
            (_RESTORE_DR, QWebEngineScript.InjectionPoint.DocumentReady),
        ):
            for script in scripts.find(name):
                scripts.remove(script)
            script = QWebEngineScript()
            script.setInjectionPoint(point)
            script.setWorldId(QWebEngineScript.ScriptWorldId.ApplicationWorld)
            script.setRunsOnSubFrames(True)
            script.setSourceCode(js)
            script.setName(name)
            scripts.insert(script)
    except Exception:
        log.misc.exception("tabcss: restore script install failed")


#HACK: config-change refresh (cache + restore reinstall) - only needed while
# the restore scripts and per-navigation re-apply exist (#8925); remove with
# the hack.
def _on_config_changed(option: str) -> None:
    """Refresh cached css and reinstall fallbacks when styling settings change."""
    if option in ("content.user_stylesheets", "scrolling.bar"):
        global _css_cache
        _css_cache = None
        _restore_done.clear()
        for window in objreg.window_registry.values():
            try:
                for i in range(window.tabbed_browser.widget.count()):
                    tab = window.tabbed_browser.widget.widget(i)
                    if tab is None:
                        continue
                    _install_restore(tab)
                    _inject_site_css(tab)
            except Exception:
                log.misc.exception("tabcss: config refresh failed")

# Tabs currently forced to plain css. WeakSet: closed tabs vanish
# automatically, no manual cleanup needed.
_plain = weakref.WeakSet()
# Tabs whose load_finished signal is already connected (also weak).
_connected = weakref.WeakSet()


def _strip(tab: apitypes.Tab) -> None:
    """Remove the stylesheet from the tab's current document."""
    tab.run_js_async(_strip_js())


def _restore(tab: apitypes.Tab) -> None:
    """Re-apply the stylesheet to the tab's current document.

    Uses the same source as qutebrowser (shared.get_user_stylesheet), so the
    restored CSS matches what a fresh page load would get, including the
    scrolling.bar rule.
    """
    tab.run_js_async(_ensure_css_js(_get_css()))


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


#HACK: also applies the base bundle to EVERY tab on load_finished/currentChanged
# as a #8925 backstop; the original returned early when no site module was
# mapped. Restore that early-return when fixed upstream.
def _inject_site_css(tab: apitypes.Tab) -> None:
    """Ensure the stylesheet is applied, including the site module when mapped.

    Runs on every load_finished/currentChanged so pages that lost the
    DocumentCreation injection (Qt 6.11) still get styled.
    """
    if tab in _plain:
        return
    css = _get_css()
    site = _site_css_for(tab.url().host())
    if site is not None:
        css += "\n" + site
    tab.run_js_async(_ensure_css_js(css))
    log.misc.debug("tabcss: stylesheet ensured on %s", tab.url().host())


#HACK: re-apply css on every load_finished as #8925 backstop; remove when fixed.
def _on_load_finished_ensure(tab: apitypes.Tab, ok: bool) -> None:
    if ok:
        _inject_site_css(tab)


def _apply_window(window) -> None:
    try:
        for i in range(window.tabbed_browser.widget.count()):
            tab = window.tabbed_browser.widget.widget(i)
            if tab is None:
                continue
            if tab not in _site_connected:
                #HACK: per-navigation ensure (see #8925); drop the connection with the hack.
                tab.load_finished.connect(
                    lambda ok, t=tab: _on_load_finished_ensure(t, ok)
                )
                _site_connected.add(tab)
            _inject_site_css(tab)  #HACK: ensure-on-every-switch (see #8925)
            if tab not in _restore_done:  #HACK: restore scripts (see #8925)
                _install_restore(tab)
                _restore_done.add(tab)
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

    _config_wired = False

    @pyqtSlot()
    def arm(self) -> None:
        try:
            if not _Scheduler._config_wired:
                from qutebrowser.config import config
                #HACK: refresh cache + restore scripts on styling changes (#8925).
                config.instance.changed.connect(_on_config_changed)
                _Scheduler._config_wired = True
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
