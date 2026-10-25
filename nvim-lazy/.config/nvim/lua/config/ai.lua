require("sidekick")

vim.api.nvim_create_autocmd("BufEnter", {
  callback = function(ev)
    local buf = ev.buf or 0
    if vim.bo[buf].buftype ~= "" or vim.bo[buf].filetype == "sidekick_terminal" then
      return
    end
    local buf_path = vim.api.nvim_buf_get_name(buf)
    vim.b[buf].sidekick_cwd = buf_path ~= "" and vim.fn.fnamemodify(buf_path, ":p:h") or vim.uv.cwd()
  end,
})
-- init b var for already-entered buffers (lazy-load race on first toggle)
for _, buf in ipairs(vim.api.nvim_list_bufs()) do
  if vim.api.nvim_buf_is_valid(buf) and vim.bo[buf].buftype == "" and vim.bo[buf].filetype ~= "sidekick_terminal" then
    local name = vim.api.nvim_buf_get_name(buf)
    if vim.b[buf].sidekick_cwd == nil then
      vim.b[buf].sidekick_cwd = name ~= "" and vim.fn.fnamemodify(name, ":p:h") or vim.uv.cwd()
    end
  end
end

local opencode_project_id = os.getenv("OPENCODE_PROJECT_ID")
local opencode_server = os.getenv("OPENCODE_SERVER")

local sidekick_float_cols = 100

local function desired_layout()
  return vim.o.columns < sidekick_float_cols and "float" or "right"
end

local function refresh_float(terminal)
  local win = terminal.win
  if not (win and vim.api.nvim_win_is_valid(win)) then
    return
  end
  if vim.api.nvim_win_get_config(win).relative == "" then
    return
  end
  local opts = terminal.opts.float or {}
  local width = opts.width or 0.9
  local height = opts.height or 0.9
  local row = opts.row or 0.5
  local col = opts.col or 0.5
  width = width <= 1 and math.floor(vim.o.columns * width) or width
  height = height <= 1 and math.floor(vim.o.lines * height) or height
  row = row <= 1 and math.floor((vim.o.lines - height) * row) or row
  col = col <= 1 and math.floor((vim.o.columns - width) * col) or col
  pcall(vim.api.nvim_win_set_config, win, {
    relative = "editor",
    row = row,
    col = col,
    width = width,
    height = height,
  })
end

require("sidekick").setup({
  cli = {
    picker = "fzf-lua",
    win = {
      layout = desired_layout(),
      float = {
        border = "single",
      },
      split = {
        width = 0,
        height = 0,
      },
      keys = {
        stopinsert = false,
        escape = { "<esc><esc>", "stopinsert", mode = "t", desc = "enter normal mode" },
      },
      config = function(terminal)
        terminal.opts.layout = desired_layout()
        terminal.opts.float = terminal.opts.float or {}
        terminal.opts.float.border = "single"

        local buf_dir = function(buf)
          local n = vim.api.nvim_buf_get_name(buf)
          return n ~= "" and vim.fn.fnamemodify(n, ":p:h") or nil
        end
        local dir = vim.b.sidekick_cwd
        if not dir or dir == "" or vim.bo[vim.api.nvim_get_current_buf()].filetype == "sidekick_terminal" then
          dir = buf_dir(vim.api.nvim_get_current_buf())
          if not dir or vim.bo[vim.api.nvim_get_current_buf()].filetype == "sidekick_terminal" then
            for _, win in ipairs(vim.api.nvim_list_wins()) do
              local b = vim.api.nvim_win_get_buf(win)
              if vim.bo[b].filetype ~= "sidekick_terminal" and vim.bo[b].buftype == "" then
                dir = vim.b[b].sidekick_cwd or buf_dir(b)
                if dir then
                  break
                end
              end
            end
          end
        end
        dir = dir and vim.fs.normalize(dir) or vim.fn.getcwd(0) or vim.uv.cwd()
        terminal.cwd = dir
        for i, arg in ipairs(terminal.tool.cmd) do
          if arg == "--dir" then
            terminal.tool.cmd[i + 1] = dir
            return
          end
        end
        terminal.tool.cmd[#terminal.tool.cmd] = dir
      end,
    },
    mux = {
      backend = "tmux",
      enabled = false,
    },
    tools = {
      opencode = {
        cmd = { "opencode", "--continue", "/tmp/placeholder" },
      },
      opencode_attach = {
        cmd = {
          "opencode",
          "attach",
          "-p",
          opencode_project_id,
          opencode_server,
          "--continue",
          "--dir",
          "/tmp/placeholder",
        },
      },
    },
  },
})

local function apply_sidekick_layout(layout)
  local ok_config, Config = pcall(require, "sidekick.config")
  if ok_config and Config.cli and Config.cli.win then
    Config.cli.win.layout = layout
  end
  local ok_term, Terminal = pcall(require, "sidekick.cli.terminal")
  if not ok_term then
    return
  end
  for _, terminal in ipairs(Terminal.sessions()) do
    if terminal.opts then
      terminal.opts.float = terminal.opts.float or {}
      terminal.opts.float.border = "single"
      if terminal.opts.layout ~= layout then
        local was_focused = terminal.is_focused and terminal:is_focused()
        terminal.opts.layout = layout
        if terminal.is_open and terminal:is_open() then
          terminal:hide()
          terminal:show()
          if (layout == "float" or was_focused) and terminal.focus then
            terminal:focus()
          end
        end
      elseif layout == "float" then
        refresh_float(terminal)
      end
    end
  end
end

require("config.layout").on_resize(function(columns)
  apply_sidekick_layout(columns < sidekick_float_cols and "float" or "right")
end)

return {
  desired_layout = desired_layout,
}
