local map = vim.keymap.set

map("n", "ze", "<cmd>e<CR>", { desc = "Edit current file" })
map("n", "zU", function()
  vim.cmd("loadview")
end, { desc = "Reload view current file" })
map("n", "zu", function()
  vim.cmd("e")
  vim.schedule(function()
    vim.cmd("loadview")
  end)
end, { desc = "Restore previous view" })

