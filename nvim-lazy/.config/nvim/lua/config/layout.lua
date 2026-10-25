local M = {}

local defaults = {
  narrow_cols = 100,
}

local excluded_filetypes = {
  ["neo-tree"] = true,
  ["NvimTree"] = true,
  ["oil"] = true,
  ["aerial"] = true,
  ["sidekick_terminal"] = true,
  ["snacks_terminal"] = true,
  ["toggleterm"] = true,
  ["trouble"] = true,
  ["noice"] = true,
}

local opts = vim.deepcopy(defaults)
local auto_stacked = false
local timer = nil
local resize_callbacks = {}

local function code_windows()
  local ret = {}
  for _, win in ipairs(vim.api.nvim_tabpage_list_wins(0)) do
    if vim.api.nvim_win_get_config(win).relative == "" then
      local buf = vim.api.nvim_win_get_buf(win)
      if vim.bo[buf].buftype == "" and not excluded_filetypes[vim.bo[buf].filetype] then
        ret[#ret + 1] = win
      end
    end
  end
  return ret
end

local function side_by_side(wins)
  local cols = {}
  for _, win in ipairs(wins) do
    cols[vim.api.nvim_win_get_position(win)[2]] = true
  end
  return vim.tbl_count(cols) > 1
end

local function reversed(t)
  local ret = {}
  for i = #t, 1, -1 do
    ret[#ret + 1] = t[i]
  end
  return ret
end

local function reposition(wins, cmd)
  local cur = vim.api.nvim_get_current_win()
  for _, win in ipairs(wins) do
    if vim.api.nvim_win_is_valid(win) then
      vim.api.nvim_set_current_win(win)
      vim.cmd("wincmd " .. cmd)
    end
  end
  if vim.api.nvim_win_is_valid(cur) then
    vim.api.nvim_set_current_win(cur)
  end
end

function M.stack()
  local wins = code_windows()
  if #wins < 2 or not side_by_side(wins) then
    return false
  end
  reposition(wins, "J")
  return true
end

function M.unstack()
  local wins = code_windows()
  if #wins < 2 or side_by_side(wins) then
    return false
  end
  reposition(reversed(wins), "H")
  return true
end

function M.equalize()
  if #code_windows() < 2 then
    return
  end
  vim.cmd("wincmd =")
end

local function ui_bounds()
  local statusline = vim.o.laststatus ~= 0 and 1 or 0
  local bottom = vim.o.lines - vim.o.cmdheight - statusline
  local showtab = vim.o.showtabline == 2
    or (vim.o.showtabline == 1 and #vim.api.nvim_list_tabpages() > 1)
  local top = (showtab and vim.o.tabline ~= "") and 1 or 0
  return top, bottom
end

local function border_pad(cfg)
  local border = cfg.border
  if border == nil or border == "" or border == "none" then
    return 0
  end
  if type(border) == "table" then
    return #border > 0 and 1 or 0
  end
  return 1
end

-- Floats are always drawn above the normal window grid, so tabline/statusline
-- can never cover them. Keep editor-relative floats inside the content area.
local function clamp_float(win)
  if not vim.api.nvim_win_is_valid(win) then
    return
  end
  local cfg = vim.api.nvim_win_get_config(win)
  if cfg.relative ~= "editor" or cfg.external then
    return
  end
  local top, bottom = ui_bounds()
  local extend = border_pad(cfg) * 2
  local row, height = cfg.row, cfg.height
  local new_row = math.max(row, top)
  if new_row + height + extend > bottom then
    new_row = math.max(bottom - height - extend, top)
  end
  if new_row + height + extend > bottom then
    height = math.max(bottom - new_row - extend, 1)
  end
  if new_row ~= row or height ~= cfg.height then
    pcall(vim.api.nvim_win_set_config, win, {
      relative = cfg.relative,
      row = new_row,
      col = cfg.col,
      width = cfg.width,
      height = height,
    })
  end
end

local function clamp_all()
  for _, win in ipairs(vim.api.nvim_list_wins()) do
    clamp_float(win)
  end
end

function M.clamp_float(win)
  clamp_float(win)
end

function M.clamp_floats()
  clamp_all()
end

function M.on_resize(fn)
  resize_callbacks[#resize_callbacks + 1] = fn
end

local function dispatch_resize()
  local columns = vim.o.columns
  local narrow = columns < opts.narrow_cols
  if narrow and not auto_stacked then
    auto_stacked = M.stack()
  elseif not narrow and auto_stacked then
    M.unstack()
    auto_stacked = false
  end
  for _, fn in ipairs(resize_callbacks) do
    fn(columns)
  end
  clamp_all()
end

function M.setup(user)
  opts = vim.tbl_deep_extend("force", vim.deepcopy(defaults), user or {})
  local group = vim.api.nvim_create_augroup("responsive_layout", { clear = true })

  vim.api.nvim_create_user_command("LayoutToggle", function()
    if not M.unstack() then
      M.stack()
    end
  end, { desc = "Toggle split orientation" })

  vim.api.nvim_create_user_command("LayoutEqualise", M.equalize, { desc = "Equalise code splits" })

  vim.keymap.set("n", "<leader>w=", "<cmd>LayoutEqualise<cr>", { desc = "Equalise splits" })

  vim.api.nvim_create_autocmd("VimResized", {
    group = group,
    callback = function()
      if timer and not timer:is_closing() then
        timer:stop()
      else
        timer = vim.uv.new_timer()
      end
      timer:start(200, 0, function()
        vim.schedule(dispatch_resize)
      end)
    end,
  })

  vim.api.nvim_create_autocmd({ "WinNew", "WinClosed" }, {
    group = group,
    callback = function()
      vim.schedule(M.equalize)
    end,
  })

  vim.api.nvim_create_autocmd("WinNew", {
    group = group,
    callback = function()
      local win = vim.api.nvim_get_current_win()
      vim.schedule(function()
        clamp_float(win)
      end)
    end,
  })

  vim.api.nvim_create_autocmd("OptionSet", {
    group = group,
    pattern = { "showtabline", "laststatus", "cmdheight" },
    callback = function()
      vim.schedule(clamp_all)
    end,
  })
end

return M
