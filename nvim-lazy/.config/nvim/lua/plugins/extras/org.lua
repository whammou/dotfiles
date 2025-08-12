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
          org_archive_location = "./log.org::ARCHIVED",
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
          win_split_mode = "horizontal",

          org_hide_leading_stars = false,
          org_hide_emphasis_markers = true,
          org_adapt_indentation = false,
          org_startup_indented = false,

          org_id_link_to_org_use_id = true,
          org_use_tag_inheritance = true,
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
