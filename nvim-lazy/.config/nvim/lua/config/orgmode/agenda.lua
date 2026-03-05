local templates = require("config.orgmode.templates")
local capture_templates = templates.capture

local tracker_agenda = {
  {
    type = "agenda",
    org_agenda_tag_filter_preset = "TASK-RECURRING",
    org_agenda_span = "day",
  },
  {
    type = "tags",
    match = "TRACKER+META",
  },
}

local task_agenda = {
  {
    type = "agenda",
    org_agenda_tag_filter_preset = "TASK-RECURRING",
    org_agenda_span = "day",
  },
  {
    type = "tags_todo",
    match = '+PRIORITY="A"',
    org_agenda_overriding_header = "Global list of High Priority tasks",
  },
  {
    type = "tags",
    match = "TASK/DOIN",
    org_agenda_overriding_header = "Global list of DOIN tasks",
  },
  {
    type = "tags",
    match = "TASK/NEXT",
    org_agenda_overriding_header = "Global list of NEXT tasks",
  },
  {
    type = "tags",
    match = "TASK/WAIT",
    org_agenda_overriding_header = "Global list of WAIT tasks",
  },
}

local task_doc_agenda = {
  {
    type = "agenda",
    org_agenda_tag_filter_preset = "TASK-RECURRING",
    org_agenda_overriding_header = " 󰄵 Task Agenda ",
    org_agenda_span = "day",
  },
  {
    type = "agenda",
    org_agenda_tag_filter_preset = "DOC",
    org_agenda_overriding_header = "  Document Agenda ",
    org_agenda_span = "day",
  },
  {
    type = "agenda",
    org_agenda_tag_filter_preset = "RECURRING",
    org_agenda_overriding_header = "  Recurring Tasks ",
    org_agenda_span = "day",
  },
}
local backlog = {
  {
    type = "tags",
    match = "/PEND|OUTL",
    org_agenda_overriding_header = "Document Tasks",
    org_agenda_span = "week",
  },
}

local function setup_org_capture_template()
  require("orgmode").setup({
    org_capture_templates = capture_templates,
    org_agenda_custom_commands = {
      K = {
        description = "Tracker Agenda",
        types = tracker_agenda,
      },
      k = {
        description = "Task Agenda",
        types = task_agenda,
      },
      c = {
        description = "Combined View",
        types = task_doc_agenda,
      },
      L = {
        description = "Backlog",
        types = backlog,
      },
    },
  })
end
setup_org_capture_template()

vim.api.nvim_create_user_command("ReloadOrgConfig", setup_org_capture_template, {
  desc = "Reloads Orgmode capture templates and related configuration",
})
