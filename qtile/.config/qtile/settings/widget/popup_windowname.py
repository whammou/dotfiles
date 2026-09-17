from libqtile import hook, qtile
from libqtile.popup import Popup
from libqtile import pangocffi
from qtile_extras import widget as ext_widget

from ..theme import colors

popup = None
visible = False


class PopupWindowBox(ext_widget.WidgetBox):
    def toggle(self):
        toggle_popup_windowname(self.qtile)


def _get_text():
    try:
        win = qtile.current_window
        if win:
            title = win.name or ""
            wm_class = win.get_wm_class()
            if wm_class:
                text = f"{title} - {wm_class[0]}"
            else:
                text = title
            if len(text) > 60:
                text = text[:59] + "…"
            return pangocffi.markup_escape_text(text) if text else " "
        return " "
    except Exception:
        return " "


def _update_popup(*args, **kwargs):
    global popup, visible
    if popup is None or not visible:
        return
    try:
        text = _get_text()
        popup.layout.text = text
        try:
            popup.vertical_padding = max(0, (popup.height - popup.layout.height) // 2)
        except Exception:
            popup.vertical_padding = 0
        popup.clear()
        try:
            hp = getattr(popup, "horizontal_padding", 3) or 3
            lw = popup.layout.width or 0
            rx = max(int(hp), int(popup.width - int(lw) - int(hp)))
            popup.draw_text(x=rx, y=popup.vertical_padding)
        except Exception:
            popup.draw_text()
        popup.draw()
    except Exception:
        pass


def _create_popup():
    global popup, visible
    try:
        bar = None
        try:
            bar = qtile.current_screen.top
        except Exception:
            try:
                bar = qtile.screens[0].top
            except Exception:
                bar = None
        if bar is None:
            return
        popup = Popup(
            qtile,
            x=bar.x + bar.width - 500,
            y=bar.y,
            width=500,
            height=bar.height,
            background=colors["bg_d"],
            foreground=colors["light_grey"],
            font="HasklugNerdFont",
            fontsize=16,
            border_width=0,
            border=colors["bg_d"],
            opacity=1,
            horizontal_padding=3,
            vertical_padding=0,
            text_alignment="right",
        )
        visible = False
        popup.hide()

        def _on_click(x, y, button):
            if button == 1:
                toggle_popup_windowname()

        popup.win.process_button_click = _on_click

        hook.subscribe.client_focus(_update_popup)
        hook.subscribe.focus_change(_update_popup)
        hook.subscribe.float_change(_update_popup)
        hook.subscribe.client_name_updated(_update_popup)
        hook.subscribe.current_screen_change(_update_popup)
    except Exception:
        pass


def toggle_popup_windowname(qtile=None):
    global popup, visible
    import libqtile
    q = qtile if qtile is not None else libqtile.qtile
    if popup is None:
        _create_popup()
        if popup is None:
            return
    visible = not visible
    try:
        box = q.widgets_map.get("windowname_box") if q and hasattr(q, "widgets_map") else None
        if box is not None:
            box.box_is_open = visible
            box.set_box_label()
            try:
                box.bar.draw()
            except Exception:
                pass
    except Exception:
        pass
    if visible:
        try:
            bar = q.current_screen.top if q else None
            box = q.widgets_map.get("windowname_box") if q and hasattr(q, "widgets_map") else None
            if bar is not None and box is not None and hasattr(box, "offsetx"):
                popup.x = box.offsetx - popup.width
                if popup.x < bar.x:
                    popup.x = bar.x
            elif bar is not None:
                popup.x = bar.x + bar.width - popup.width
            else:
                popup.x = 0
            if bar is not None:
                popup.y = bar.y
                popup.height = bar.height
                popup.win.x = popup.x
                popup.win.y = popup.y
                popup.win.width = popup.width
                popup.win.height = popup.height
                popup.drawer.width = popup.width
                popup.drawer.height = popup.height
        except Exception:
            pass
        try:
            popup.unhide()
            popup.place()
        except Exception:
            pass
        _update_popup()
    else:
        try:
            popup.hide()
        except Exception:
            pass


hook.subscribe.startup_complete(_create_popup)
