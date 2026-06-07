local map = vim.keymap.set

for i = 1, 9 do
  map({ "n", "t" }, "<M-S-" .. i .. ">", function()
    local wins = vim.api.nvim_list_wins()
    if wins[i] then
      vim.api.nvim_set_current_win(wins[i])
    end
  end, { desc = "which_key_ignore" })
end

map("n", "<leader>ws", "<cmd>split # | wincmd p<CR>", { desc = "Split with prev buffer, keep focus" })
map("n", "<leader>wv", "<cmd>vsplit # | wincmd p<CR>", { desc = "Vsplit with prev buffer, keep focus" })
