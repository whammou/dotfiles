-- Neo-tree source selector highlight groups matching bufferline `#21252b` fill
vim.api.nvim_set_hl(0, "NeoTreeTabBarBg", { bg = "#21252b" })
vim.api.nvim_set_hl(0, "NeoTreeTabBarInactive", { bg = "#1c2028", fg = "#5c6370" })
vim.api.nvim_set_hl(0, "NeoTreeTabBarActive", { bg = "#2b303b", fg = "#e5e7eb", bold = true })
vim.api.nvim_set_hl(0, "NeoTreeTabBarSepInactive", { bg = "#21252b", fg = "#3b4048" })
vim.api.nvim_set_hl(0, "NeoTreeTabBarSepActive", { bg = "#2b303b", fg = "#3b4048" })

return {
  {
    "nvim-neo-tree/neo-tree.nvim",
    lazy = true,
    dependencies = {
      "whammou/netman.nvim",
      lazy = true,
      opts = {},
    },
    keys = {
      {
        "<leader>ef",
        "<cmd>Neotree show toggle<CR>",
        desc = "Toggle file explorer (cwd)",
      },
      {
        "<leader>eh",
        "<cmd>Neotree show toggle dir=~<cr>",
        desc = "Neotree go HOME",
      },
      {
        "<leader>es",
        "<cmd>Neotree show toggle remote<cr>",
        desc = "Open remote home via netrw",
      },
    },
    opts = {
      sources = {
        "filesystem",
        "git_status",
        "netman.ui.neo-tree",
      },
      source_selector = {
        winbar = false,
        sources = {
          { source = "filesystem", display_name = "  Files" },
          { source = "git_status", display_name = "  Git" },
          { source = "remote", display_name = " 󰒍 Remote" },
        },
        highlight_tab = "NeoTreeTabBarInactive",
        highlight_tab_active = "NeoTreeTabBarActive",
        highlight_background = "NeoTreeTabBarBg",
        highlight_separator = "NeoTreeTabBarSepInactive",
        highlight_separator_active = "NeoTreeTabBarSepActive",
        separator = { left = "▏", right = "▕" },
        show_separator_on_edge = false,
      },
      window = {
        width = "25",
      },
      default_component_configs = {
        git_status = {
          symbols = {
            added = "✚",
            modified = "",
            deleted = "✖",
            renamed = "󰁕",
            untracked = "",
            ignored = "",
            unstaged = "󰄱",
            staged = "",
            conflict = "",
          },
        },
      },
      event_handlers = {
        {
          event = "neo_tree_buffer_enter",
          handler = function()
            -- This effectively hides the cursor
            vim.cmd("highlight! CursorBlock blend=100")
          end,
        },
        {
          event = "neo_tree_buffer_leave",
          handler = function()
            -- Make this whatever your current Cursor highlight group is.
            vim.cmd("highlight! CursorBlock guibg=#5f87af blend=0")
          end,
        },
        -- Cache neo-tree source selector for bufferline tabline integration
        {
          event = "after_render",
          handler = function(state)
            if state.current_position == "left" or state.current_position == "right" then
              local selector = require("neo-tree.ui.selector")
              local width = vim.api.nvim_win_get_width(state.winid)
              local str = selector.get_selector(state, width)
              if str then
                _G.__cached_neo_tree_selector = str
                vim.cmd("redrawtabline")
              end
            end
          end,
        },
      },
    },
  },
  {
    "folke/which-key.nvim",
    opts = {
      preset = "classic",
      win = {
        border = "single",
      },
      icons = {
        separator = "",
      },
    },
  },
  {
    "ibhagwan/fzf-lua",
    keys = {
      {
        "<leader>fh",
        function()
          require("fzf-lua").files({ cwd = "~/" })
        end,
        desc = "Find HOME files",
      },
      {
        "<leader>fC",
        function()
          require("fzf-lua").files({ cwd = "~/.config" })
        end,
        desc = "Find system config files",
      },
      {
        "<leader>fu",
        function()
          require("fzf-lua").files({ cwd = "~/.local/bin" })
        end,
        desc = "Find bin files",
      },
    },
    dependencies = { "nvim-tree/nvim-web-devicons" },
    opts = {
      winopts = {
        split = "belowright new",
        border = "single",
      },
    },
  },
  {
    "chrisgrieser/nvim-origami",
    event = "VeryLazy",
    opts = {
      foldtext = {
        lineCount = {
          template = "%d",
          hlgroup = "Comment",
        },
      },
    },
  },
  {
    "norcalli/nvim-colorizer.lua",
    lazy = true,
    keys = {
      { "<leader>Ct", "<cmd>ColorizerToggle<CR>", desc = "Toggle color code" },
    },
    event = "VeryLazy",
    opts = {},
  },
  {
    "pysan3/fcitx5.nvim",
    event = "VeryLazy",
    opts = {},
  },
  {
    "tpope/vim-eunuch",
    lazy = true,
    event = "VeryLazy",
  },
  {
    "soemre/commentless.nvim",
    lazy = true,
    cmd = "Commentless",
    keys = {
      {
        "z[",
        function()
          require("commentless").hide()
        end,
        desc = "Hide Comments",
      },
      {
        "z]",
        function()
          require("commentless").reveal()
        end,
        desc = "Reveal Comments",
      },
    },
    opts = {
      hide_following_blank_lines = true,
      foldtext = function(folded_count)
        return ""
      end,
    },
  },
  {
    "numEricL/table.vim",
    lazy = true,
    event = "VeryLazy",
    option = function()
      require("table_vim").setup({
        style = "default",
        options = { multiline = "auto", multiline_format = "block_wrap" },
      })
    end,
  },
}
