return {
  {
    "catppuccin/nvim",
    priority = 1000,
    lazy = true,
    config = function()
      require("config.extras.catppuccin")
    end,
  },
  {
    "LazyVim/LazyVim",
    opts = {
      colorscheme = "catppuccin-macchiato",
    },
  },
}
