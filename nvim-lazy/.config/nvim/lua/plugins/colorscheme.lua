return {
  {
    "navarasu/onedark.nvim",
    lazy = true,
    opts = {
      style = "deep",
      lualine = {
        transparent = true,
      },
      -- highlights = {
      --   ["@org.agenda.scheduled"] = { fg = "$blue" },
      -- },
    },
  },

  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "onedark",
    },
  },
}
