local orgmode = require("orgmode")
local khalorg = require("khalorg")
local roam = require("org-roam")
local Menu = require("org-modern.menu")

local rtf_export = {
  label = "Export to RTF format",
  action = function(exporter)
    local current_file = vim.api.nvim_buf_get_name(0)
    local target = vim.fn.fnamemodify(current_file, ":p:r") .. ".rtf"
    local command = { "pandoc", current_file, "-o", target }
    local on_success = function(output)
      print("Success!")
      vim.api.nvim_echo({ { table.concat(output, "\n") } }, true, {})
    end
    local on_error = function(err)
      print("Error!")
      vim.api.nvim_echo({ { table.concat(err, "\n"), "ErrorMsg" } }, true, {})
    end
    return exporter(command, target, on_success, on_error)
  end,
}

local custom_exports = {
  n = { label = "Add a new khal item", action = khalorg.new },
  d = { label = "Delete a khal item", action = khalorg.delete },
  e = { label = "Edit properties of a khal item", action = khalorg.edit },
  E = { label = "Edit properties & dates of a khal item", action = khalorg.edit_all },
  f = rtf_export,
}

require("orgmode").setup({
  org_custom_exports = custom_exports,
})
