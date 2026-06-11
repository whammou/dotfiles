return {
  {
    "michaelb/sniprun",
    enabled = false,
    build = "sh install.sh",
    lazy = true,
    ft = { "org", "python", "lua", "rust", "go", "c", "cpp", "javascript", "typescript", "bash", "sh" },
    config = function()
      require("sniprun").setup({
        selected_interpreters = {}, -- use defaults per filetype
        repl_enable = {},
        repl_disable = {},
        interpreter_options = {
          OrgMode_original = {
            -- Delegates to the underlying language interpreter (e.g. Python3_original)
          },
          Python3_original = {
            -- Point to the venv python so sniprun finds numpy, matplotlib, etc.
            -- Arch Linux discourages system pip installs; this venv is the clean workaround.
            interpreter = vim.fn.expand("~/.local/share/sniprun-venv/bin/python3"),
          },
        },
        display = {
          "Classic",
          "VirtualTextOk", -- ok results inline
          "VirtualTextErr", -- error results inline
        },
        display_options = {
          terminal_scrollback = vim.o.scrollback,
          terminal_line_number = false,
          terminal_signcolumn = false,
          terminal_position = "vertical",
          terminal_width = 45,
          terminal_height = 20,
          notification_timeout = 5,
          max_fw_width = 80,
        },
        show_no_output = { "Classic" },
        borders = "single",
      })
    end,
    keys = {
      -- Normal mode: run line or block under cursor
      {
        "<leader>rr",
        "<Plug>SnipRun",
        desc = "SnipRun (line/block)",
        ft = { "org" },
      },
      -- Visual mode: run selection
      {
        "<leader>rr",
        "<Plug>SnipRun",
        desc = "SnipRun (selection)",
        mode = "v",
        ft = { "org" },
      },
      -- Operator mode: combine with motion
      {
        "<leader>rf",
        "<Plug>SnipRunOperator",
        desc = "SnipRun operator",
        ft = { "org" },
      },
      -- Reset/kill running sniprun processes
      {
        "<leader>rR",
        "<cmd>SnipReset<CR>",
        desc = "SnipReset",
      },
      -- Clear virtual text / floating windows
      {
        "<leader>rc",
        "<cmd>SnipClose<CR>",
        desc = "SnipClose",
      },
      -- Info about current interpreter
      {
        "<leader>ri",
        "<cmd>SnipInfo<CR>",
        desc = "SnipInfo",
      },
      -- Run whole buffer
      {
        "<leader>ra",
        "<cmd>%SnipRun<CR>",
        desc = "SnipRun all blocks",
        ft = { "org" },
      },
      -- Toggle live mode
      {
        "<leader>rl",
        "<cmd>SnipLive<CR>",
        desc = "Toggle live mode",
      },
    },
    init = function()
      -- Org-mode specific autocmd mappings
      vim.api.nvim_create_autocmd("FileType", {
        pattern = "org",
        group = vim.api.nvim_create_augroup("sniprun-org", { clear = true }),
        callback = function(event)
          -- Run named block under cursor: place cursor on the #+NAME line
          -- and use :SnipRun <name>
        end,
      })
    end,
  },
}
