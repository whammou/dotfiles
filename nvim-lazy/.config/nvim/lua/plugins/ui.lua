return {
  {
    "akinsho/bufferline.nvim",
    opts = {
      options = {
        buffer_close_icon = " ",
        always_show_bufferline = true,
        hover = {
          enabled = false,
          delay = 200,
          reveal = { "close" },
        },
      },
      highlights = {
        --close_button_selected = {
        --  fg = "#1a212e",
        --},
        fill = {
          bg = "#283347",
        },
      },
    },
  },
  {
    "nvim-lualine/lualine.nvim",
    lazy = true,
    config = function()
      require("config.ui.lualine")
    end,
    -- opts = {
    --   sections = {
    --     lualine_z = { "filesize" },
    --   },
    -- },
  },
  {
    "folke/snacks.nvim",
    opts = {},
    keys = {
      { "<leader>n", false },
      {
        "<leader>N",
        function()
          if Snacks.config.picker and Snacks.config.picker.enabled then
            Snacks.picker.notifications()
          else
            Snacks.notifier.show_history()
          end
        end,
        desc = "Notification History",
      },
      {
        "<leader>un",
        function()
          Snacks.notifier.hide()
        end,
        desc = "Dismiss All Notifications",
      },
    },
  },
}
