-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
local map = vim.keymap.set
local del = vim.keymap.del

map("n", "zo", "zMzvzz", { desc = "Unfold only at this level" })
map("n", "<C-g>u", "<cmd>GetCurrentBranchLink<CR>", { desc = "Get current branch link" })
map("n", "<C-A-j>", "<cmd>set paste<CR>m`o<ESC>``<cmd>set nopaste<CR>", { desc = "Add empty line above" })
map("n", "<C-A-k>", "<cmd>set paste<CR>m`O<ESC>``<cmd>set nopaste<CR>", { desc = "Add empty line below" })
