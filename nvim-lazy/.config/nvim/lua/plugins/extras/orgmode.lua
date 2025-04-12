return {
  {
    "nvim-orgmode/orgmode",
    lazy = true,
    ft = "org",

    dependencies = {
      {
        "lukas-reineke/headlines.nvim",
        lazy = true,
        ft = "org",
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

      {
        "nvim-orgmode/org-bullets.nvim",
        lazy = true,
        ft = "org",
        opts = {},
      },
    },

    opts = {
      org_agenda_files = { "~/notes/**/*" },
      org_default_notes_file = "~/notes/capture.org",
      org_archive_location = "./archive/log.org::ARCHIVED",
      org_log_into_drawer = "LOGBOOK",

      org_ellipsis = "",
      win_split_mode = { "float", 0.9 },

      org_split_mode = { "auto" },
      org_hide_leading_stars = false,
      org_adapt_indentaion = false,
      org_startup_indented = true,

      org_use_tag_inheritance = true,
      org_tags_column = 0,

      org_todo_keywords = { "TODO(t)", "PENDING(p)", "DOING(d)", "|", "DONE(f)", "ABORTED(a)" },
      org_todo_keyword_faces = {
        ABORTED = ":foreground #f65866 :weight bold",
        DOING = ":foreground #34bfd0 :weight bold",
        PENDING = ":foreground #93a4c3 :weight bold",
      },

      org_priority_highest = "A",
      org_priority_default = "B",
      org_priority_lowest = "F",
      org_deadline_warning_days = 0,

      org_capture_templates = {
        d = { description = "Document", template = "* %? [%]" },
      },

      mappings = {
        org_return_uses_meta_return = false,
        org = {
          org_cycle = false,
        },
      },

      ui = {
        input = {
          use_vim_ui = true,
        },
        folds = {
          colored = false,
        },
      },
    },
  },
}
