--- color-picker: fzf-lua picker for colorscheme palette colors.
---
--- Extracts the NAMED color variables from the active colorscheme
--- (e.g. onedark's `dimmed_red = "#3e323a"`) and presents them
--- in an fzf-lua picker.  On Enter, inserts the hex at cursor.
---
--- Usage:
---   :lua require("custom.color-picker").pick()
---   (or via the registered <leader>uC keymap)

local fzf = require("fzf-lua")

local M = {}

-- ── Colorscheme palette adapters ──────────────────────────────────

local palette_adapters = {}

--- navarasu/onedark.nvim
palette_adapters["onedark"] = function()
  local ok_pal, palette = pcall(require, "onedark.palette")
  if not ok_pal then
    return nil
  end
  local config = vim.g.onedark_config or {}
  local style = config.style or "dark"
  local base = palette[style] or palette.dark or {}
  return vim.tbl_extend("force", base, config.colors or {})
end

--- Generic fallback via highlight groups.
local function fallback_palette()
  local hls = vim.api.nvim_get_hl(0, {})
  local seen = {}
  local colors = {}
  for name, hl in pairs(hls) do
    if hl.link then
      local resolved = vim.api.nvim_get_hl(0, { name = hl.link })
      if resolved then
        if resolved.fg and not seen[resolved.fg] then
          seen[resolved.fg] = true
          colors[name .. ":fg"] = string.format("#%06x", resolved.fg)
        end
        if resolved.bg and not seen[resolved.bg] then
          seen[resolved.bg] = true
          colors[name .. ":bg"] = string.format("#%06x", resolved.bg)
        end
      end
    else
      if hl.fg and not seen[hl.fg] then
        seen[hl.fg] = true
        colors[name .. ":fg"] = string.format("#%06x", hl.fg)
      end
      if hl.bg and not seen[hl.bg] then
        seen[hl.bg] = true
        colors[name .. ":bg"] = string.format("#%06x", hl.bg)
      end
    end
  end
  return colors
end

---@return table<string,string>  { name = "#hex", ... }
function M.get_palette()
  local cs_name = vim.g.colors_name or ""
  local adapter = palette_adapters[cs_name]
  if adapter then
    local ok, result = pcall(adapter)
    if ok and result and next(result) then
      return result
    end
  end
  return fallback_palette()
end

-- ── Main picker entry point ──────────────────────────────────────

--- Open the fzf-lua colorscheme palette color picker.
function M.pick()
  local palette = M.get_palette()
  local count = 0
  for _ in pairs(palette) do
    count = count + 1
  end

  if count == 0 then
    vim.notify("No colorscheme palette colors found", vim.log.levels.WARN)
    return
  end

  -- Show "name  #hex" in the picker list.
  local names = vim.tbl_keys(palette)
  table.sort(names)
  local entries = {}
  for _, name in ipairs(names) do
    table.insert(entries, string.format("%s  %s", name, palette[name]))
  end

  fzf.fzf_exec(entries, {
    prompt = "Palette> ",
    actions = {
      ["default"] = function(selected)
        local hex = selected[1]:match("(#%x+)")
        if hex then
          vim.fn.setreg("+", hex)
          vim.api.nvim_put({ hex }, "c", false, true)
        end
      end,
      ["ctrl-y"] = function(selected)
        local hex = selected[1]:match("(#%x+)")
        if hex then
          vim.fn.setreg("+", hex)
        end
      end,
    },
  })
end

return M
