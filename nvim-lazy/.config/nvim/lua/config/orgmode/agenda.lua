local templates = require("config.orgmode.templates")
local capture_templates = templates.capture

local tracker_agenda = {
  {
    type = "agenda",
    org_agenda_tag_filter_preset = "typTask-catRecurring",
    org_agenda_span = "day",
  },
  {
    type = "tags",
    match = "typDev-meta/OPEN",
  },
}

local task_agenda = {
  {
    type = "agenda",
    org_agenda_tag_filter_preset = "typTask-catRecurring",
    org_agenda_span = "day",
  },
  {
    type = "tags",
    match = "typTask/PROG",
    org_agenda_overriding_header = "Global list of PROG tasks",
  },
  {
    type = "tags",
    match = "typTask/DOIN",
    org_agenda_overriding_header = "Global list of DOIN tasks",
  },
  {
    type = "tags",
    match = "typTask/NEXT",
    org_agenda_overriding_header = "Global list of NEXT tasks",
  },
  {
    type = "tags",
    match = "typTask/WAIT",
    org_agenda_overriding_header = "Global list of WAIT tasks",
  },
  {
    type = "tags_todo",
    match = 'typTask+PRIORITY>="C"',
    org_agenda_overriding_header = "Global list of High Priority tasks",
  },
  {
    type = "tags",
    match = "typTask/TODO",
    org_agenda_overriding_header = "Global list of TODO tasks",
  },
  {
    type = "tags",
    match = "typTask/PEND",
    org_agenda_overriding_header = "Global list of PEND tasks",
  },
}

local task_doc_agenda = {
  {
    type = "agenda",
    org_agenda_tag_filter_preset = "typTask-catRecurring",
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
    org_agenda_tag_filter_preset = "catRecurring",
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

local extended_agenda_commands = {
  K = { description = "Tracker Agenda", types = tracker_agenda },
  k = { description = "Task Agenda", types = task_agenda },
  c = { description = "Combined View", types = task_doc_agenda },
  L = { description = "Backlog", types = backlog },
  h = {
    description = "HOME+Name tags searches",
    submenu = {
      l = { description = "Lisa  — home+Lisa", types = { { type = "tags", match = "+home+Lisa", org_agenda_overriding_header = "HOME Lisa" } } },
      p = { description = "Peter — home+Peter", types = { { type = "tags", match = "+home+Peter", org_agenda_overriding_header = "HOME Peter" } } },
      k = { description = "Kim   — home+Kim", types = { { type = "tags", match = "+home+Kim", org_agenda_overriding_header = "HOME Kim" } } },
    },
  },
  Q = {
    description = "Queries (subpage)",
    submenu = {
      a = { description = "Project A — project-A", types = { { type = "tags", match = "project-A", org_agenda_overriding_header = "Project A" } } },
      b = { description = "Project B — project-B", types = { { type = "tags", match = "project-B", org_agenda_overriding_header = "Project B" } } },
      c = {
        description = "Combined HQ (agenda + tags)",
        types = {
          { type = "agenda", org_agenda_span = "day" },
          { type = "tags", match = "project-A", org_agenda_overriding_header = "Project A Tasks" },
        },
      },
    },
  },
  T = {
    description = "Entry points",
    submenu = {
      k = { description = "Task Agenda  (task_agenda)", types = task_agenda },
      K = { description = "Tracker Agenda", types = tracker_agenda },
      c = { description = "Combined View (task_doc_agenda)", types = task_doc_agenda },
      L = { description = "Backlog", types = backlog },
      n = {
        description = "Nested demo ▶",
        submenu = {
          a = { description = "Nested A", types = { { type = "tags", match = "project-A" } } },
          b = { description = "Nested B", types = { { type = "tags", match = "project-B" } } },
        },
      },
    },
  },
}

require("orgmode.extensions.extended_agenda").setup(extended_agenda_commands, capture_templates)
