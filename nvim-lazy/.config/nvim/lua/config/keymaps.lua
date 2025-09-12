-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
local map = vim.keymap.set
local del = vim.keymap.del

map("n", "zo", "zMzvzz", { desc = "Unfold only at this level" })
map("n", "<C-g>u", "<cmd>GetCurrentBranchLink<CR>", { desc = "Get current branch link" })
map("n", "<C-A-j>", "<cmd>set paste<CR>m`o<ESC>``<cmd>set nopaste<CR>", { desc = "Add empty line above" })
map("n", "<C-A-k>", "<cmd>set paste<CR>m`O<ESC>``<cmd>set nopaste<CR>", { desc = "Add empty line below" })

local function yank_git_relative_path()
  -- Get the absolute path of the current buffer
  local current_file = vim.fn.expand("%:p")

  -- Check if a file is open in the current buffer
  if current_file == "" then
    print("No file open in the current buffer.")
    return
  end

  -- Get the Git repository root directory
  -- `git rev-parse --show-toplevel` returns the absolute path to the top-level directory
  -- of the Git repository. It does not include a trailing slash, unless the repository
  -- root is the filesystem root itself (i.e., "/").
  local git_root_cmd = "git rev-parse --show-toplevel"
  local git_root_raw = vim.fn.system(git_root_cmd)
  local git_root = vim.trim(git_root_raw)

  -- Check if the git command was successful (i.e., we are inside a Git repo)
  if vim.v.shell_error ~= 0 then
    print("Not inside a Git repository or 'git' command failed.")
    return
  end

  -- Normalize paths for consistent comparison. This helps by:
  -- - Removing redundant slashes (e.g., /a//b -> /a/b)
  -- - Resolving '..' and '.' components
  -- - Ensuring consistent path separator usage (though Neovim handles this well usually)
  current_file = vim.fs.normalize(current_file)
  git_root = vim.fs.normalize(git_root)

  local relative_path

  if current_file == git_root then
    -- If the current file is exactly the Git repository root (e.g., when browsing the root
    -- directory with Netrw or if the buffer itself represents the root).
    relative_path = "."
  elseif current_file:sub(1, #git_root) == git_root then
    -- Check if the current file path starts with the git_root path.
    -- Determine the position of the character immediately after the git_root.
    local char_after_git_root_pos = #git_root + 1

    -- Special handling for when the Git root is the filesystem root "/"
    if git_root == vim.fs.path_separator then
      -- If git_root is "/", we just need to remove that initial "/" from current_file.
      -- E.g., "/home/user/file.txt" becomes "home/user/file.txt"
      relative_path = current_file:sub(char_after_git_root_pos)
    -- For all other Git roots, we expect a path separator after the git_root to confirm
    -- that current_file is a subdirectory or file within the repository.
    elseif current_file:sub(char_after_git_root_pos, char_after_git_root_pos) == vim.fs.path_separator then
      -- If the character after git_root is a separator, remove git_root and that separator.
      -- E.g., "/repo/src/file.txt" relative to "/repo" becomes "src/file.txt"
      relative_path = current_file:sub(char_after_git_root_pos + 1)
    else
      -- This handles cases where `current_file` starts with `git_root` but is not a direct
      -- subdirectory (e.g., `git_root="/a/b"`, `current_file="/a/b_c/d"`).
      print("Current file is not a direct subdirectory of the Git repository root.")
      return
    end
  else
    -- Current file is not within the Git repository root (e.g., in a parent directory).
    print("Current file is not within the Git repository root.")
    return
  end

  -- Yank the calculated relative path to the unnamed register.
  -- If you have `set clipboard=unnamed` or `set clipboard=unnamedplus` in your Neovim config,
  -- this will automatically copy it to your system clipboard as well.
  vim.fn.setreg('"', relative_path)
  print("Yanked Git relative path: " .. relative_path)
end

-- Bind the function to a key.
-- The example uses `<leader>gy` (your leader key + 'g' + 'y').
-- You can change '<leader>gy' to any key combination you prefer.
vim.keymap.set("n", "<leader>gy", yank_git_relative_path, {
  desc = "Yank current buffer's file path relative to Git root",
})
