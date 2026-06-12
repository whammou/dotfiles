return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      folds = {
        enabled = true, -- prevents LazyVim's foldingRange handler from overriding orgmode's foldmethod
      },
    },
  },
}
