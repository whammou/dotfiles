require("sidekick")

vim.api.nvim_create_autocmd("BufEnter", {
  callback = function()
    local buf_path = vim.api.nvim_buf_get_name(0)
    vim.b.sidekick_cwd = buf_path ~= "" and vim.fn.fnamemodify(buf_path, ":p:h") or vim.loop.cwd()
  end,
})

local opencode_project_id = os.getenv("OPENCODE_PROJECT_ID")
local opencode_server = os.getenv("OPENCODE_SERVER")

require("sidekick").setup({
  -- add any options here
  cli = {
    win = {
      layout = "bottom",
      split = {
        width = 0,
        height = 0,
      },
      config = function(terminal)
        local dir = vim.b.sidekick_cwd or vim.loop.cwd()
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
