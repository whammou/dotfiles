# OneDark Dark Variant — Color Palette Reference

## Source

Colors from `onedark.nvim` palette.lua `dark` variant, plus derived colors used across
kitty, dunst, opencode, qtile, qutebrowser, nvim, rofi, mpv, zathura, and lazygit configs.

---

## 1. Core Backgrounds

| Name     | Hex       | Usage                           |
|----------|-----------|---------------------------------|
| `black`  | `#181a1f` | Deepest bg (qutebrowser)        |
| `bg_d`   | `#21252b` | Borders, darkest panel          |
| `bg0`    | `#282c34` | **Main background**             |
| `bg1`    | `#31353f` | UI elements, code blocks        |
| `bg2`    | `#393f4a` | Hover, active states, borders   |
| `bg3`    | `#3b3f4c` | Accent backgrounds, code blocks |

## 2. Foreground / Text

| Name          | Hex       | Usage                |
|---------------|-----------|----------------------|
| `fg`          | `#abb2bf` | **Main text color**  |
| `grey`        | `#5c6370` | Muted text, metadata |
| `light_grey`  | `#848b98` | Secondary text       |
| `bg_blue`     | `#73b8f1` | Notification accent  |

## 3. Accent Colors (Bright)

Used directly for syntax highlighting, UI accents, status indicators.

| Name     | Hex       |
|----------|-----------|
| `red`    | `#e86671` |
| `green`  | `#98c379` |
| `yellow` | `#e5c07b` |
| `blue`   | `#61afef` |
| `purple` | `#c678dd` |
| `cyan`   | `#56b6c2` |
| `orange` | `#d19a66` |

## 4. Dimmed Accents — 50/50 Blend with Background

> `dimmed = round(0.5 × accent + 0.5 × bg0)`

Used for secondary UI (inactive borders, dimmed text, TODO keywords).

| Name          | Hex       | Derivation                      |
|---------------|-----------|---------------------------------|
| `dark_red`    | `#884953` | 50% `#e86671` + 50% `#282c34`  |
| `dark_green`  | `#607857` | 50% `#98c379` + 50% `#282c34`  |
| `dark_yellow` | `#877658` | 50% `#e5c07b` + 50% `#282c34`  |
| `dark_blue`   | `#456E92` | 50% `#61afef` + 50% `#282c34`  |
| `dark_purple` | `#775289` | 50% `#c678dd` + 50% `#282c34`  |
| `dark_cyan`   | `#3F717B` | 50% `#56b6c2` + 50% `#282c34`  |
| `dark_orange` | `#6e594f` | 50% `#d19a66` + 50% `#282c34`  |
| `color8`      | `#323640` | 50% bg3 `#3b3f4c` + 50% `#282c34` |
| `color15`     | `#565C66` | 50% light_grey `#848b98` + 50% `#282c34` |
| `borderSubtle`| `#2d313a` | 50% bg0 `#282c34` + 50% bg1 `#31353f` |

## 5. Dimmer Backgrounds — Subtle Heading BGs

> Offset from bg0 by the same delta as the original deep dimmed colors.

Used as heading backgrounds in orgmode, headlines, and qutebrowser.

| Name             | Hex       | For                |
|------------------|-----------|--------------------|
| `dimmed_cyan`    | `#2b3c44` | Headline1 / h1 bg   |
| `dimmed_purple`  | `#393247` | Headline2 / h2 bg   |
| `dimmed_blue`    | `#2c3949` | Headline3 / h3 bg   |
| `dimmed_yellow`  | `#3d3c39` | Headline4 / h4 bg   |
| `dimmed_green`   | `#333d39` | Headline5 / h5 bg   |
| `dimmed_red`     | `#3e323a` | Headline6 / h6 bg   |
| `dimmed_orange`  | `#3c3736` | misc                |

## 6. Diff / Git Colors

