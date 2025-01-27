-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
local map = vim.keymap.set

-- Fold
map("n", "zo", "zMzvzz", { desc = "Unfold only at this level" })

-- Git
map("n", "<C-g>s", "<cmd>Git | only<cr>")
map("n", "<C-g>u", "<cmd>GetCurrentBranchLink<CR>")

-- Edit
map("n", "<C-A-j>", "<cmd>set paste<CR>m`o<ESC>``<cmd>set nopaste<CR>")
map("n", "<C-A-k>", "<cmd>set paste<CR>m`O<ESC>``<cmd>set nopaste<CR>")
