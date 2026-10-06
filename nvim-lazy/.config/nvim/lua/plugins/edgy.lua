return {
  "folke/edgy.nvim",
  event = "VeryLazy",
  init = function()
    vim.opt.splitkeep = "screen"
    vim.opt.laststatus = 3
  end,
  opts = {
    left = {
      { ft = "neo-tree", title = "Neo-Tree", size = { width = 25 }, wo = { winhighlight = "" } },
    },
    bottom = {
      { ft = "qf", title = "QuickFix", size = { height = 15 } },
      { ft = "help", size = { height = 20 } },
      { ft = "snacks_terminal", title = "Terminal", size = { height = 0.3 }, wo = { winhighlight = "" } },
      -- Enable when trouble is re-enabled:
      -- { ft = "trouble", title = "Trouble", size = { height = 10 } },
    },
    options = {
      left = { size = 25 },
      bottom = { size = 10 },
    },
    fix_win_height = true,
    wo = {
      winfixwidth = true,
      winfixheight = false,
      winbar = false,
    },
    animate = {
      enabled = false,
    },
    keys = {
      ["<c-w>e"] = function()
        require("edgy").toggle()
      end,
    },
  },
}
