return {
  {
    "tpope/vim-fugitive",
    lazy = true,
    event = "LazyFile",
  },

  {
    "knsh14/vim-github-link",
    lazy = true,
  },

  {
    "kdheepak/lazygit.nvim",
    lazy = true,
    cmd = {
      -- "LazyGit",
      -- "LazyGitConfig",
      -- "LazyGitCurrentFile",
      "LazyGitFilter",
      "LazyGitFilterCurrentFile",
    },
  },

  {
    "Almo7aya/openingh.nvim",
    lazy = true,
    event = "VeryLazy",
    keys = {
      { "<leader>gr", "<cmd>OpenInGHRepo <CR>", desc = "Current GitHub repo" },
      { "<leader>gf", "<cmd>OpenInGHFile <CR>", desc = "Current File GitHub" },
      { "v", "<leader>gf", "<cnd>OpenInGHFileLines <CR>", desc = "Current Line Github" },
    },
  },
}
