local map = vim.keymap.set

-- local opt = vim.opt
--
-- opt.foldmethod = "indent"

vim.o.breakindent = true
vim.o.breakindentopt = "list:-1"

map("n", "<leader>ohl", "<leader>oih<leader>ols", { desc = "Create new headline with uuid" })
