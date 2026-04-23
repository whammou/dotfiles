local Snacks = require("snacks")

vim.api.nvim_create_autocmd("BufWinEnter", {
  pattern = "orgagenda",
  once = true,
  callback = function()
    vim.defer_fn(function()
      Snacks.bufdelete.other()
      vim.cmd.only()
      vim.cmd("set foldmethod=indent")
    end, 0)
  end,
})
