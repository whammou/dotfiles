return {
  {
    "folke/which-key.nvim",
    opts = {
      preset = "classic",
      win = {
        border = "single",
      },
      icons = {
        separator = "",
      },
    },
  },
  {
    "ibhagwan/fzf-lua",
    -- optional for icon support
    dependencies = { "nvim-tree/nvim-web-devicons" },
    -- or if using mini.icons/mini.nvim
    -- dependencies = { "nvim-mini/mini.icons" },
    opts = {
      winopts = {
        split = "belowright new",
        border = "single",
      },
    },
  },
  -- lazy.nvim
  {
    "chrisgrieser/nvim-origami",
    event = "VeryLazy",
    opts = {
      foldtext = {
        lineCount = {
          template = "󰘖 %d",
        },
      },
    }, -- needed even when using default config

    -- recommended: disable vim's auto-folding
    -- init = function()
    --   vim.opt.foldlevel = 99
    --   vim.opt.foldlevelstart = 99
    -- end,
  },
}
