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
    local command = {
      "pandoc",
      "--template=eisvogel",
      "--lua-filter=org-html-image.lua",
      "-o",
      target,
      current_file,
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
  P = eisvolgel_pdf,
}

require("orgmode").setup({
  org_custom_exports = custom_exports,
})
