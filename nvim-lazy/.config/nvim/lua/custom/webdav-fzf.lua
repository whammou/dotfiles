--- webdav-fzf: Browse a WebDAV server via fzf-lua and insert URL at cursor.
--- Usage:
---   :WebdavFzf                    -- prompts for URL
---   :WebdavFzf https://example/   -- uses given URL
---
--- Requires: fzf-lua (ibhagwan/fzf-lua), rclone CLI

local fzf = require("fzf-lua")

local M = {}

--- URL-encode a path in pure Lua (handles UTF-8 multi-byte).
--- Keeps `/`, `.`, `-`, `_`, `~` and alphanumerics unencoded.
local function url_encode(str)
  local encoded = {}
  for i = 1, #str do
    local c = str:byte(i)
    if
      (c >= 48 and c <= 57) -- 0-9
      or (c >= 65 and c <= 90) -- A-Z
      or (c >= 97 and c <= 122) -- a-z
      or c == 46 -- .
      or c == 45 -- -
      or c == 95 -- _
      or c == 126 -- ~
      or c == 47 -- /
    then
      table.insert(encoded, string.char(c))
    else
      table.insert(encoded, string.format("%%%02X", c))
    end
  end
  return table.concat(encoded)
end

--- Prompt user for a WebDAV URL.
--- Uses vim.ui.input if available, falls back to vim.fn.input.
---@return string|nil
local function prompt_url()
  local input_fn
  local ok, ui_mod = pcall(require, "custom.ui")
  if ok and type(ui_mod) == "table" and type(ui_mod.input) == "function" then
    input_fn = ui_mod.input
  end

  if not input_fn then
    local ok_dressing, dressing = pcall(require, "dressing")
    if ok_dressing and dressing and vim.ui.input then
      input_fn = vim.ui.input
    end
  end

  if not input_fn then
    -- raw fallback
    local result = vim.fn.input({
      prompt = "WebDAV URL: ",
      default = "https://",
    })
    return (result ~= nil and result ~= "") and result or nil
  end

  -- async input via vim.ui.input pattern (yields to scheduler)
  local result
  input_fn({ prompt = "WebDAV URL: ", default = "https://" }, function(r)
    result = r
  end)
  vim.wait(30000, function()
    return result ~= nil
  end)
  return (result ~= nil and result ~= "") and result or nil
end

--- Open the fzf-lua WebDAV file picker.
---@param url string|nil WebDAV base URL. Prompts if nil or empty.
function M.browse(url)
  if not url or url == "" then
    url = os.getenv("WEBDAB_DRIVE") or prompt_url()
    if not url then
      return
    end
  end

  -- Normalise: strip trailing slash, then re-add one
  url = url:gsub("/+$", "") .. "/"

  if vim.fn.executable("rclone") == 0 then
    vim.notify("webdav-fzf: 'rclone' not found in PATH", vim.log.levels.ERROR)
    return
  end

  local function url_from_item(display)
    -- Strip ANSI escape codes (from icon coloring or path)
    local plain = display:gsub("\027%[[%d;]+m", "")
    -- Strip icon + U+2002 EN SPACE separator; remainder is the raw file path
    local file = plain:match("\xe2\x80\x82(.+)") or plain
    return url .. url_encode(file)
  end

  local cmd = string.format("rclone lsf :webdav: --webdav-url %q -R --files-only 2>/dev/null", url)
  fzf.fzf_exec(cmd, {
    prompt = "WebDAV> ",
    _type = "file",
    file_icons = true,
    color_icons = true,
    multiprocess = 1,
    actions = {
      ["default"] = function(selected, opts)
        local full_url = url_from_item(selected[1])
        local ctx = opts and opts.__CTX
        if ctx then
          vim.api.nvim_buf_set_text(
            ctx.bufnr,
            ctx.cursor[1] - 1,
            ctx.cursor[2],
            ctx.cursor[1] - 1,
            ctx.cursor[2],
            { full_url }
          )
        end
      end,
      ["ctrl-y"] = function(selected)
        local full_url = url_from_item(selected[1])
        vim.fn.setreg("+", full_url)
        vim.notify("Yanked: " .. full_url, vim.log.levels.INFO)
      end,
    },
    fzf_opts = {
      ["--bind"] = "ctrl-y:accept",
      ["--ansi"] = "",
    },
  })
end

--- Register the :WebdavFzf command.
vim.api.nvim_create_user_command("WebdavFzf", function(opts)
  M.browse(opts.args ~= "" and opts.args or nil)
end, {
  nargs = "?",
  desc = "Browse WebDAV files and insert URL at cursor",
})

return M
