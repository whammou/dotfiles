local orgmode = require("orgmode")

local buf_name = vim.api.nvim_buf_get_name(0)
if buf_name:match("orgagenda$") then
  orgmode.agenda:redo("mapping", true)
elseif buf_name:match("%.org$") then
  vim.cmd("silent! RoamUpdate!")
end
