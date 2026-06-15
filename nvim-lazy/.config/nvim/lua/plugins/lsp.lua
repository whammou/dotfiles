return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      folds = {
        enabled = true, -- prevents LazyVim's foldingRange handler from overriding orgmode's foldmethod
      },
      servers = {
        pyright = {
          handlers = {
            ["$/progress"] = function(err, result, ctx)
              if result and result.token then
                if result.token == (vim.g.pyright_progress_token or result.token) then
                  vim.g.pyright_progress_token = result.token
                  vim.lsp.handlers["$/progress"](err, result, ctx)
                end
              end
            end,
          },
        },
        pylsp = {
          handlers = {
            ["$/progress"] = function(err, result, ctx)
              if result and result.token then
                if result.token == (vim.g.pylsp_progress_token or result.token) then
                  vim.g.pylsp_progress_token = result.token
                  vim.lsp.handlers["$/progress"](err, result, ctx)
                end
              end
            end,
          },
        },
      },
    },
  },
}
