-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua
--
-- Add any additional autocmds here
-- with `vim.api.nvim_create_autocmd`

vim.api.nvim_create_user_command("Redir", function(ctx)
  local lines = vim.split(vim.api.nvim_exec(ctx.args, true), "\n", { plain = true })
  vim.cmd("new")
  vim.api.nvim_buf_set_lines(0, 0, -1, false, lines)
  vim.opt_local.modified = false
end, { nargs = "+", complete = "command" })
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

-- via an autocmd
vim.api.nvim_create_autocmd("BufEnter", {
  pattern = "org-roam-select",
  callback = function()
    vim.b.completion = false
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

-- Function to find the project root.
-- It looks for common markers like .git, .svn, or specific files.
local function find_project_root()
  -- You can customize these markers
  local markers = { ".git", "init.lua", "package.json", "pyproject.toml", "Cargo.toml", "go.mod" }

  -- Get the directory of the current file
  local current_file_path = vim.fn.expand("%:p")
  if current_file_path == "" then
    return nil
  end -- No file open
  local current_dir = vim.fn.fnamemodify(current_file_path, ":h")

  -- Traverse up the directory tree
  return vim.fs.find(markers, { path = current_dir, upward = true, type = "directory" })[1]
    or vim.fs.find(markers, { path = current_dir, upward = true, type = "file" })[1]
end

-- Function to copy the relative path
--function CopyRelativePath()
--  local root_marker_path = find_project_root()
--
--  if not root_marker_path then
--    print("Error: Project root not found.")
--    return
--  end
--
--  -- The root is the directory containing the marker
--  local project_root = vim.fn.fnamemodify(root_marker_path, ":h")
--  local file_path = vim.fn.expand("%:p")
--
--  -- Make the file path relative to the project root
--  local relative_path = vim.fn.fnamemodify(file_path, ":~:.")
--
--  -- On Windows, vim.fn.fnamemodify can be inconsistent, so we can do a string replacement
--  if vim.fn.has("win32") == 1 then
--    relative_path = file_path:sub(#project_root + 2) -- +2 for the trailing slash
--    relative_path = relative_path:gsub("\\", "/") -- Optional: convert to forward slashes
--  else
--    relative_path = file_path:sub(#project_root + 2)
--  end
--
--  if relative_path and relative_path ~= "" then
--    vim.fn.setreg("+", relative_path)
--    print("Copied to clipboard: " .. relative_path)
--  else
--    print("Error: Could not determine relative path.")
--  end
--end

-- Create a user command
--vim.api.nvim_create_user_command("CopyRelativePath", CopyRelativePath, {})
--
---- Create a keymap. <leader>yr stands for "yank relative"
---- Use 'n' for normal mode.
--vim.keymap.set("n", "<leader>yr", "<Cmd>CopyRelativePath<CR>", {
--  noremap = true,
--  silent = true,
--  desc = "Copy relative path to project root",
--})
