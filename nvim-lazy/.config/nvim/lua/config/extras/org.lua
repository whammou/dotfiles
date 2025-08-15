local orgmode = require("orgmode")
local khalorg = require("khalorg")
local roam = require("org-roam")

local zettel_dir = "~/notes/vault"

local zettel = table.concat(
  vim.tbl_map(function(path)
    local filename = vim.fn.fnamemodify(path, ":t")
    return (string.gsub(filename, "%.org$", ""))
  end, vim.split(vim.fn.globpath(zettel_dir, "*.org"), "\n", { trimempty = true })),
  "|"
)
local function _get_dir_path(filename)
  local cmd = 'find "' .. vim.fn.fnamemodify(vim.fn.getcwd(), ":p") .. '" -name ' .. filename .. " | paste -s -d '|'"
  local result = vim.fn.system(cmd)
  return result:gsub("\n$", "")
end

local org_tasks = "%^{Topic|system|" .. _get_dir_path("tasks.org") .. "}"
local org_docs = "%^{Topic|system|" .. _get_dir_path("doc.org") .. "}"

local capture_templates = {
  c = { description = "Capture", template = "* %?", target = "~/notes/capture.org" },
  d = {
    description = "Document",
    template = "** %?",
    target = org_docs,
    headline = "Documents",
  },
  t = {
    description = "Task",
    subtemplates = {
      o = {
        description = "One-off",
        template = "** %?",
        target = org_tasks,
        headline = "One-off",
      },
      i = {
        description = "Incidental",
        template = "** %?",
        target = org_tasks,
        headline = "Incidental",
      },
      c = {
        description = "Coordinated",
        template = "** %?",
        target = org_tasks,
        headline = "Coordinated",
      },
      u = {
        description = "Urgent",
        template = "** %?",
        target = org_tasks,
        headline = "Urgent",
      },
      r = {
        description = "Recurring",
        template = "** %?",
        target = org_tasks,
        headline = "Recurring",
      },
    },
  },
}

local task_agenda = {
  {
    type = "agenda",
    org_agenda_tag_filter_preset = { "ONEOFF", "INCIDENTAL", "COORDINATED", "URGENT" },
    org_agenda_overriding_header = "Daily Tasks",
    org_agenda_span = "week",
  },
}

local doc_agenda = {
  {
    type = "agenda",
    org_agenda_tag_filter_preset = "DOC",
    org_agenda_overriding_header = "Document Tasks",
    org_agenda_span = "week",
  },
}

local task_doc_agenda = {
  {
    type = "agenda",
    org_agenda_tag_filter_preset = "TASK-RECURRING",
    org_agenda_overriding_header = "Daily Tasks",
    org_agenda_span = "day",
  },
  {
    type = "agenda",
    org_agenda_tag_filter_preset = "DOC",
    org_agenda_overriding_header = "Document Tasks",
    org_agenda_span = "day",
  },
}

local custom_exports = {
  n = { label = "Add a new khal item", action = khalorg.new },
  d = { label = "Delete a khal item", action = khalorg.delete },
  e = { label = "Edit properties of a khal item", action = khalorg.edit },
  E = { label = "Edit properties & dates of a khal item", action = khalorg.edit_all },
}

roam.setup({
  directory = "~/notes/vault/",
  org_files = { "~/notes/**/*.org" },
  database = {
    path = "/home/whammou/notes/.roamdb.json",
    persist = true,
    update_on_save = false,
  },
  templates = {
    t = {
      description = "zettel",
      template = [[#+OPTIONS: title:nil tags:nil todo:nil ^:nil f:t
#+LATEX_HEADER: \\renewcommand\\maketitle{} \\usepackage[scaled]{helvet} \\renewcommand\\familydefault{\\sfdefault}
%?]],
      target = "%^{Insert node|draft|%(return vim.fn.expand('%:t:r'))|" .. zettel .. "}",
    },
  },
  ui = {
    node_buffer = {
      show_keybindings = false,
      focus_on_toggle = false,
      highlight_previews = true,
    },
  },
})

orgmode.setup({
  org_custom_exports = custom_exports,
  org_capture_templates = capture_templates,
  org_agenda_custom_commands = {
    k = {
      description = "Task Agenda",
      types = task_agenda,
    },
    c = {
      description = "Document Agenda",
      types = doc_agenda,
    },
    A = {
      description = "Combined View",
      types = task_doc_agenda,
    },
  },
})
