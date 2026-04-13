local map = vim.keymap.set

map("n", "<C-g>u", "<cmd>GetCurrentBranchLink<CR>", { desc = "Get current branch link" })
map("n", "<C-A-j>", "<cmd>set paste<CR>m`o<ESC>``<cmd>set nopaste<CR>", { desc = "Add empty line above" })
map("n", "<C-A-k>", "<cmd>set paste<CR>m`O<ESC>``<cmd>set nopaste<CR>", { desc = "Add empty line below" })