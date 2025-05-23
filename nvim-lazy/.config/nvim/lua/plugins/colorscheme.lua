return {
  {
    "navarasu/onedark.nvim",
    lazy = true,
    opts = {
      style = "deep",
      lualine = {
        transparent = false,
      },
      colors = {
        dimmed_red = "#830712",
        dimmed_green = "#406b20",
        dimmed_yellow = "#8f610d",
        dimmed_blue = "#024c8a",
        dimmed_purple = "#661280",
        dimmed_cyan = "#1b6a74",
      },
      highlights = {
        -- Orgmode agenda
        ["@org.agenda.day"] = { fg = "none", fmt = "bold" },
        ["@org.agenda.today"] = { fg = "$yellow", fmt = "bold" },
        ["@org.agenda.weekend"] = { fg = "$red", fmt = "bold" },

        -- Markdown headlines
        ["@markup.heading.1.markdown"] = { fg = "$cyan" },
        ["RenderMarkdownH1Bg"] = { bg = "$bg1" },
        ["@markup.heading.2.markdown"] = { fg = "$cyan" },
        ["RenderMarkdownH2Bg"] = { bg = "$bg1" },
        ["@markup.heading.3.markdown"] = { fg = "$red" },
        ["RenderMarkdownH3Bg"] = { bg = "$bg1" },
        ["@markup.heading.4.markdown"] = { fg = "$purple" },
        ["RenderMarkdownH4Bg"] = { bg = "$bg1" },
        ["@markup.heading.5.markdown"] = { fg = "$purple" },
        ["RenderMarkdownH5Bg"] = { bg = "$bg1" },
        ["@markup.heading.6.markdown"] = { fg = "$yellow" },
        ["RenderMarkdownH6Bg"] = { bg = "$bg1" },

        -- Orgmode headlines
        ["@org.headline.level1"] = { fg = "$cyan", fmt = "bold" },
        ["@org.headline.level2"] = { fg = "$cyan", fmt = "bold" },
        ["@org.headline.level3"] = { fg = "$red", fmt = "bold" },
        ["@org.headline.level4"] = { fg = "$purple", fmt = "bold" },
        ["@org.headline.level5"] = { fg = "$purple", fmt = "bold" },
        ["@org.headline.level6"] = { fg = "$yellow", fmt = "bold" },
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
