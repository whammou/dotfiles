return {
  {
    "mikavilpas/yazi.nvim",
    enabled = false,
    event = "VeryLazy",
    keys = {
      {
        "<leader>ef",
        mode = { "n", "v" },
        "<cmd>Yazi<cr>",
        desc = "Open yazi at the current file",
      },
      {
        "<leader>er",
        function()
          local git_root = vim.fn.systemlist("git rev-parse --show-toplevel 2>/dev/null")[1]
          local root = git_root ~= "" and git_root or "/"
          require("yazi").yazi({}, root)
        end,
        desc = "Open yazi at git root or system root",
      },
      {
        "<leader>et",
        "<cmd>Yazi toggle<cr>",
        desc = "Resume the last yazi session",
      },
      {
        "<leader>es",
        "<cmd>edit scp://homelab//home/homelab/<cr>",
        desc = "Open remote home via netrw",
      },
    },
    opts = {
      open_for_directories = false,
      -- floating_window_scaling_factor = 0.7,
      yazi_floating_window_border = "single",
      highlights_groups = {
      hovered_buffer = { bg = "#393f4a" },
      hovered_buffer_in_same_directory = { bg = "#3b3f4c" },
      },
      keymaps = {
        show_help = "<f1>",
      },
      -- Make yazi window floats bat bottom
      hooks = {
        before_opening_window = function(options)
          options.col = vim.o.columns
          options.row = vim.o.lines
          options.height = math.floor(vim.o.lines / 2)
          options.width = vim.o.columns
        end,
      },
    },
    --init = function()
    --  vim.g.loaded_netrwPlugin = 0
    --  vim.g.loaded_netrw = 0
    --end,
  },
}
