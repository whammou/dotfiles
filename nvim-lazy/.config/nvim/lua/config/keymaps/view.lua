local map = vim.keymap.set

map("n", "ze", "<cmd>e<CR>", { desc = "Edit current file" })
map("n", "zU", function()
  vim.cmd("loadview")
end, { desc = "Reload view current file" })
map("n", "zu", function()
  vim.cmd("e")
  vim.schedule(function()
    vim.cmd("loadview")
  end)
end, { desc = "Restore previous view" })

map("n", "P", function()
  local ok, doc = pcall(require, "snacks.image.doc")
  if not ok then
    return
  end
  local has_preview = false
  for _, win in ipairs(vim.api.nvim_list_wins()) do
    local cfg = vim.api.nvim_win_get_config(win)
    if type(cfg) == "table" and cfg.relative ~= "" and cfg.relative ~= vim.NIL then
      local buf = vim.api.nvim_win_get_buf(win)
      local ft = vim.bo[buf].filetype
      if
        ft == "alpha"
        or ft == "image"
        or ft:match("^snacks")
        or vim.api.nvim_buf_get_name(buf):match(".-_preview.-%.")
      then
        has_preview = true
        break
      end
    end
  end

  if has_preview then
    doc.hover_close()
  else
    doc.hover()
  end
end, { desc = "Toggle Snacks image preview" })
