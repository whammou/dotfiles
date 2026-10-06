local map = vim.keymap.set

for i = 0, 9 do
  pcall(vim.keymap.del, "n", "<leader>w" .. i)
end

for i = 0, 9 do
  local target = i == 0 and 10 or i
  map("n", "<leader>w" .. i, function()
    local wins = vim.api.nvim_list_wins()
    if wins[target] then
      vim.api.nvim_set_current_win(wins[target])
    end
  end, { desc = "Go to window " .. target })
end

map("n", "<leader>ws", "<cmd>split # | wincmd p<CR>", { desc = "Split with prev buffer, keep focus" })
map("n", "<leader>wv", "<cmd>vsplit # | wincmd p<CR>", { desc = "Vsplit with prev buffer, keep focus" })
