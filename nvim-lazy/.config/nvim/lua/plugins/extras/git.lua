return {
  {
    "tpope/vim-fugitive",
    lazy = false,
    event = { "LazyFile" },
  },

  {
    "knsh14/vim-github-link",
    lazy = false,
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
    keys = {
      { "<leader>gH", "<cmd>LazyGitFilterCurrentFile<cr>", desc = "Lazygit filter current file" },
    },
  },

  {
    "Almo7aya/openingh.nvim",
    lazy = true,
    keys = {
      { "<leader>gr", "<cmd>OpenInGHRepo <CR>", desc = "Current GitHub repo" },
      { "<leader>gf", "<cmd>OpenInGHFile <CR>", desc = "Current File GitHub" },
      --{ "<leader>gf", "<cnd>OpenInGHFileLines <CR>", desc = "Current Line Github" },
    },
  },
}
