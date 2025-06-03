-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua
--
-- Add any additional autocmds here
-- with `vim.api.nvim_create_autocmd`

-- Binding org-meta-return
vim.api.nvim_create_autocmd("FileType", {
  pattern = "org",
  callback = function()
    vim.keymap.set("i", "<S-CR>", '<cmd>lua require("orgmode").action("org_mappings.meta_return")<CR>', {
      silent = true,
      buffer = true,
    })
  end,
})

-- Disable tree-sitter for larg file
-- vim.api.nvim_create_autocmd({ "InsertLeave", "InsertEnter" }, {
--   pattern = "*",
--   callback = function()
--     if vim.api.nvim_buf_line_count(0) > 0 then
--       vim.cmd(
--         "TSToggle highlight autotag indent textobjects.swap textobjects.move textobjects.select increment_selection"
--       )
--     end
--   end,
-- })
-- Or remove existing autocmds by their group name (which is prefixed with `lazyvim_` for the defaults)
-- e.g. vim.api.nvim_del_augroup_by_name("lazyvim_wrap_spell")
