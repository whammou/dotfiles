return {
  -- {
  --   "tpope/vim-fugitive",
  --   lazy = false,
  -- },

  {
    "knsh14/vim-github-link",
    event = "VeryLazy",
  },
  {
    "kdheepak/lazygit.nvim",
    lazy = true,
    event = "VeryLazy",
    cmd = {
      "LazyGit",
      "LazyGitConfig",
      "LazyGitCurrentFile",
      "LazyGitFilter",
      "LazyGitFilterCurrentFile",
    },
    -- optional for floating window border decoration
    -- dependencies = {
    --   "nvim-lua/plenary.nvim",
    -- },
    -- setting the keybinding for LazyGit with 'keys' is recommended in
    -- order to load the plugin when the command is run for the first time
    --keys = {
    --  { "<leader>lg", "<cmd>LazyGit<cr>", desc = "LazyGit" },
    --},
  },
}
