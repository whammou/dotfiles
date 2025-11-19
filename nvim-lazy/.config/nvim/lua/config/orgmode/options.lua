local dir = require("config.orgmode.directories")

local base_dir = dir.base_dir

require("orgmode").setup({
  org_agenda_files = { base_dir .. "**/*.org" },
  org_default_notes_file = base_dir .. "capture.org",
  org_log_into_drawer = "LOGBOOK",
  org_highlight_latex_and_related = "entities",

  org_archive_location = "./log/archive_%s",
  org_agenda_text_search_extra_files = { "agenda-archives" },

  org_return_uses_meta_return = false,
  mappings = {
    global = {
      org_capture = "<leader>oc",
    },
    org = {
      org_cycle = false,
      org_toggle_checkbox = "<Leader>oC",
    },
  },

  org_ellipsis = "",
  org_hide_leading_stars = false,
  org_hide_emphasis_markers = true,
  org_adapt_indentation = false,
  org_startup_indented = false,
  org_startup_folded = "inherit",
  win_split_mode = "auto",

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
})
