return {
  {
    "navarasu/onedark.nvim",
    lazy = true,
    opts = {
      style = "deep",
      lualine = {
        transparent = false,
      },
      highlights = {
        ["@org.agenda.day"] = { fg = "none", fmt = "bold" },
        ["@org.agenda.today"] = { fg = "$yellow", fmt = "bold" },
        ["@org.agenda.weekend"] = { fg = "$red", fmt = "bold" },
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
