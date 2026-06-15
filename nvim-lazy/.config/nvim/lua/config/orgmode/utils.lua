---@diagnostic disable: undefined-global

local dir = require("config.orgmode.directories")
local base_dir = dir.base_dir

local M = {}

function M.get_filename(directory)
  local filename = table.concat(
    vim.tbl_map(function(path)
      local filename = vim.fn.fnamemodify(path, ":t")
      return (string.gsub(filename, "%.org$", ""))
    end, vim.split(vim.fn.globpath(directory, "*.org"), "\n", { trimempty = true })),
    "|"
  )
  return filename
end

function M.get_file_path(directory, filename)
  local cmd = 'find "' .. vim.fn.fnamemodify(directory, ":p") .. '" -name ' .. filename .. " | paste -s -d '|'"
  local result = vim.fn.system(cmd)
  return string.gsub(string.gsub(result:gsub("\n$", ""), base_dir, ""), filename, "")
end

function M.get_dir_path(directory, filename)
  local cmd = 'find "' .. vim.fn.fnamemodify(directory, ":p") .. '" -type d -name ' .. filename .. " | paste -s -d '|'"
  local result = vim.fn.system(cmd)
  return string.gsub(result:gsub("\n$", ""), directory, "")
end

--- List all topic directories under topics/ for capture completion.
--- Always returns all topics regardless of whether subdirectories exist.
function M.get_topic_dirs()
  local topics_dir = dir.base_dir .. "topics/"
  local dirs = vim.fn.glob(topics_dir .. "*", 0, 1)
  local result = {}
  for _, d in ipairs(dirs) do
    if vim.fn.isdirectory(d) == 1 then
      table.insert(result, vim.fn.fnamemodify(d, ":t"))
    end
  end
  return table.concat(result, "|")
end

return M
