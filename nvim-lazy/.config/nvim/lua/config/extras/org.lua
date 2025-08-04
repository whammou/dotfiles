local orgmode = require("orgmode")
local khalorg = require("khalorg")
local roam = require("org-roam")

local zettel_dir = "~/notes/vault"

local zettel = table.concat(
  vim.tbl_map(
    function(path)
      -- Get the filename from the full path (e.g., "/home/user/doc.org" -> "doc.org")
      local filename = vim.fn.fnamemodify(path, ":t")
      -- Remove the ".org" extension from the end of the filename
      return string.gsub(filename, "%.org$", "")
    end,
    -- Get a list of all .org files in the current working directory, separated by newlines
    -- Then split this string into a Lua table of individual file paths
    vim.split(vim.fn.globpath(zettel_dir, "*.org"), "\n", { trimempty = true })
  ),
  "|"
)

local cmd = 'find "' .. vim.fn.fnamemodify(vim.fn.getcwd(), ":p") .. "\" -name tasks.org | paste -s -d '|'"
local result = vim.fn.system(cmd)
-- system() often includes a trailing newline, remove it
result = result:gsub("\n$", "")
-- print(result)

--local note_topics =
--  "~/notes/%^{Topic|system|academic|academic/teaching|coding|finance|language|platform|read|routine|system|system/packages|travel|university|work}/tasks.org"

local note_topics = "%^{Topic|system|" .. result .. "}"

local capture_templates = {
  d = { description = "Document", template = "* %? [%]" },
  c = { description = "Capture", template = "* %?", target = "~/notes/capture.org" },
  t = {
    description = "Task",
    subtemplates = {
      o = {
        description = "One-off",
        template = "** %?",
        target = note_topics,
        headline = "One-off",
      },
      i = {
        description = "Incidental",
        template = "** %?",
        target = note_topics,
        headline = "Incidental",
      },
      c = {
        description = "Coordinated",
        template = "** %?",
        target = note_topics,
        headline = "Coordinated",
      },
      u = {
        description = "Urgent",
        template = "** %?",
        target = note_topics,
        headline = "Urgent",
      },
      r = {
        description = "Recurring",
        template = "** %?",
        target = note_topics,
        headline = "Recurring",
      },
    },
  },
}

local task_agenda = {
  {
    type = "agenda",
    org_agenda_tag_filter_preset = "TASK",
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
    org_agenda_tag_filter_preset = "TASK",
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
      template = "#+OPTIONS: title:nil tags:nil todo:nil ^:nil f:t\n#+LATEX_HEADER: \\renewcommand\\maketitle{} \\usepackage[scaled]{helvet} \\renewcommand\\familydefault{\\sfdefault}\n%?",
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
