return {
  {
    "chipsenkbeil/org-roam.nvim",
    lazy = true,
    ft = "org",
    keys = {
      { "<leader>nu", "<Cmd>RoamUpdate<CR>", desc = "Update Roam database" },
    },
    dependencies = {
      {
        "nvim-orgmode/orgmode",
        lazy = true,
        opts = {
          org_agenda_files = { "~/notes/**/*.org" },
          --org_agenda_skip_scheduled_if_done = true,
          org_default_notes_file = "~/notes/capture.org",
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
          win_split_mode = "auto",

          org_hide_leading_stars = false,
          org_hide_emphasis_markers = true,
          org_adapt_indentation = false,
          org_startup_indented = false,

          org_id_link_to_org_use_id = true,
          org_use_tag_inheritance = true,
          org_tags_exclude_from_inheritance = { "PROJECT" },
          org_tags_column = 0,
          org_cycle_separator_lines = 0,
          org_blank_before_new_entry = { heading = false, plain_list_item = false },

          org_priority_highest = "A",
          org_priority_default = "B",
          org_priority_lowest = "F",
          org_deadline_warning_days = 0,

          org_todo_keywords = {
            "TODO(t)",
            "DOING(d)",
            "(e)",
            "PENDING(p)",
            "OUTLINE(o)",
            "WAITING(w)",
            "RESEARCH(s)",
            "FEEDBACK(b)",
            "NEXT(n)",
            "|",
            "IDEA(i)",
            "PARTIAL(r)",
            "DONE(f)",
            "REVIEW(v)",
            "ABORTED(a)",
          },
          org_todo_keyword_faces = {
            TODO = ":foreground #c75ae8 :weight bold :slant italic",
            DOING = ":foreground #34bfd0 :weight bold :slant italic",
            PENDING = ":foreground #93a4c3 :weight bold :slant italic",
            OUTLINE = ":foreground #93a4c3 :weight bold :slant italic",
            IDEA = ":foreground #93a4c3 :weight bold :slant italic",
            WAITING = ":foreground #dd9046 :weight bold :slant italic",
            RESEARCH = ":foreground #dd9046 :weight bold :slant italic",
            FEEDBACK = ":foreground #dd9046 :weight bold :slant italic",
            NEXT = ":foreground #54b0fd :weight bold :slant italic",
            REVIEW = ":foreground #efbd5d :weight bold :slant italic",
            PARTIAL = ":foreground #efbd5d :weight bold :slant italic",
            ABORTED = ":foreground #f65866 :weight bold :slant italic",
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
          org_directories = { "/home/whammou/notes/" },
          show_filename = false,
          window = {
            border = "single",
          },
          todo_states = {
            { name = "TODO", color = "#c75ae8" },
            { name = "DOING", color = "#34bfd0" },
            { name = "PENDING", color = "#93a4c3" },
            { name = "OUTLINE", color = "#93a4c3" },
            { name = "IDEA", color = "#93a4c3" },
            { name = "WAITING", color = "#dd9046" },
            { name = "RESEARCH", color = "#dd9046" },
            { name = "FEEDBACK", color = "#dd9046" },
            { name = "NEXT", color = "#54b0fd" },
            { name = "REVIEW", color = "#efbd5d" },
            { name = "PARTIAL", color = "#efbd5d" },
            { name = "ABORTED", color = "#f65866", strike_through = true },
            { name = "DONE", color = "#8bcd5b", strike_through = true },
          },
          groups = {
            {
              name = " Today",
              matcher = function(i)
                return i.scheduled and i.scheduled:is_today()
              end,
              sort = { by = "priority", order = "desc" },
            },
            {
              name = " Tomorrow",
              matcher = function(i)
                return i.scheduled and i.scheduled:days_from_today() == 1
              end,
            },
            {
              name = "󱓇 Deadlines",
              matcher = function(i)
                return i.deadline
                  and i.todo_state ~= "ABORTED"
                  and i.todo_state ~= "DONE"
                  and i.todo_state ~= "PARTIAL"
                  and i.todo_state ~= "REVIEW"
              end,
              sort = { by = "deadline", order = "asc" },
            },
            {
              name = " Important",
              matcher = function(i)
                return i.priority == "A" and (i.deadline or i.scheduled)
              end,
              sort = { by = "date_nearest", order = "asc" },
            },
            {
              name = "󰔟 Overdue",
              matcher = function(i)
                return i.todo_state ~= "DONE"
                  and i.todo_state ~= "PARTIAL"
                  and i.todo_state ~= "ABORTED"
                  and ((i.deadline and i.deadline:is_past()) or (i.scheduled and i.scheduled:is_past()))
              end,
              sort = { by = "date_nearest", order = "asc" },
            },
            {
              name = " Personal",
              matcher = function(i)
                return i:has_tag("personal")
              end,
            },
            {
              name = "󰃖 Work",
              matcher = function(i)
                return i:has_tag("work")
              end,
            },
            {
              name = "📆 Upcoming",
              matcher = function(i)
                local days = require("org-super-agenda.config").get().upcoming_days or 10
                local d1 = i.deadline and i.deadline:days_from_today()
                local d2 = i.scheduled and i.scheduled:days_from_today()
                return (d1 and d1 >= 0 and d1 <= days) or (d2 and d2 >= 0 and d2 <= days)
              end,
              sort = { by = "date_nearest", order = "asc" },
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
            list = "◆",
          },
        },
      },
      {
        "lukas-reineke/headlines.nvim",
        lazy = true,
        opts = {
          markdown = {
            headline_highlights = false,
            bullets_highlights = false,
            codeblock_highlight = false,
            dash_highlight = false,
            quote_highlight = false,
          },
          org = {
            headline_highlights = { "Headline" },
          },
        },
      },
    },
    config = function()
      require("config.extras.org")
    end,
  },
}
