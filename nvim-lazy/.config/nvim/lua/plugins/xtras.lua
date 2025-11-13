return {

  {
    "norcalli/nvim-colorizer.lua",
    lazy = true,
    keys = {
      { "<leader>Ct", "<cmd>ColorizerToggle<CR>", desc = "Toggle color code" },
    },
    event = "VeryLazy",
    opts = {},
  },
  {
    "pysan3/fcitx5.nvim",
    -- lazy = true,
    event = "VeryLazy",
    opts = {},
  },
  {
    "tpope/vim-eunuch",
    lazy = true,
    event = "VeryLazy",
    -- Lua
    {
      "folke/persistence.nvim",
      event = "BufReadPre", -- this will only start session saving when an actual file was opened
      opts = {
        dir = vim.fn.stdpath("state") .. "/sessions/", -- directory where session files are saved
        -- minimum number of file buffers that need to be open to save
        -- Set to 0 to always save
        need = 0,
        branch = true, -- use git branch to save session
      },
    },
    {
      "rmagatti/auto-session",
      lazy = false,

      ---enables autocomplete for opts
      ---@module "auto-session"
      ---@type AutoSession.Config
      opts = {
        suppressed_dirs = { "~/", "~/Projects", "~/Downloads", "/" },
        -- log_level = 'debug',
      },
    },
  },
}
