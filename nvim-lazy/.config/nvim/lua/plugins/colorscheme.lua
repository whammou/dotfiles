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
        bg_orange = "#604E49",
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
        ["@org.tag.org"] = { fg = "$grey", fmt = "italic" },
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
        ["@org.agenda.day"] = { fg = "none", fmt = "bold" },
        ["@org.agenda.today"] = { fg = "$yellow", fmt = "bold" },
        ["@org.agenda.weekend"] = { fg = "$red", fmt = "bold" },
        ["@org.agenda.deadline"] = { fg = "$cyan" },
        ["@org.agenda.header"] = { fg = "$blue", fmt = "bold,underline" },

        --Snack dashboard
        ["SnacksDashBoardHeader"] = { fg = "$fg" },
        ["SnacksDashBoardFooter"] = { fg = "$fg" },
        ["SnacksDashBoardSpecial"] = { fg = "$fg" },
        ["SnacksDashBoardDesc"] = { fg = "$fg" },
        ["SnacksDashBoardIcon"] = { fg = "$fg" },
        ["SnacksDashBoardKey"] = { fg = "$fg" },

        -- Nvim
        ["Conceal"] = { bg = "$bg0", fg = "$red" },
        ["SpellBad"] = { sp = "$orange", fmt = "underline" },
        ["CursorLineNr"] = { fg = "$orange", fmt = "bold" },
        ["CodeBlock"] = { bg = "$bg3" },

        -- Which-key
        ["WhichKeyDesc"] = { fg = "$green" },
        ["WhichKeySeparator"] = { fg = "$yellow" },

        -- Fzf-lua
        ["FzfLuaBorder"] = { fg = "$grey" },
        ["FzfLuaFzfPrompt"] = { fg = "$blue" },
        ["FzfLuaHeaderText"] = { fg = "$purple" },
        ["FzfLuaHeaderBind"] = { fg = "$green" },
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
