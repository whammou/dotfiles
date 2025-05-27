local orgmode = require("orgmode")
local khalorg = require("khalorg")

local custom_exports = {
  n = { label = "Add a new khal item", action = khalorg.new },
  d = { label = "Delete a khal item", action = khalorg.delete },
  e = { label = "Edit properties of a khal item", action = khalorg.edit },
  E = { label = "Edit properties & dates of a khal item", action = khalorg.edit_all },
}

local capture_templates = {
  d = { description = "Document", template = "* %? [%]" },
  t = { description = "Task", template = "\n* TODO %?" },
}

local todo_keyword_faces = {
  ABORTED = ":foreground #f65866 :weight bold",
  DOING = ":foreground #34bfd0 :weight bold",
  PENDING = ":foreground #93a4c3 :weight bold",
}

local mappings = {
  org_return_uses_meta_return = false,
  global = {
    org_capture = "<leader>oC",
  },
  org = {
    org_cycle = false,
    org_toggle_checkbox = "<Leader>oc",
  },
}

local ui = {
  input = {
    use_vim_ui = true,
  },
  folds = {
    colored = false,
  },
}

khalorg.setup({
  calendar = "private",
})

orgmode.setup({
  ui = ui,
  mappings = mappings,
  org_custom_exports = custom_exports,
  org_todo_keyword_faces = todo_keyword_faces,
  org_capture_templates = capture_templates,
  org_agenda_files = { "~/notes/**/*" },
  org_default_notes_file = "~/notes/capture.org",
  org_archive_location = "./log.org::ARCHIVED",
  org_log_into_drawer = "LOGBOOK",

  org_ellipsis = "",
  win_split_mode = { "float", 0.9 },
  org_split_mode = { "auto" },

  org_hide_leading_stars = false,
  org_adapt_indentaion = false,
  org_startup_indented = true,
  org_id_link_to_org_use_id = true,
  org_use_tag_inheritance = true,
  org_tags_column = 0,
  org_cycle_separator_lines = 0,
  org_blank_before_new_entry = { heading = false, plain_list_item = false },

  org_todo_keywords = { "TODO(t)", "DOING(d)", "|", "PENDING(p)", "DONE(f)", "ABORTED(a)" },
  org_priority_highest = "A",
  org_priority_default = "B",
  org_priority_lowest = "F",
  org_deadline_warning_days = 0,
})
