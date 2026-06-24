--- Preview the target of an [[id:UUID]] link under the cursor.
--- Returns true if an id: link was handled, false if the cursor is not on an id: link
--- (allowing callers to fall through to other preview handlers).
local function preview_id_link()
  local ok, org = pcall(require, "orgmode")
  if not ok then
    return false
  end

  local instance = org.instance()
  if not instance or not instance.files then
    return false
  end

  local OrgHyperlink = require("orgmode.org.links.hyperlink")
  local link = OrgHyperlink.at_cursor()
  if not link then
    return false
  end

  if not link.url:is_id() then
    return false
  end

  local id = link.url:get_id()
  if not id or id == "" then
    return true
  end

  local headlines = instance.files:find_headlines_with_property("id", id)
  if #headlines == 0 then
    local files = instance.files:find_files_with_property("id", id)
    if #files == 0 then
      vim.notify("No node found with ID: " .. id, vim.log.levels.WARN)
      return true
    end
    vim.notify("File-level ID (opening file)", vim.log.levels.INFO)
    vim.cmd("edit " .. vim.fn.fnameescape(files[1].filename))
    return true
  end

  local hl = headlines[1]
  local lines = hl:get_lines()
  if #lines == 0 then
    return true
  end

  local offset = 4
  local width = lines[1]:len() + offset
  vim.tbl_map(function(line)
    width = math.max(width, line:len() + offset)
  end, lines)

  local win_opts = {
    width = width,
    wrap = true,
    border = "single",
    anchor_bias = "above",
    focusable = true,
  }

  local buf = vim.lsp.util.open_floating_preview(lines, "", win_opts)
  vim.api.nvim_set_option_value("filetype", "org", { buf = buf })

  pcall(vim.api.nvim_buf_clear_namespace, buf,
    vim.api.nvim_create_namespace("headlines_namespace"), 0, -1)

  return true
end

return { preview_id_link = preview_id_link }
