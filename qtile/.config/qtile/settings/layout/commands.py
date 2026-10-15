# Floating-window commands and shared helpers.
#
# Split from settings/layouts.py — pure window helpers with no hook
# subscriptions. Hook handlers live in .hooks and import from here.

# Window rules are defined once in settings/layouts.py (WIN_RULES) and
# sourced here via deferred import (avoids a circular import).


def _is_focus_allowed(window) -> bool:
    from settings.layouts import WIN_RULES

    for rule in WIN_RULES:
        try:
            match = rule.focus_match if rule.focus_match is not None else rule.match
            if rule.focus and match.compare(window):
                return True
        except Exception:
            continue
    return False


_hidden_geoms: dict[int, tuple[int, int, int, int]] = {}
_last_toggle_geoms: dict[int, tuple[int, int, int, int]] = {}


def _is_visible(win) -> bool:
    return not bool(getattr(win, "hidden", False) or getattr(win, "minimized", False))


def _save_geom(win) -> None:
    wid = getattr(win, "wid", None)
    if wid is None:
        return
    try:
        w, h, x, y = int(win.width), int(win.height), int(win.x), int(win.y)
        if w > 0 and h > 0:
            cur = (x, y, w, h)
            if _hidden_geoms.get(wid) != cur:
                _hidden_geoms[wid] = cur
    except Exception:
        pass


def _hide_all_in_group(group, exclude=None) -> None:
    if group is None:
        return
    for w in list(getattr(group, "windows", [])):
        if (
            w is exclude
            or getattr(w, "fullscreen", False)
            or not getattr(w, "floating", False)
        ):
            continue
        if _is_visible(w):
            hide_floating_win(w)


def _forget(wid: int | None) -> None:
    if wid is not None:
        _hidden_geoms.pop(wid, None)


def _forget_toggle(wid: int | None) -> None:
    if wid is not None:
        _last_toggle_geoms.pop(wid, None)


def _forget_all(wid: int | None) -> None:
    if wid is not None:
        _hidden_geoms.pop(wid, None)
        _last_toggle_geoms.pop(wid, None)


def _remember_toggle_geom(win) -> None:
    wid = getattr(win, "wid", None)
    if wid is None:
        return
    try:
        w, h, x, y = int(win.width), int(win.height), int(win.x), int(win.y)
        if w > 0 and h > 0:
            _last_toggle_geoms[wid] = (x, y, w, h)
    except Exception:
        pass


def _restore_toggle_geom(win) -> bool:
    wid = getattr(win, "wid", None)
    geom = _last_toggle_geoms.get(wid) if wid is not None else None
    if geom is not None:
        try:
            x, y, w, h = geom
            win.place(
                x,
                y,
                w,
                h,
                win.borderwidth,
                win.bordercolor,
                above=False,
                respect_hints=False,
            )
            try:
                win.bring_to_front()
            except Exception:
                pass
            return True
        except Exception:
            pass
    try:
        win.center()
    except Exception:
        pass
    return False


def hide_floating_win(win) -> None:
    if not getattr(win, "floating", False) or getattr(win, "fullscreen", False):
        return
    _save_geom(win)
    if not _is_visible(win):
        return
    try:
        if hasattr(win, "hide"):
            win.hide()
        elif hasattr(win, "minimized"):
            win.minimized = True  # type: ignore[attr-defined]
    except (AttributeError, RuntimeError):
        pass


def show_floating_win(win) -> None:
    if not getattr(win, "floating", False) or getattr(win, "fullscreen", False):
        return
    if _is_visible(win):
        try:
            win.bring_to_front()
        except Exception:
            pass
        return
    wid = getattr(win, "wid", None)
    geom = _hidden_geoms.pop(wid, None) if wid is not None else None
    try:
        if hasattr(win, "unhide"):
            win.unhide()
        elif hasattr(win, "minimized"):
            win.minimized = False  # type: ignore[attr-defined]
    except (AttributeError, RuntimeError):
        pass
    if geom is not None:
        try:
            x, y, w, h = geom
            win.place(
                x,
                y,
                w,
                h,
                win.borderwidth,
                win.bordercolor,
                above=False,
                respect_hints=False,
            )
        except Exception:
            pass
    try:
        win.bring_to_front()
    except Exception:
        pass


def toggle_floating_minimize(win) -> None:
    if not getattr(win, "floating", False) or getattr(win, "fullscreen", False):
        return
    hide_floating_win(win) if _is_visible(win) else show_floating_win(win)


def is_floating_hidden(win) -> bool:
    return bool(getattr(win, "floating", False) and not _is_visible(win))