| Name                | Hex       | Usage            |
|---------------------|-----------|------------------|
| `diff_add`          | `#31392b` | Added lines bg   |
| `diff_delete`       | `#382b2c` | Deleted lines bg |
| `diff_change`       | `#1c3448` | Changed lines bg |
| `diff_text`         | `#2c5372` | Changed text bg  |
| `diffHighlightAdded` | `#a2bb9c` | 50% green + 50% fg |
| `diffHighlightRemoved` | `#ca8c98` | 50% red + 50% fg |
| `diffLineNumber`    | `#5c5e63` | proportional bg3→fg |
| `diffAddedLineNumberBg` | `#2d3527` | shift from diff_add |
| `diffRemovedLineNumberBg` | `#342728` | shift from diff_delete |

## 7. Terminal ANSI Mapping (kitty)

| ANSI | Hex       | Source     |
|------|-----------|------------|
| color0  (black)       | `#3b3f4c` | bg3        |
| color1  (red)         | `#e86671` | red        |
| color2  (green)       | `#98c379` | green      |
| color3  (yellow)      | `#e5c07b` | yellow     |
| color4  (blue)        | `#61afef` | blue       |
| color5  (magenta)     | `#c678dd` | purple     |
| color6  (cyan)        | `#56b6c2` | cyan       |
| color7  (white)       | `#848b98` | light_grey |
| color8  (bright-black) | `#323640` | 50% bg3 + 50% bg0 |
| color9  (bright-red)   | `#884953` | 50% red + 50% bg0 |
| color10 (bright-green) | `#607857` | 50% green + 50% bg0 |
| color11 (bright-yellow)| `#877658` | 50% yellow + 50% bg0 |
| color12 (bright-blue)  | `#456E92` | 50% blue + 50% bg0 |
| color13 (bright-magenta)| `#775289` | 50% purple + 50% bg0 |
| color14 (bright-cyan)  | `#3F717B` | 50% cyan + 50% bg0 |
| color15 (bright-white) | `#565C66` | 50% light_grey + 50% bg0 |

## 8. Quick Reference: All Alias Names by Config

```
Core palette name   kitty    qtile      qutebrowser      nvim-colorscheme
─────────────────────────────────────────────────────────────────────────
bg0                 bg       bg0        --od-bg0         —
bg1                 —        bg1        --od-bg1         —
bg2                 —        bg2        --od-bg2         —
bg3                 color0   bg3        --od-bg3         —
bg_d                —        —          --od-bg_d        —
fg                  fg       fg         --od-fg          —
grey                —        grey       --od-grey        tbg_grey
light_grey          color7   —          --od-light-grey  —
red                 color1   red        --od-red         —
green               color2   green      --od-green       —
yellow              color3   yellow     --od-yellow      —
blue                color4   blue/      --od-blue        —
                                    focus
purple              color5   purple     --od-purple      —
cyan                color6   cyan       --od-cyan        —
orange              —        orange     --od-orange      —
dark_red            color9   red_dimmed --od-dark-red    tbg_red
dark_green          color10  green_dimmed --od-dark-green tbg_green
dark_yellow         color11  yellow_dimmed --od-dark-yellow tbg_yellow
dark_blue           color12  blue_dimmed --od-dark-blue  tbg_blue
dark_purple         color13  purple_dimmed --od-dark-purple tbg_purple
dark_cyan           color14  cyan_dimmed --od-dark-cyan  tbg_cyan
dark_orange         —        —          —                tbg_orange
dimmed_cyan         —        —          --od-dimmed-cyan dimmed_cyan
dimmed_purple       —        —          --od-dimmed-purple dimmed_purple
dimmed_blue         —        —          --od-dimmed-blue dimmed_blue
dimmed_yellow       —        —          --od-dimmed-yellow dimmed_yellow
dimmed_green        —        —          --od-dimmed-green dimmed_green
dimmed_red          —        —          --od-dimmed-red  dimmed_red
dimmed_orange       —        —          —                dimmed_orange
```
