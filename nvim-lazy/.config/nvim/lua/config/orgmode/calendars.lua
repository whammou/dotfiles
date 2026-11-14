local M = { default = "gcal", by_area = {}, by_calendar = {} }

-- The area -> calendar table lives next to the orgpush runner so the timer and
-- nvim read one file. The repo sits three levels above the config directory
-- (dotfiles/nvim-lazy/.config/nvim).
local function map_path()
  local dir = vim.uv.fs_realpath(vim.fn.stdpath("config")) or vim.fn.stdpath("config")
  return dir .. "/../../../orgpush/calendars.tsv"
end

function M.load()
  local ok, lines = pcall(vim.fn.readfile, map_path())
  if not ok then
    return M
  end
  for _, line in ipairs(lines) do
    local area, calendar = line:match("^([^\t#]+)\t([^\t]+)")
    if area and calendar then
      M.by_area[area] = calendar
      M.by_calendar[calendar] = M.by_calendar[calendar] or {}
      table.insert(M.by_calendar[calendar], area)
    end
  end
  return M
end

---Calendar of the buffer's area, or the default calendar when it has none.
function M.for_file(file)
  file = file or vim.api.nvim_buf_get_name(0)
  local area = file:match("/share/orgmode/([^/]+)/")
  if not area then
    return M.default
  end
  area = area:gsub("%s+$", "")
  return M.by_area[area] or M.default
end

return M
