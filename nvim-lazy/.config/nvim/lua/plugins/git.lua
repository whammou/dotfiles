return {
  {
    "lewis6991/gitsigns.nvim",
    -- Keep LazyVim's BufReadPre trigger but detach for org to avoid 200ms stall on Journal
    event = { "BufReadPre", "BufNewFile" },
    opts = function(_, opts)
      vim.api.nvim_create_autocmd("FileType", {
        pattern = "org",
        callback = function(args)
          vim.schedule(function()
            pcall(require("gitsigns").detach, args.buf)
          end)
        end,
      })
      return opts
    end,
  },
}
