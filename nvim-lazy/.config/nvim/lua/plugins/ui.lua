-- Getter for neo-tree source selector cached by editor.lua's after_render handler
_G.__cached_neo_tree_selector = nil
_G.__get_selector = function()
  return _G.__cached_neo_tree_selector or ""
end

return {
  {
    "akinsho/bufferline.nvim",
    config = function()
      local bufferline = require("bufferline")
      bufferline.setup({
        options = {
          buffer_close_icon = " ",
          always_show_bufferline = true,
          offsets = {
            {
              filetype = "neo-tree",
              raw = "%{%v:lua.__get_selector()%}",
              highlight = { sep = { link = "WinSeparator" } },
              separator = "┃",
            },
          },
          hover = {
            enabled = false,
            delay = 200,
            reveal = { "close" },
          },
        },
        highlights = {
          fill = {
            bg = "#21252b",
          },
        },
      })

      -- Patch bufferline's internal get_section_text to support raw offset field
      -- Reference: https://github.com/nvim-neo-tree/neo-tree.nvim/issues/1368
      local Offset = require("bufferline.offset")
      local get_func = Offset.get
      for i = 1, 100 do
        local name, val = debug.getupvalue(get_func, i)
        if name == "get_section_text" then
          local orig = val
          debug.setupvalue(get_func, i, function(size, highlight, offset, is_left)
            if offset.raw then
              local text = offset.raw
              if type(text) == "function" then text = text() end
              text = text or ""
              if offset.separator then
                local sep_icon = type(offset.separator) == "string" and offset.separator or "│"
                local sep = (highlight.sep or "") .. sep_icon
                return (not is_left and sep or "") .. text .. (is_left and sep or "")
              end
              return text
            end
            return orig(size, highlight, offset, is_left)
          end)
          break
        end
      end
    end,
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
