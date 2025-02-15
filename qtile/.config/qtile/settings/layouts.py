from libqtile import layout
from libqtile.config import Match
from qtile_bonsai import Bonsai

layouts = [
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    #layout.Max(),
    Bonsai(**{
        "auto_cwd_for_terminals": False,
        "window.border_size": 0,
        "window.margin": [0, 3, 6, 3],
        "window.default_add_mode": "tab",
        "container_select_mode.border_color": "ff00ff",
        "container_select_mode.borser_size": 1,
        "L1.tab_bar.hide_when": "always",
        "tab_bar.height": 6,
        "tab_bar.margin": [0, 3, 0, 3],
        "tab_bar.tab.font_size": 1,
        "L2.tab_bar.tab.bg_color": "007676",
        "L2.tab_bar.tab.active.bg_color": "41a7fc",
        "L3.tab_bar.tab.bg_color": "500076",
        "L3.tab_bar.tab.active.bg_color": "c75ae8",
        #"L4.tab_bar.tab.bg_color": "76002a",
        #"L4.tab_bar.tab.active.bg_color": "ff005c",
    }),
]

floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
