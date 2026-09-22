-- Neo-tree source selector highlights defined in colorscheme.lua (onedark opts.highlights)
-- to avoid being wiped by onedark's `hi clear` during colorscheme application.

return {
  -- Disable LazyVim's default <leader>e explorer remap (neo-tree / snacks_explorer extra)
  { "nvim-neo-tree/neo-tree.nvim", keys = { { "<leader>e", false }, { "<leader>E", false } } },
  { "folke/snacks.nvim", keys = { { "<leader>e", false }, { "<leader>E", false } } },

  {
    "m00qek/baleia.nvim",
    lazy = true,
    config = function()
      require("baleia").setup({ strip_ansi_codes = true })
      vim.api.nvim_create_autocmd("FileType", {
        pattern = "kitty-scrollback",
        callback = function()
          require("baleia").once(vim.api.nvim_get_current_buf())
        end,
      })
    end,
  },
  {
    "lukas-reineke/headlines.nvim",
    lazy = true,
    ft = { "markdown", "org" },
    dependencies = {
      "nvim-orgmode/orgmode",
    },
    config = function()
      require("config.editor")
    end,
  },
  {
    "nvim-neo-tree/neo-tree.nvim",
    lazy = true,
    init = function()
      if vim.fn.argc() == 1 then
        local stat = (vim.uv or vim.loop).fs_stat(vim.fn.argv(0))
        if stat and stat.type == "directory" then
          require("lazy").load({ plugins = { "neo-tree.nvim" } })
        end
      end
    end,
    dependencies = {
      "whammou/netman.nvim",
      lazy = true,
      opts = {},
    },
    keys = {
      {
        "<leader>ef",
        function()
          local dir = vim.fn.expand("%:p:h")
          if dir == "" or vim.fn.isdirectory(dir) == 0 then
            dir = vim.fn.getcwd()
          end
          require("neo-tree.command").execute({
            action = "show",
            dir = dir,
            reveal = true,
            reveal_force_cwd = true,
          })
        end,
        desc = "Show file explorer (buffer dir)",
      },
      {
        "<leader>ep",
        function()
          local function git_root()
            local path = vim.fn.expand("%:p:h")
            if path == "" or vim.fn.isdirectory(path) == 0 then
              path = vim.fn.getcwd()
            end
            local found = vim.fs.find(".git", { upward = true, path = path })
            if found and #found > 0 then
              return vim.fn.fnamemodify(found[1], ":h")
            end
            local out = vim.fn.system({ "git", "-C", path, "rev-parse", "--show-toplevel" })
            if vim.v.shell_error == 0 then
              return vim.trim(out)
            end
            return nil
          end
          local dir = git_root()
          if dir then
            require("neo-tree.command").execute({
              action = "show",
              dir = dir,
              reveal = true,
              reveal_force_cwd = true,
            })
          else
            require("neo-tree.command").execute({ action = "show", dir = vim.fn.expand("~") })
          end
        end,
        desc = "Show file explorer (git root or HOME)",
      },
      {
        "<leader>er",
        function()
          require("neo-tree.command").execute({ action = "show", source = "remote" })
        end,
        desc = "Show remote home via netrw",
      },
      {
        "<leader>ex",
        function()
          require("neo-tree.command").execute({ action = "close" })
        end,
        desc = "Hide file explorer",
      },
      { "<leader>e", false },
      { "<leader>E", false },
    },
    opts = {
      filesystem = {
        hijack_netrw_behavior = "open_default",
        use_libuv_file_watcher = true,
      },
      sources = {
        "filesystem",
        "git_status",
        "netman.ui.neo-tree",
      },
      source_selector = {
        winbar = false,
        -- "equal" gives every provider an identical slot width at any window
        -- width (each slot = (width - separators) / #providers). Names must
        -- fit the smallest slot: at 25 cells that is 7 cells, so display
        -- names drop the leading space and icons ("Files"=5, "Git"=3,
        -- "Remote"=6 cells) to avoid truncation with "…".
        -- "start" is NOT used: it appends all leftover width to the LAST tab,
        -- so expanding the window makes the last provider ("Remote") look
        -- like it has larger spacing than the rest.
        tabs_layout = "equal",
        content_layout = "center",
        sources = {
          { source = "filesystem", display_name = " Files" },
          { source = "git_status", display_name = " Git" },
          { source = "remote", display_name = "󰒍 Remote" },
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
        width = 25,
      },
      default_component_configs = {
        git_status = {
          symbols = {
            added = "",
            modified = "󰝤",
            deleted = "",
            renamed = "󰏬",
            untracked = "󰐖",
            ignored = "󰿠",
            unstaged = "󰍵",
            staged = "",
            conflict = "󰅗",
          },
        },
      },
      event_handlers = {
        {
          event = "neo_tree_buffer_enter",
          handler = function()
            -- This effectively hides the cursor
            vim.cmd("highlight! CursorBlock blend=100")
            -- Prevent neo-tree window from being resized by other splits
            vim.wo.winfixwidth = true
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
                _G.__cached_neo_tree_selector_width = width
                _G.__cached_neo_tree_state = state
                vim.schedule(function()
                  vim.cmd("redrawtabline")
                end)
              end
            end
          end,
        },
        -- Clear cached selector when the tree window closes, so the tabline
        -- toggles away along with the neo-tree buffer (after_render never
        -- fires on close, so without this the stale selector stays rendered)
        {
          event = "neo_tree_window_after_close",
          handler = function()
            _G.__cached_neo_tree_selector = nil
            _G.__cached_neo_tree_selector_width = nil
            _G.__cached_neo_tree_state = nil
            vim.schedule(function()
              vim.cmd("redrawtabline")
            end)
          end,
        },
        -- Clean up the hijack's listed empty [No Name] buffer when nvim is
        -- launched with a directory (e.g. `nvim ~/.config/qtile`). netrw hijack
        -- creates a listed empty buffer to replace the directory buffer; after
        -- opening a file via neo-tree that empty buffer stays listed as No Name.
        {
          event = "file_opened",
          handler = function(file_path)
            for _, buf in ipairs(vim.api.nvim_list_bufs()) do
              if vim.api.nvim_buf_is_valid(buf) and vim.api.nvim_buf_get_name(buf) == "" and vim.bo[buf].buftype == "" then
                if vim.api.nvim_buf_line_count(buf) == 1 and vim.api.nvim_buf_get_lines(buf, 0, 1, false)[1] == "" then
                  if #vim.api.nvim_list_wins() > 1 then
                    pcall(vim.api.nvim_buf_delete, buf, { force = true })
                  end
                end
              end
            end
          end,
        },
      },
    },
    config = function(_, opts)
      require("neo-tree").setup(opts)
      -- Collapsing the auto-expanded width (`e` inside the tree buffer runs
      -- toggle_auto_expand_width, which resizes the window and calls
      -- renderer.redraw -> render_tree) never fires after_render, so the
      -- cached selector stays at the widened width. WinResized covers both
      -- the expand and collapse directions.
      vim.api.nvim_create_autocmd("WinResized", {
        group = vim.api.nvim_create_augroup("NeoTreeSelectorResize", { clear = true }),
        callback = function()
          local state = _G.__cached_neo_tree_state
          if not state or not state.winid or not vim.api.nvim_win_is_valid(state.winid) then
            return
          end
          local width = vim.api.nvim_win_get_width(state.winid)
          if width == _G.__cached_neo_tree_selector_width then
            return
          end
          local selector = require("neo-tree.ui.selector")
          local ok, str = pcall(selector.get_selector, state, width)
          if ok and str then
            _G.__cached_neo_tree_selector = str
            _G.__cached_neo_tree_selector_width = width
            vim.schedule(function()
              vim.cmd("redrawtabline")
            end)
          end
        end,
      })
    end,
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
      {
        "<leader>fw",
        function()
          require("custom.webdav-fzf").browse()
        end,
        desc = "Browse WebDAV files",
      },
    },
    cmd = { "WebdavFzf" },
    dependencies = { "nvim-tree/nvim-web-devicons" },
    opts = {
      actions = {
        files = {
          ["enter"] = function(selected, opts)
            if #selected > 1 then
              return require("fzf-lua.actions").file_edit_or_qf(selected, opts)
            end
            local entry = require("fzf-lua.path").entry_to_file(selected[1], opts)
            local path = entry.path or entry.bufname or entry.uri
            if path then
              if not require("fzf-lua.path").is_absolute(path) then
                path = require("fzf-lua.path").join({ opts.cwd or opts._cwd or vim.fn.getcwd(), path })
              end
              local stat = (vim.uv or vim.loop).fs_stat(path)
              if (stat and stat.type == "directory") or vim.fn.isdirectory(path) == 1 then
                require("neo-tree.command").execute({ action = "show", dir = path })
                return
              end
            end
            require("fzf-lua.actions").file_edit_or_qf(selected, opts)
          end,
        },
      },
      winopts = {
        split = "belowright new",
        border = "single",
      },
      git_icons = {
        ["M"] = { icon = "", color = "yellow" },
        ["D"] = { icon = "", color = "red" },
        ["A"] = { icon = "", color = "green" },
        ["R"] = { icon = "", color = "yellow" },
        ["C"] = { icon = "", color = "yellow" },
        ["T"] = { icon = "", color = "magenta" },
        ["?"] = { icon = "", color = "magenta" },
      },
    },
  },
  {
    "chrisgrieser/nvim-origami",
    event = "VeryLazy",
    opts = {
      useLspFoldsWithTreesitterFallback = {
        enabled = false, -- prevents overriding orgmode's foldmethod/foldexpr when LSP attaches to ANY buffer (e.g. otter hidden buffer)
      },
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
