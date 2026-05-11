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
      presets = {
        lsp_doc_border = false, -- disable rounded LSP doc borders
        command_palette = false, -- disable palette preset that force-overrides borders to rounded
      },
      views = {
        cmdline_popup = {
          border = { style = "single" },
          position = { row = 3, col = "50%" },
          size = { min_width = 60, width = "auto", height = "auto" },
        },
        cmdline_popupmenu = {
          border = { style = "single" },
          position = { row = 6, col = "50%" },
          size = { width = 60, height = "auto", max_height = 15 },
          win_options = {
            winhighlight = { Normal = "Normal", FloatBorder = "NoiceCmdlinePopupBorder" },
          },
        },
        cmdline_input = { border = { style = "single" } },
        popupmenu = { border = { style = "single" } },
        popup = { border = { style = "single" } },
        hover = { border = { style = "single" } },
        confirm = { border = { style = "single" } },
      },
    },
  },
  {
    "folke/snacks.nvim",
    opts = {
      image = {
        enabled = true,
        doc = {
          enabled = false, -- Enable document rendering for org files
          inline = false,
          float = true,
          max_width = 100,
          max_height = 50,
        },
        convert = {
          notify = true,
          mermaid = { "-i", "{src}", "-o", "{file}", "-b", "transparent", "-t", "dark", "-e", "png", "-s", "2" },
          -- PlantUML: requires plantuml (brew install plantuml)
          plantuml = {
            "-charset",
            "utf8",
            "{src}",
            "-tp",
            "png",
            "-o",
            "{file}",
          },
        },
        math = {
          enabled = true,
          latex = {
            font_size = "Large",
            color = "E63946",
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
          border = "single",
          height = 0.5,
          position = "bottom",
        },
        terminal = {
          border = "single",
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
        timeout = 5000,
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
