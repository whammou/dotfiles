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

local eisvolgel_pdf = {
  label = "Export to Eisvogel PDF format",
  action = function(exporter)
    local current_file = vim.api.nvim_buf_get_name(0)
    local target = vim.fn.fnamemodify(current_file, ":p:r") .. ".pdf"
    -- sed 's/ \$\$/ $/g; s/\$\$ /$ /g' tasks/incidental.org | pandoc --template=eisvogel --lua-filter=org-html-image.lua -f org -t pdf -o tasks/incidental.pdf

    local command = {
      "eisvogel-pdf",
      current_file,
      target,
    }
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
  f = rtf_export,
  e = eisvolgel_pdf,
}

local khalorg_ok, khalorg = pcall(function()
  require("lazy").load({ plugins = { "nvim-khalorg" } })
  return require("khalorg")
end)

if khalorg_ok and khalorg then
  custom_exports.n = { label = "Add a khal event", action = function() return khalorg.new() end }
  custom_exports.k = { label = "Edit a khal event", action = function() return khalorg.edit() end }
  custom_exports.K = { label = "Edit a khal event and its dates", action = function() return khalorg.edit_all() end }
  custom_exports.D = { label = "Delete a khal event", action = function() return khalorg.delete() end }
end

require("orgmode").setup({
  org_custom_exports = custom_exports,
})
