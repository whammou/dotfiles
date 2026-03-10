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
      require("config.ui.evilline")
    end,
    -- opts = {
    --   sections = {
    --     lualine_z = { "filesize" },
    --   },
    -- },
  },
  -- lazy.nvim
  {
    "folke/noice.nvim",
    event = "VeryLazy",
    opts = {
      cmdline = {
        opts = {
          border = "single",
        },
      },
      cmdline_popup = {
        opt = {
          border = "single",
        },
      },
      views = {
        cmdline_popup = {
          border = { style = "none" },
        },
        popupmenu = {
          border = { style = "single" },
        },
      },
    },
  },
  {
    "folke/snacks.nvim",
    opts = {
      image = {
        doc = {
          inline = true,
        },
        math = {
          enabled = true,
          latex = {
            font_size = "Large",
            tpl = [[
              \documentclass[preview,border=0pt,varwidth,12pt]{standalone}
              \usepackage{${packages}}
              \begin{document}
              ${header}
              { \${font_size} \selectfont
                \color[HTML]{${color}}
              ${content}}
              \end{document}]],
          },
        },
      },
      picker = {
        enabled = false,
      },
      styles = {
        lazygit = {
          height = 0.5,
          position = "bottom",
        },
        terminal = {
          height = 0.3,
          position = "bottom",
        },
        notification = {
          border = "single",
          wo = {
            wrap = true,
          },
        },
        notification_history = {
          border = "single",
        },
        snacks_image = {
          relative = "cursor",
          border = "single",
          focusable = false,
          backdrop = false,
          row = 1,
          col = 1,
        },
      },
      dashboard = { enabled = false },
      notifier = {
        timeout = 1000,
      },
    },
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
  --{
  --  "tpope/vim-repeat",
  --  lazy = true,
  --  event = "VeryLazy",
  --  enabled = false,
  --},
}
