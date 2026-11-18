local orgmode = require("orgmode")

local function agenda_buffer()
  for _, bufnr in ipairs(vim.api.nvim_list_bufs()) do
    if vim.api.nvim_buf_is_loaded(bufnr) and vim.api.nvim_buf_get_name(bufnr):match("orgagenda$") then
      return bufnr
    end
  end
end

if agenda_buffer() then
  orgmode.agenda:redo("mapping", true)
elseif vim.api.nvim_buf_get_name(0):match("%.org$") then
  vim.cmd("silent! RoamUpdate!")
end
