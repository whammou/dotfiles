return {
  {
    "navarasu/onedark.nvim",
    priority = 1000,
    lazy = true,
    opts = {
      style = "dark",
      transparent = false,
      term_colors = false,
      lualine = {
        transparent = false,
      },
      colors = {
        dimmed_red = "#3e323a",
        dimmed_green = "#333d39",
        dimmed_yellow = "#3d3c39",
        dimmed_blue = "#2c3949",
        dimmed_purple = "#393247",
        dimmed_cyan = "#2b3c44",
        dimmed_orange = "#3c3736",
        tbg_red = "#884953",
        tbg_green = "#607857",
        tbg_blue = "#456E92",
        tbg_purple = "#775289",
        tbg_cyan = "#3F717B",
        tbg_yellow = "#877658",
        tbg_orange = "#6e594f",
        tbg_grey = "#5c6370",
      },
      highlights = {

        -- Gitsign
        ["GitSignsChange"] = { fg = "$orange" },
        --["GitSignsChangeLn"] = { fg = "$orange" },

        -- Markdown headlines
        ["@markup.heading.1.markdown"] = { fg = "$cyan" },
        ["RenderMarkdownH1Bg"] = { bg = "$bg1" },
        ["@markup.heading.2.markdown"] = { fg = "$purple" },
        ["RenderMarkdownH2Bg"] = { bg = "$bg1" },
        ["@markup.heading.3.markdown"] = { fg = "$blue" },
        ["RenderMarkdownH3Bg"] = { bg = "$bg1" },
        ["@markup.heading.4.markdown"] = { fg = "$yellow" },
        ["RenderMarkdownH4Bg"] = { bg = "$bg1" },
        ["@markup.heading.5.markdown"] = { fg = "$green" },
        ["RenderMarkdownH5Bg"] = { bg = "$bg1" },
        ["@markup.heading.6.markdown"] = { fg = "$red" },
        ["RenderMarkdownH6Bg"] = { bg = "$bg1" },

        -- Orgmode
        ["@org.tag.org"] = { fg = "$tbg_grey", fmt = "none,italic" },
        ["@org.directive.org"] = { fg = "$tbg_grey", fmt = "none" },
        ["@org.block.org"] = { fg = "$tbg_grey", fmt = "none" },
        -- Orgmode markup
        ["@org.code"] = { fg = "$green", bg = "$bg2" },
        ["@org.code.delimeter"] = { fg = "$green", bg = "$bg2" },
        ["@org.verbatim"] = { fg = "$green", bg = "$bg2" },
        ["@org.verbatim.delimeter"] = { fg = "$green", bg = "$bg2" },
        -- Orgmode headlines
        ["@org.headline.level1"] = { fg = "$cyan", fmt = "bold" },
        ["@org.headline.level2"] = { fg = "$purple", fmt = "bold" },
        ["@org.headline.level3"] = { fg = "$blue", fmt = "bold" },
        ["@org.headline.level4"] = { fg = "$yellow", fmt = "bold" },
        ["@org.headline.level5"] = { fg = "$green", fmt = "bold" },
        ["@org.headline.level6"] = { fg = "$red", fmt = "bold" },
        -- Orgmode agenda
        ["@org.agenda.day"] = { fg = "none", fmt = "bold,italic" },
        ["@org.agenda.today"] = { fg = "$orange", fmt = "bold,italic" },
        ["@org.agenda.weekend"] = { fg = "$red", fmt = "bold,italic" },
        ["@org.agenda.weekend.today"] = { fg = "$orange", fmt = "bold,italic,underline" },
        ["@org.agenda.deadline"] = { fg = "$cyan" },
        ["@org.agenda.deadline.upcoming"] = { fg = "$yellow" },
        ["@org.agenda.scheduled"] = { fg = "$green" },
        ["@org.agenda.scheduled_past"] = { fg = "$red" },
        ["@org.agenda.header"] = { fg = "$green", bg = "$dimmed_green", fmt = "bold" },
        ["@org.agenda.time_grid"] = { fg = "$red", fmt = "bold" },

        ["@org.plan.org"] = { fg = "$tbg_cyan" },
        ["@org.timestamp.active.org"] = { fg = "$tbg_purple" },
        ["@org.properties.org"] = { fg = "$tbg_cyan" },
        ["@org.properties.name.org"] = { fg = "$tbg_cyan", fmt = "bold" },
        ["@org.drawer.org"] = { fg = "none" },
        ["OrgLinksLink"] = { fg = "$blue" },

        --Snack dashboard
        ["SnacksDashBoardHeader"] = { fg = "$fg" },
        ["SnacksDashBoardFooter"] = { fg = "$fg" },
        ["SnacksDashBoardSpecial"] = { fg = "$fg" },
        ["SnacksDashBoardDesc"] = { fg = "$fg" },
        ["SnacksDashBoardIcon"] = { fg = "$fg" },
        ["SnacksDashBoardKey"] = { fg = "$fg" },

        -- Math
        ["texMathZoneY"] = { bg = "none", fg = "$fg" },
        ["SnacksImageMath"] = { fg = "$fg", bg = "$bg3" },
        ["@markup.math"] = { fg = "$tbg_blue", bg = "none", fmt = "bold" },

        -- Nvim
        ["Conceal"] = { bg = "none", fg = "$tbg_blue", fmt = "bold" },
        ["SpellBad"] = { sp = "$orange", fmt = "underline" },
        ["CursorLineNr"] = { fg = "$orange", fmt = "bold" },
        ["Cursor"] = { fg = "$fg" },
        ["CodeBlock"] = { bg = "$bg3" },

        -- Which-key
        ["WhichKeyDesc"] = { fg = "$green" },
        ["WhichKeySeparator"] = { fg = "$yellow" },

        -- Fzf-lua
        ["FzfLuaBorder"] = { fg = "$grey" },
        ["FzfLuaFzfPrompt"] = { fg = "$blue" },
        ["FzfLuaHeaderText"] = { fg = "$purple" },
        ["FzfLuaHeaderBind"] = { fg = "$green" },

        -- Neo-tree
        --["NeoTreeNormal"] = { bg = "$bg_d" },
        --["NeoTreeNormalNC"] = { bg = "$bg_d" },
        --["NeoTreeEndOfBuffer"] = { bg = "$bg_d" },
        ["NeoTreeGitAdded"] = { fg = "$green" },
        ["NeoTreeGitModified"] = { fg = "$orange" },
        ["NeoTreeGitDeleted"] = { fg = "$red" },
        ["NeoTreeGitUntracked"] = { fg = "$purple" },
        ["NeoTreeWinseparator"] = { bg = "none" },
        ["NeoTreeRootName"] = { fg = "$blue" },
      },
    },
  },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "onedark",
    },
  },
}
