return {
  {
    "chipsenkbeil/org-roam.nvim",
    lazy = true,
    ft = "org",
    keys = {
      { "<leader>nu", "<Cmd>RoamUpdate<CR>", desc = "Update Roam database" },
      { "<leader>nU", "<Cmd>RoamUpdate!<CR>", desc = "Force update Roam database" },
    },
    dependencies = {
      {
        "nvim-orgmode/orgmode",
        lazy = true,
        keys = {
          { "<leader>oR", "<cmd>Lazy reload orgmode<CR>", desc = "Org reload" },
        },
        opts = {
          org_agenda_files = { "~/Journal/**/*.org" },
          --org_agenda_skip_scheduled_if_done = true,
          org_default_Journal_file = "~/Journal/capture.org",
          org_archive_location = "log/archive_%s",
          org_log_into_drawer = "LOGBOOK",
          org_highlight_latex_and_related = "entities",

          org_return_uses_meta_return = false,
          mappings = {
            global = {
              org_capture = "<leader>oC",
            },
            org = {
              org_cycle = false,
              org_toggle_checkbox = "<Leader>oc",
            },
          },

          org_ellipsis = "",

          org_hide_leading_stars = false,
          org_hide_emphasis_markers = true,
          org_adapt_indentation = false,
          org_startup_indented = false,
          org_startup_folded = "inherit",

          org_id_link_to_org_use_id = true,
          org_use_tag_inheritance = true,
          org_tags_exclude_from_inheritance = { "META" },
          org_tags_column = 0,
          org_cycle_separator_lines = 0,
          org_blank_before_new_entry = { heading = false, plain_list_item = false },

          org_priority_highest = "A",
          org_priority_default = "B",
          org_priority_lowest = "F",
          org_deadline_warning_days = 0,

          org_todo_repeat_to_state = "RECR",
          org_todo_keywords = {
            "TODO(t)",
            "DOIN(d)",
            "(e)",
            "PEND(p)",
            "OUTL(o)",
            "WAIT(w)",
            "EXPL(x)",
            "FDBK(b)",
            "NEXT(n)",
            "TARGET(g)",
            "IDEA(i)",
            "RECR(l)",
            "|",
            "PRTL(r)",
            "DONE(f)",
            "RVIW(v)",
            "ABRT(a)",
          },
          org_todo_keyword_faces = {
            TODO = ":foreground #c75ae8 :weight bold :slant italic",
            RECR = ":foreground #c75ae8 :weight bold :slant italic",
            DOIN = ":foreground #34bfd0 :weight bold :slant italic",
            PEND = ":foreground #93a4c3 :weight bold :slant italic",
            OUTL = ":foreground #93a4c3 :weight bold :slant italic",
            IDEA = ":foreground #93a4c3 :weight bold :slant italic",
            WAIT = ":foreground #dd9046 :weight bold :slant italic",
            EXPL = ":foreground #dd9046 :weight bold :slant italic",
            FDBK = ":foreground #dd9046 :weight bold :slant italic",
            NEXT = ":foreground #54b0fd :weight bold :slant italic",
            TARGET = ":foreground #c75ae8 :weight bold :slant italic",
            RVIW = ":foreground #efbd5d :weight bold :slant italic",
            PRTL = ":foreground #efbd5d :weight bold :slant italic",
            ABRT = ":foreground #f65866 :weight bold :slant italic",
            DONE = ":foreground #8bcd5b :weight bold :slant italic",
          },

          input = {
            use_vim_ui = true,
          },
          folds = {
            colored = true,
          },
          agenda = {
            preview_window = {
              border = "single",
            },
          },
          ui = {
            agenda = {
              preview_window = {
                wrap = true,
                border = "single",
              },
            },
          },
        },
      },
      {
        "BartSte/nvim-khalorg",
        lazy = true,
        opts = {
          calendar = "private",
        },
      },
      {
        "hamidi-dev/org-super-agenda.nvim",
        lazy = true,
        opts = {
          org_directories = { "/home/whammou/Journal/" },
          show_filename = false,
          keep_order = true,
          window = {
            width = 0.8,
            height = 0.8,
            border = "none",
          },
          todo_states = {
            { name = "TODO", keymap = "ot", color = "#c75ae8" },
            { name = "DOIN", keymap = "od", color = "#34bfd0" },
            { name = "PEND", keymap = "op", color = "#93a4c3" },
            { name = "OUTL", keymap = "oo", color = "#93a4c3" },
            { name = "IDEA", keymap = "oi", color = "#93a4c3" },
            { name = "WAIT", keymap = "ow", color = "#dd9046" },
            { name = "EXPL", keymap = "os", color = "#dd9046" },
            { name = "FDBK", keymap = "ob", color = "#dd9046" },
            { name = "NEXT", keymap = "on", color = "#54b0fd" },
            { name = "RVIW", keymap = "ov", color = "#efbd5d" },
            { name = "PRTL", keymap = "or", color = "#efbd5d" },
            { name = "ABRT", keymap = "oa", color = "#f65866", strike_through = true },
            { name = "DONE", keymap = "of", color = "#8bcd5b" },
          },
          keymaps = {
            toggle_other = "oO",
            cycle_view = "oV",
            filter = "oF",
            filter_fuzzy = "oZ",
            filter_query = "oQ",
            filter_reset = "oA",
          },
          upcoming_days = 7,
          group_format = "* /%s/",
          groups = {
            {
              name = " Oneoff",
              matcher = function(i)
                return i:has_tag("oneoff") and (i.deadline and i.deadline:is_today())
                  or (i.scheduled and i.scheduled:is_today())
              end,
            },
            {
              name = " Recurring",
              matcher = function(i)
                return i:has_tag("recurring") and (i.deadline and i.deadline:is_today())
                  or (i.scheduled and i.scheduled:is_today())
              end,
            },
            {
              name = " Incidental",
              matcher = function(i)
                return i:has_tag("incidental") and (i.deadline and i.deadline:is_today())
                  or (i.scheduled and i.scheduled:is_today())
              end,
            },
            {
              name = " Coordinated",
              matcher = function(i)
                return i:has_tag("coordinated") and (i.deadline and i.deadline:is_today())
                  or (i.scheduled and i.scheduled:is_today())
              end,
            },
            {
              name = " Planned",
              matcher = function(i)
                return i:has_tag("planned") and (i.deadline and i.deadline:is_today())
                  or (i.scheduled and i.scheduled:is_today())
              end,
            },
            {
              name = "󱔗 Documents",
              matcher = function(i)
                return i:has_tag("doc") and (i.deadline and i.deadline:is_today())
                  or (i.scheduled and i.scheduled:is_today())
              end,
            },
          },
        },
      },
      {
        "nvim-orgmode/org-bullets.nvim",
        lazy = true,
        opts = {
          concealcursor = true,
          symbols = {
            list = "»",
          },
        },
      },
      {
        "lukas-reineke/headlines.nvim",
        lazy = true,
        config = function()
          require("config.extras.headlines")
        end,
      },
      {
        "0xzhzh/fzf-org.nvim",
        lazy = true,
        keys = {
          -- example keybindings
          {
            "<leader>ozg",
            function()
              require("fzf-org").orgmode()
            end,
            desc = "org-browse",
          },
          {
            "<leader>ozf",
            function()
              require("fzf-org").files()
            end,
            desc = "org-files",
          },
          {
            "<leader>ozr",
            function()
              require("fzf-org").refile_to_file()
            end,
            desc = "org-refile",
          },
        },
        opts = {},
      },
      {
        "danilshvalov/org-modern.nvim",
        lazy = true,
      },

      --{
      --  "mrshmllow/orgmode-babel.nvim",
      --  cmd = { "OrgExecute", "OrgTangle" },
      --  opts = {
      --    -- by default, none are enabled
      --    langs = { "python", "lua", ... },

      --    -- paths to emacs packages to additionally load
      --    load_paths = {},
      --  },
      --},
    },
    config = function()
      require("config.extras.org")
    end,
  },
}
