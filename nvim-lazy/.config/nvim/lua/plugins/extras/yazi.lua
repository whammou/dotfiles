return {
  {
    "mikavilpas/yazi.nvim",
    event = "VeryLazy",
    keys = {
      {
        "<leader>e",
        mode = { "n", "v" },
        "<cmd>Yazi<cr>",
        desc = "Open yazi at the current file",
      },
      {
        "<leader>E",
        "<cmd>Yazi cwd<cr>",
        desc = "Open the file manager in nvim's working directory",
      },
      {
        "<c-up>",
        "<cmd>Yazi toggle<cr>",
        desc = "Resume the last yazi session",
      },
    },
    opts = {
      open_for_directories = true,
      --floating_window_scaling_factor = 0.7,
      yazi_floating_window_border = "single",
      highlights_groups = {
        hovered_buffer = { bg = "#283347" },
        hovered_buffer_in_same_directory = { bg = "#2a324a" },
      },
      keymaps = {
        show_help = "<f1>",
      },
      hooks = {
        before_opening_window = function(options)
          options.col = vim.o.columns
          options.row = vim.o.lines
          options.height = math.floor(vim.o.lines / 2)
          options.width = vim.o.columns
        end,
      },
    },
    init = function()
      vim.g.loaded_netrwPlugin = 1
      vim.g.loaded_netrw = 1
    end,
  },
}
