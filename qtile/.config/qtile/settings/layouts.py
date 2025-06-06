from libqtile import layout
from libqtile.config import Match
from qtile_bonsai import Bonsai
from libqtile import hook

from .theme import colors


@hook.subscribe.client_new
def center_floating_win(window):
    if window._wm_class[0] == "mpv-preview":
        window.keep_below(enable=True)
    if window._wm_class[0] == "feh":
        window.focus()


@hook.subscribe.client_new
def prevent_focus_steal(client):
    client.__class__.can_steal_focus = property(lambda self: False)


@hook.subscribe.client_focus
def set_hint(window):
    window.window.set_property(
        "IS_FLOATING", str(window.floating), type="STRING", format=8
    )


class MyCustomBonsai(Bonsai):
    def add_client(self, window):
        prev_window = self.focused_window
        super().add_client(window)
        if prev_window is not None:
            # Lord forgive me.
            self.group.qtile.call_soon(lambda: self.group.focus(prev_window))


layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(),
    MyCustomBonsai(
        **{
            "auto_cwd_for_terminals": False,
            "window.border_size": 2,
            "window.single.border_size": 2,
            "window.border_color": colors["bg0"],
            "window.active.border_color": colors["cyan"],
            "window.margin": [0, 3, 6, 3],
            "window.default_add_mode": "tab",
            "container_select_mode.border_color": colors["fg"],
            "container_select_mode.border_size": 2,
            "L1.tab_bar.hide_when": "always",
            "tab_bar.height": 6,
            "tab_bar.margin": [0, 3, 0, 3],
            "tab_bar.tab.font_size": 1,
            "L2.tab_bar.tab.bg_color": colors["cyan_dimmed"],
            "L2.tab_bar.tab.active.bg_color": colors["cyan"],
            "L3.tab_bar.tab.bg_color": colors["purple_dimmed"],
            "L3.tab_bar.tab.active.bg_color": colors["purple"],
            "L4.tab_bar.tab.bg_color": colors["blue_dimmed"],
            "L4.tab_bar.tab.active.bg_color": colors["blue"],
            "L5.tab_bar.tab.bg_color": colors["yellow_dimmed"],
            "L5.tab_bar.tab.active.bg_color": colors["yellow"],
            "L6.tab_bar.tab.bg_color": colors["green_dimmed"],
            "L6.tab_bar.tab.active.bg_color": colors["green"],
            "L7.tab_bar.tab.bg_color": colors["red_dimmed"],
            "L7.tab_bar.tab.active.bg_color": colors["red"],
        }
    ),
]

floating_layout = layout.Floating(
    border_width=2,
    border_focus=colors["cyan"],
    border_normal=colors["bg0"],
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="vimiv"),
        Match(wm_class="mpv-preview"),
        Match(wm_class="matplotlib"),
        Match(wm_class="feh"),
    ],
)
