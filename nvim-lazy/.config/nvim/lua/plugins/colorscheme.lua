return {
  {
    "navarasu/onedark.nvim",
    priority = 1000,
    lazy = true,
    opts = {
      style = "deep",
      transparent = false,
      term_colors = false,
      lualine = {
        transparent = false,
      },
      colors = {
        dimmed_red = "#302734",
        dimmed_green = "#253233",
        dimmed_yellow = "#2F3133",
        dimmed_blue = "#1E2E43",
        dimmed_purple = "#2B2741",
        dimmed_cyan = "#1D313E",
        dimmed_orange = "#2E2C30",
        tbg_red = "#883D4A",
        tbg_green = "#537745",
        tbg_blue = "#2E6495",
        tbg_purple = "#713E8B",
        tbg_cyan = "#27707F",
        tbg_yellow = "#856F46",
        tbg_orange = "#604E49",
        tbg_grey = "#455574",
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
        ["@org.agenda.deadline"] = { fg = "$cyan" },
        ["@org.agenda.scheduled"] = { fg = "$purple" },
        ["@org.agenda.header"] = { fg = "$green", bg = "$dimmed_green", fmt = "bold" },
        ["@org.agenda.time_grid"] = { fg = "$red", fmt = "bold" },

        ["@org.plan.org"] = { fg = "$tbg_cyan" },
        ["@org.timestamp.active.org"] = { fg = "$tbg_purple" },
        ["@org.properties.org"] = { fg = "$tbg_cyan" },
        ["@org.properties.name.org"] = { fg = "$tbg_cyan", fmt = "bold" },
        ["@org.drawer.org"] = { fg = "none" },

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
        ["NeoTreeNormal"] = { bg = "$bg0" },
        ["NeoTreeNormalNC"] = { bg = "$bg0" },
        ["NeoTreeEndOfBuffer"] = { bg = "$bg0" },
        ["NeoTreeGitAdded"] = { fg = "$green" },
        ["NeoTreeGitModified"] = { fg = "$orange" },
        ["NeoTreeGitDeleted"] = { fg = "$red" },
        ["NeoTreeGitUntracked"] = { fg = "$purple" },
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
