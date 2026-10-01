local dir = require("config.orgmode.directories")
local base_dir = dir.base_dir
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

-- Two different parsers consume the strings below; keep both in mind when editing.
-- `match` (tags/tags_todo rows) goes through Search (files/elements/search.lua): real `|`
-- OR, `&` AND, `+`/`-` include/exclude per branch, `/TODO` suffix filters the todo keyword
-- GLOBALLY. A trailing `-tag` after `/TODO` would land in the todo-keyword matcher
-- (compares keywords, not tags) and silently do nothing, and one `-tag` at the end of an
-- `A|B` string covers only branch B — so match() distributes the exclusion into every
-- branch BEFORE the `/` suffix.
-- `org_agenda_tag_filter_preset` (agenda row) goes through AgendaFilter (agenda/filter.lua:102):
-- pure AND of `+`/`-` conditions with NO `|` support (`|` is swallowed into a literal tag
-- name that can never match). Appending `-tag` there is still effective (global AND).
-- Canonical tag is topTeaching (format_topic in filetags.lua:210), not topteaching.
-- The exclusion lives in exactly one place: EXCLUDE. Casing matters (has_tag is exact).
local EXCLUDE = "-catOneoff"

local function make_task_agenda(branches, preset)
  branches = branches or { "typTask" }
  local function match(tail)
    local parts = {}
    for _, b in ipairs(branches) do
      table.insert(parts, b .. EXCLUDE)
    end
    return table.concat(parts, "|") .. tail
  end
  return {
    { type = "agenda", org_agenda_tag_filter_preset = preset .. EXCLUDE, org_agenda_span = "day" },
    { type = "tags", match = match("/PROG"), org_agenda_overriding_header = "Global list of PROG tasks" },
    { type = "tags", match = match("/DOIN"), org_agenda_overriding_header = "Global list of DOIN tasks" },
    { type = "tags", match = match("/NEXT"), org_agenda_overriding_header = "Global list of NEXT tasks" },
    { type = "tags", match = match("/WAIT"), org_agenda_overriding_header = "Global list of WAIT tasks" },
    { type = "tags_todo", match = match('+PRIORITY>="C"'), org_agenda_overriding_header = "Global list of High Priority tasks" },
    { type = "tags", match = match("/TODO"), org_agenda_overriding_header = "Global list of TODO tasks" },
    { type = "tags", match = match("/PEND"), org_agenda_overriding_header = "Global list of PEND tasks" },
  }
end

-- Teaching branch intentionally bare (no +typTask): preserves current behavior where
-- teaching headlines match regardless of typ.
local work_agenda =
  make_task_agenda({ "topTeaching", "topWork+typTask" }, "topWork+typTask-catRecurring|topTeaching+typTask-catRecurring")
local task_agenda = make_task_agenda(nil, "typTask-catRecurring")

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
    org_agenda_files = { base_dir .. "**/*.org", base_dir .. "**/.logs/**/*.org" },
  },
}

local extended_agenda_commands = {
  K = { description = "Tracker Agenda", types = tracker_agenda },
  k = { description = "Task Agenda", types = task_agenda },
  w = { description = "Work Agenda", types = work_agenda },
  c = { description = "Combined View", types = task_doc_agenda },
  L = { description = "Backlog", types = backlog },
  h = {
    description = "HOME+Name tags searches",
    submenu = {
      l = {
        description = "Lisa  — home+Lisa",
        types = { { type = "tags", match = "+home+Lisa", org_agenda_overriding_header = "HOME Lisa" } },
      },
      p = {
        description = "Peter — home+Peter",
        types = { { type = "tags", match = "+home+Peter", org_agenda_overriding_header = "HOME Peter" } },
      },
      k = {
        description = "Kim   — home+Kim",
        types = { { type = "tags", match = "+home+Kim", org_agenda_overriding_header = "HOME Kim" } },
      },
    },
  },
  Q = {
    description = "Queries (subpage)",
    submenu = {
      a = {
        description = "Project A — project-A",
        types = { { type = "tags", match = "project-A", org_agenda_overriding_header = "Project A" } },
      },
      b = {
        description = "Project B — project-B",
        types = { { type = "tags", match = "project-B", org_agenda_overriding_header = "Project B" } },
      },
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
