require("sidekick")

vim.api.nvim_create_autocmd("BufEnter", {
  callback = function()
    local buf_path = vim.api.nvim_buf_get_name(0)
    vim.b.sidekick_cwd = buf_path ~= "" and vim.fn.fnamemodify(buf_path, ":p:h") or vim.loop.cwd()
  end,
})

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
        cmd = {
          "opencode",
          "attach",
          "-p",
          "Unlimitednova199-",
          "http://whamlab.sytes.net:5000",
          "--dir",
          "/tmp/placeholder",
        },
      },
    },
  },
})
