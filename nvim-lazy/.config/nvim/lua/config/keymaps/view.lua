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

local url_preview = require("config.url_preview")

local IMAGE_EXTS = {
  png = true, jpg = true, jpeg = true, gif = true, webp = true,
  svg = true, bmp = true, ico = true, avif = true, tif = true, tiff = true,
}

local function is_image_url(url)
  local lower = url:lower():gsub("[?#].*$", "")
  local ext = lower:match("%.([a-z0-9]+)$")
  return ext and IMAGE_EXTS[ext] or false
end

map("n", "P", function()
  -- Org [[id:UUID]] link preview (only check in org buffers)
  if vim.bo.filetype == "org" then
    local ok, mod = pcall(require, "config.orgmode.preview_id")
    if ok and mod.preview_id_link() then
      return
    end
  end

  local url = vim.fn.expand("<cfile>")
  if url and url:match("^https?://[^%s\"'<>()]+") and not is_image_url(url) then
    return url_preview.preview_url(url)
  end

  local ok, doc = pcall(require, "snacks.image.doc")
  if not ok then
    return
  end

  url_preview.close()

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
end, { desc = "Preview: org ID / URL / image" })
