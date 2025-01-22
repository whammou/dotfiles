local map = vim.keymap.set

-- Navigation
-- Adding space above and below
map("n", "<A-j>", "<cmd>set paste<CR>m`o<ESC>``<cmd>set nopaste<CR>")
map("n", "<A-k>", "<cmd>set paste<CR>m`O<ESC>``<cmd>set nopaste<CR>")
map("n", "co", "<cmd>Bufonly<CR>")

-- Jump to "bad word" and open dictionary
map("n", "<C-[>s", "[sz=")
map("n", "<C-]>s", "]sz=")

-- Open ONLY current fold
map("n", "zo", "zMzvzz")


-- Git
map("n", "<C-g>s", "<cmd>Git | only<cr>")
map("n", "<C-g>u", "<cmd>GetCurrentBranchLink<CR>")

-- FZF
map("n", "<C-z>b", "<cmd>Buffers<CR>")
map("n", "<C-z>m", "<cmd>Marks<CR>")
map("n", "<C-z>l", "<cmd>Lines<CR>")
map("n", "<C-z>L", "<cmd>BLines<CR>")
map("n", "<C-z>f", "<cmd>Files<CR>")
map("n", "<C-z>R", "<cmd>RG<CR>")
map("n", "<C-z>ng", "<cmd>cd ~/notes | RG<CR>")
map("n", "<C-z>nl", "<cmd>cd ~/notes | Files<CR>")

-- Format
map("n", "<Leader>fr", "<cmd>set wrap!<CR>")
map("n", "<Leader>fs", "<cmd>set spell!<CR>")

-- Markdown
map("n", "<Leader>G", "<cmd>GripStart<CR>", { desc ="Render markdown in browser" })
