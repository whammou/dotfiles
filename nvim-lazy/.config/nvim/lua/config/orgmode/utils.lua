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

return M
