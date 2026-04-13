local map = vim.keymap.set

map("n", "<leader>zc", function()
  require("chezmoi.pick").fzf()
end, { desc = "Chezmoi search all" })