return {
  {
    "nvim-neo-tree/neo-tree.nvim",
    keys = {
      {
        "<leader>ef",
        "<cmd>Neotree show toggle<CR>",
        desc = "Toggle file explorer (no focus)",
      },
      {
        "<leader>eh",
        "<cmd>Neotree show dir=~<cr>",
        desc = "Neotree go HOME",
      },
      {
        "<leader>es",
        "<cmd>edit scp://homelab//home/homelab/<cr>",
        desc = "Open remote home via netrw",
      },
    },
    opts = {
      window = {
        width = "30%",
      },
      default_component_configs = {
        git_status = {
          symbols = {
            -- Change type
            added = "✚", -- or "✚"
            modified = "", -- or ""
            deleted = "✖", -- this can only be used in the git_status source
            renamed = "󰁕", -- this can only be used in the git_status source
            -- Status type
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
            vim.cmd("highlight! Cursor blend=100")
          end,
        },
        {
          event = "neo_tree_buffer_leave",
          handler = function()
            -- Make this whatever your current Cursor highlight group is.
            vim.cmd("highlight! Cursor guibg=#5f87af blend=0")
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
    -- optional for icon support
    dependencies = { "nvim-tree/nvim-web-devicons" },
    -- or if using mini.icons/mini.nvim
    -- dependencies = { "nvim-mini/mini.icons" },
    opts = {
      winopts = {
        split = "belowright new",
        border = "single",
      },
    },
  },
  -- lazy.nvim
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
    }, -- needed even when using default config

    -- recommended: disable vim's auto-folding
    -- init = function()
    --   vim.opt.foldlevel = 99
    --   vim.opt.foldlevelstart = 99
    -- end,
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
    -- lazy = true,
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
      -- Customize Configuration
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
    -- init.lua - set defaults for all buffers (overridden by ftplugins)
    option = function()
      require("table_vim").setup({
        style = "default",
        options = { multiline = "auto", multiline_format = "block_wrap" },
      })
    end,
  },
}
