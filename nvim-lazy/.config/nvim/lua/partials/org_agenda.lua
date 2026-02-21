---@diagnostic disable: undefined-global
local Snacks = require("snacks")

vim.api.nvim_create_autocmd("BufWinEnter", {
  pattern = "orgagenda",
  callback = function()
    --Snacks.zen.zoom()
    Snacks.bufdelete.other()
    vim.cmd.only()
    --vim.opt.spell = false
  end,
})
