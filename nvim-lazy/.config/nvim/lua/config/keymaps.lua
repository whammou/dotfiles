local map = vim.keymap.set
local del = vim.keymap.del

map("n", "<leader>zc", function()
  require("chezmoi.pick").fzf()
end, { desc = "Chezmoi search all" })
for i = 1, 9 do
  vim.keymap.set({ "n", "t" }, "<leader>" .. i, function()
    vim.api.nvim_set_current_win(vim.api.nvim_list_wins()[i])
  end, { desc = "which_key_ignore" })
end

map("n", "zp", "zMzvzz", { desc = "Unfold only at this level" })
map("n", "zP", "zozczOzt", { desc = "Unfold levels below at this level" })
map("n", "<C-g>u", "<cmd>GetCurrentBranchLink<CR>", { desc = "Get current branch link" })
map("n", "<C-A-j>", "<cmd>set paste<CR>m`o<ESC>``<cmd>set nopaste<CR>", { desc = "Add empty line above" })
map("n", "<C-A-k>", "<cmd>set paste<CR>m`O<ESC>``<cmd>set nopaste<CR>", { desc = "Add empty line below" })

map("n", "<C-A-k>", "<cmd>set paste<CR>m`O<ESC>``<cmd>set nopaste<CR>", { desc = "Add empty line below" })

local function yank_git_relative_path()
  local current_file = vim.fn.expand("%:p")

  if current_file == "" then
    print("No file open in the current buffer.")
    return
  end

  local git_root_cmd = "git rev-parse --show-toplevel"
  local git_root_raw = vim.fn.system(git_root_cmd)
  local git_root = vim.trim(git_root_raw)

  if vim.v.shell_error ~= 0 then
    print("Not inside a Git repository or 'git' command failed.")
    return
  end

  current_file = vim.fs.normalize(current_file)
  git_root = vim.fs.normalize(git_root)

  local relative_path

  if current_file == git_root then
    relative_path = "."
  elseif current_file:sub(1, #git_root) == git_root then
    local char_after_git_root_pos = #git_root + 1

    if git_root == vim.fs.path_separator then
      relative_path = current_file:sub(char_after_git_root_pos)
    elseif current_file:sub(char_after_git_root_pos, char_after_git_root_pos) == vim.fs.path_separator then
      relative_path = current_file:sub(char_after_git_root_pos + 1)
    else
      print("Current file is not a direct subdirectory of the Git repository root.")
      return
    end
  else
    print("Current file is not within the Git repository root.")
    return
  end

  vim.fn.setreg('"', relative_path)
  print("Yanked Git relative path: " .. relative_path)
end

vim.keymap.set("n", "<leader>gy", yank_git_relative_path, {
  desc = "Yank current buffer's file path relative to Git root",
})
