require("config.keymaps.chezmoi")
require("config.keymaps.window")
require("config.keymaps.view")
require("config.keymaps.fold")
require("config.keymaps.edit")
require("config.keymaps.git")

vim.api.nvim_create_autocmd({ "VimEnter", "User" }, {
  group = vim.api.nvim_create_augroup("UnbindLeaderE", { clear = true }),
  pattern = { "*", "VeryLazy" },
  callback = function(ev)
    if ev.event == "User" and ev.match ~= "VeryLazy" then
      return
    end
    pcall(vim.keymap.del, "n", "<leader>e")
    pcall(vim.keymap.del, "n", "<leader>E")
    pcall(vim.keymap.del, "v", "<leader>e")
    pcall(vim.keymap.del, "v", "<leader>E")
  end,
})
