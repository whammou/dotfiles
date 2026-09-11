local lualine = require("lualine")

-- VSCode One Dark Pro palette using your onedark colors
-- statusBar.background #21252b (bg_d), tab.activeBackground #282c34 (bg0)
-- stylua: ignore
local colors = {
  bg       = '#21252b',
  bg0      = '#282c34',
  bg1      = '#31353f',
  fg       = '#abb2bf',
  light_grey = '#848b98',
  grey     = '#5c6370',
  yellow   = '#e5c07b',
  cyan     = '#56b6c2',
  darkblue = '#081633',
  green    = '#98c379',
  orange   = '#d19a66',
  violet   = '#c678dd',
  magenta  = '#c678dd',
  blue     = '#61afef',
  red      = '#e86671',
}

local conditions = {
  buffer_not_empty = function()
    return vim.fn.empty(vim.fn.expand("%:t")) ~= 1
  end,
  hide_in_width = function()
    return vim.fn.winwidth(0) > 80
  end,
  check_git_workspace = function()
    local filepath = vim.fn.expand("%:p:h")
    local gitdir = vim.fn.finddir(".git", filepath .. ";")
    return gitdir and #gitdir > 0 and #gitdir < #filepath
  end,
}

local config = {
  options = {
    component_separators = "",
    section_separators = "",
    theme = {
      normal = { c = { fg = colors.light_grey, bg = colors.bg } },
      inactive = { c = { fg = colors.light_grey, bg = colors.bg } },
    },
    globalstatus = true,
  },
  sections = {
    lualine_a = {},
    lualine_b = {},
    lualine_y = {},
    lualine_z = {},
    lualine_c = {},
    lualine_x = {},
  },
  inactive_sections = {
    lualine_a = {},
    lualine_b = {},
    lualine_y = {},
    lualine_z = {},
    lualine_c = {},
    lualine_x = {},
  },
}

local function ins_left(component)
  table.insert(config.sections.lualine_c, component)
end

local function ins_right(component)
  table.insert(config.sections.lualine_x, component)
end

ins_left({
  function()
    local mode_name = {
      n = "NORMAL",
      i = "INSERT",
      v = "VISUAL",
      [""] = "V-BLOCK",
      V = "V-LINE",
      c = "COMMAND",
      no = "NORMAL",
      s = "SELECT",
      S = "S-LINE",
      [""] = "S-BLOCK",
      ic = "INSERT",
      R = "REPLACE",
      Rv = "V-REPLACE",
      cv = "V-BLOCK",
      ce = "COMMAND",
      r = "REPLACE",
      rm = "MORE",
      ["r?"] = "CONFIRM",
      ["!"] = "SHELL",
      t = "TERMINAL",
    }
    return mode_name[vim.fn.mode()] or vim.fn.mode():upper()
  end,
  color = function()
    local mode_color = {
      n = { bg = colors.blue, fg = colors.bg, gui = "bold" },
      i = { bg = colors.green, fg = colors.bg, gui = "bold" },
      v = { bg = colors.violet, fg = colors.bg, gui = "bold" },
      [""] = { bg = colors.violet, fg = colors.bg, gui = "bold" },
      V = { bg = colors.violet, fg = colors.bg, gui = "bold" },
      c = { bg = colors.yellow, fg = colors.bg, gui = "bold" },
      no = { bg = colors.blue, fg = colors.bg, gui = "bold" },
      s = { bg = colors.orange, fg = colors.bg, gui = "bold" },
      S = { bg = colors.orange, fg = colors.bg, gui = "bold" },
      [""] = { bg = colors.orange, fg = colors.bg, gui = "bold" },
      ic = { bg = colors.yellow, fg = colors.bg, gui = "bold" },
      R = { bg = colors.red, fg = colors.bg, gui = "bold" },
      Rv = { bg = colors.red, fg = colors.bg, gui = "bold" },
      cv = { bg = colors.red, fg = colors.bg, gui = "bold" },
      ce = { bg = colors.red, fg = colors.bg, gui = "bold" },
      r = { bg = colors.cyan, fg = colors.bg, gui = "bold" },
      rm = { bg = colors.cyan, fg = colors.bg, gui = "bold" },
      ["r?"] = { bg = colors.cyan, fg = colors.bg, gui = "bold" },
      ["!"] = { bg = colors.red, fg = colors.bg, gui = "bold" },
      t = { bg = colors.red, fg = colors.bg, gui = "bold" },
    }
    return mode_color[vim.fn.mode()] or { bg = colors.blue, fg = colors.bg, gui = "bold" }
  end,
  padding = { left = 1, right = 1 },
})

