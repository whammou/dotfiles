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
        opts = {},
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
      org_split_mode = { "auto" },
      org_hide_leading_stars = false,
      org_adapt_indentaion = false,
      org_startup_indented = true,
      org_use_tag_inheritance = true,
      org_tags_column = 0,
      org_todo_keywords = { "TODO(t)", "PENDING(p)", "DOING(d)", "|", "DONE(f)", "ABORTED(a)" },
      mappings = {
        org_return_uses_meta_return = true,
        org = {
          org_cycle = false,
        },
      },
      ui = {
        folds = {
          colored = false,
        },
        ui = {
          use_vim_ui = true,
        },
      },
    },
  },
}
