# tabcss.py - per-tab user stylesheet toggle.
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

import json
import weakref

from qutebrowser.api import cmdutils, apitypes

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