ins_left({
  "branch",
  icon = "",
  color = { fg = colors.light_grey },
})

ins_left({
  "diagnostics",
  sources = { "nvim_diagnostic" },
  symbols = { error = " ", warn = " ", info = " " },
  diagnostics_color = {
    error = { fg = colors.red },
    warn = { fg = colors.yellow },
    info = { fg = colors.cyan },
  },
})

ins_left({
  "diff",
  symbols = { added = " ", modified = "󰝤 ", removed = " " },
  diff_color = {
    added = { fg = colors.green, gui = "bold" },
    modified = { fg = colors.orange, gui = "bold" },
    removed = { fg = colors.red, gui = "bold" },
  },
  colored = true,
})

ins_left({
  function()
    return "%="
  end,
})

ins_right({
  function()
    local line = vim.fn.line(".")
    local col = vim.fn.col(".")
    return string.format("Ln %d, Col %d", line, col)
  end,
  color = { fg = colors.light_grey },
})

ins_right({
  "o:encoding",
  fmt = string.upper,
  cond = conditions.hide_in_width,
  color = { fg = colors.light_grey },
})

ins_right({
  "fileformat",
  fmt = string.upper,
  icons_enabled = false,
  color = { fg = colors.light_grey },
})

ins_right({
  function()
    local msg = "inactive"
    local buf_ft = vim.api.nvim_get_option_value("filetype", { buf = 0 })
    local clients = vim.lsp.get_clients()
    if next(clients) == nil then
      return msg
    end
    for _, client in ipairs(clients) do
      local filetypes = client.config.filetypes
      if filetypes and vim.fn.index(filetypes, buf_ft) ~= -1 then
        return client.name
      end
    end
    return msg
  end,
  color = { fg = colors.light_grey },
})

ins_right({
  "filetype",
  cond = conditions.buffer_not_empty,
  icon_only = false,
  color = { fg = colors.light_grey },
})

ins_right({
  function()
    local ft = vim.api.nvim_get_option_value("filetype", { buf = 0 })
    if ft == "" then
      return ""
    end
    local cache = vim.g._lualine_version_cache or {}
    if cache[ft] then
      return cache[ft]
    end
    local version = ""
    if ft == "python" then
      if vim.fn.executable("python3") == 1 then
        version = vim.fn.system("python3 --version 2>&1"):gsub("\n", ""):gsub("Python ", "")
      elseif vim.fn.executable("python") == 1 then
        version = vim.fn.system("python --version 2>&1"):gsub("\n", ""):gsub("Python ", "")
      else
        return ""
      end
    elseif ft == "javascript" or ft == "typescript" or ft == "javascriptreact" or ft == "typescriptreact" then
      if vim.fn.executable("node") == 1 then
        version = vim.fn.system("node --version 2>&1"):gsub("\n", ""):gsub("v", "")
      else
        return ""
      end
    elseif ft == "lua" then
      version = _VERSION:gsub("Lua ", "")
    elseif ft == "go" then
      if vim.fn.executable("go") == 1 then
        version = vim.fn.system("go version 2>&1"):match("go version go([%d%.]+)")
        if not version then
          return ""
        end
      else
        return ""
      end
    elseif ft == "rust" then
      if vim.fn.executable("rustc") == 1 then
        version = vim.fn.system("rustc --version 2>&1"):match("rustc ([%d%.]+)")
        if not version then
          return ""
        end
      else
        return ""
      end
    else
      return ""
    end
    version = version:gsub("^%s+", ""):gsub("%s+$", "")
    cache[ft] = version
    vim.g._lualine_version_cache = cache
    return version
  end,
  cond = conditions.buffer_not_empty,
  color = { fg = colors.light_grey },
})

lualine.setup(config)
