local orgmode = require("orgmode")

if vim.api.nvim_buf_get_name(0):match("orgagenda$") then
  orgmode.agenda:redo("mapping", true)
  print("Refresh orgmode agenda")
end
