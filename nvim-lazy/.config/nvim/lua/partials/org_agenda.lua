local Snacks = require("snacks")

vim.api.nvim_create_autocmd("BufEnter", {
  pattern = "orgagenda",
  callback = function()
    Snacks.zen.zoom()
    Snacks.bufdelete.other()
    vim.opt.spell = false
  end,
})
