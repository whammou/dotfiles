-- Getter for neo-tree source selector cached by editor.lua's after_render handler.
-- Visibility is derived from live windows at render time, so the tabline is
-- always correct the instant the tree closes, regardless of cache/event timing.
_G.__cached_neo_tree_selector = nil
_G.__get_selector = function()
  for _, win in ipairs(vim.api.nvim_tabpage_list_wins(0)) do
    if vim.bo[vim.api.nvim_win_get_buf(win)].filetype == "neo-tree" then
      return _G.__cached_neo_tree_selector or ""
    end
  end
  return ""
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
              if type(text) == "function" then
                text = text()
              end
              text = text or ""
              -- Pad to the slot width (the neo-tree window width) like the native
              -- implementation, so the tabline expands in sync with the tree.
              -- Measure the evaluated string with strwidth: eval_statusline's
              -- .width miscounts ambiguous-width glyphs (e.g. the selector's
              -- "▕" separators), and %{...} literals would inflate strwidth.
              local ok, evaluated = pcall(vim.api.nvim_eval_statusline, text, { use_tabline = true })
              local text_size = 0
              if ok and evaluated and evaluated.str then
                text_size = vim.api.nvim_strwidth((evaluated.str:gsub("%%#%w+#", ""):gsub("%%%*", "")))
              end
              if text_size < size then
                local pad = size - text_size
                local left, right = math.floor(pad / 2), math.ceil(pad / 2)
                text = string.rep(" ", left) .. text .. string.rep(" ", right)
              end
              -- Prepend the offset text highlight (resolved from the tree window's
              -- winhighlight) like the native implementation, so padded/empty cells
              -- render with the tree's background instead of the default tabline bg.
              text = (highlight.text or "") .. text
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
      lsp = {
        -- Option A: disable noice hover interception → native vim.lsp.buf.hover() popup
        hover = { enabled = false },
        -- disable noice signature interception → native vim.lsp.buf.signature_help() popup
        signature = { enabled = false },
      },
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
    config = function(_, opts)
      require("snacks").setup(opts)

      -- LazyVim loads snacks.statuscolumn for its statuscolumn line,
      -- which creates a 50ms cache-clearing timer (20Hz). Since we
      -- don't need that timer (LazyVim manages its own statuscolumn),
      -- patch setup to a no-op so the timer is never created.
      -- pcall(function()
      --   require("snacks.statuscolumn").setup = function() end
      -- end)

      local convert = require("snacks.image.convert")
      local _convert = convert.convert
      ---@diagnostic disable-next-line: duplicate-set-field
      function convert.convert(copts)
        local src = copts.src
        local ext = src and src:match("%.(%w+)$")
        local diag_exts = { mmd = "mermaid", dot = "DOT", puml = "PlantUML", gv = "DOT" }
        local label = diag_exts[ext or ""]
        if label then
          local cache = Snacks.image.config.cache
          local base = vim.fn.fnamemodify(src, ":t:r")
          local prefix = vim.fn.sha256(src .. "0"):sub(1, 8) .. "-" .. base:gsub("[^%w%.]+", "-")
          local expected = cache .. "/" .. prefix .. "." .. vim.o.background .. ".png"
          local uncached = vim.fn.filereadable(expected) == 0
          if uncached then
            vim.notify("Rendering " .. label .. " diagram …", vim.log.levels.INFO)
          end
          local orig_on_done = copts.on_done
          copts.on_done = function(c)
            vim.schedule(function()
              if c:error() then
                vim.notify("Rendering failed: " .. src, vim.log.levels.WARN)
              elseif uncached then
                vim.notify("Rendered " .. label .. " diagram", vim.log.levels.INFO)
              end
            end)
            if orig_on_done then
              orig_on_done(c)
            end
          end
        end
        return _convert(copts)
      end
    end,
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
