local orgmode = require("orgmode")
local khalorg = require("khalorg")
local roam = require("org-roam")
local Menu = require("org-modern.menu")

local base_dir = vim.fn.expand("~/Journal/")
local zettel_dir = base_dir .. "topics/vault/"
local relative_dir = vim.fn.getcwd():gsub(base_dir, "")

local function _get_filename(directory)
  local filename = table.concat(
    vim.tbl_map(function(path)
      local filename = vim.fn.fnamemodify(path, ":t")
      return (string.gsub(filename, "%.org$", ""))
    end, vim.split(vim.fn.globpath(directory, "*.org"), "\n", { trimempty = true })),
    "|"
  )
  return filename
end

local function _get_file_path(directory, filename)
  local cmd = 'find "' .. vim.fn.fnamemodify(directory, ":p") .. '" -name ' .. filename .. " | paste -s -d '|'"
  local result = vim.fn.system(cmd)
  return string.gsub(string.gsub(result:gsub("\n$", ""), base_dir, ""), filename, "")
end

local function _get_dir_path(directory, filename)
  local cmd = 'find "' .. vim.fn.fnamemodify(directory, ":p") .. '" -type d -name ' .. filename .. " | paste -s -d '|'"
  local result = vim.fn.system(cmd)
  return string.gsub(result:gsub("\n$", ""), base_dir, "")
end

local org_tasks = base_dir .. "%^{Topic|" .. _get_file_path(base_dir, "tasks") .. "}"
local org_doc_dirs = "%^{Topic|" .. _get_dir_path(base_dir, "docs") .. "}"
local org_lists = base_dir .. "%^{Topic|" .. _get_file_path(base_dir, "lists") .. "}"

local capture_templates = {
  c = { description = "Capture", template = "* %?", target = "~/Journal/capture.org" },
  t = {
    description = "Task",
    subtemplates = {
      o = {
        description = "Oneoff Tasks",
        template = "** %?",
        target = org_tasks .. "/tasks/oneoff.org",
        headline = "List of Oneoff Tasks",
      },
      i = {
        description = "Incidental Tasks",
        template = "** %?",
        target = org_tasks .. "/tasks/incidental.org",
        headline = "List of Incidental Tasks",
      },
      c = {
        description = "Coordinated Tasks",
        template = "** %?",
        target = org_tasks .. "/tasks/coordinated.org",
        headline = "List of Coordinated Tasks",
      },
      p = {
        description = "Planned Tasks",
        template = "** %?",
        target = org_tasks .. "/tasks/planned.org",
        headline = "List of Planned Tasks",
      },
      r = {
        description = "Recurring Tasks",
        template = "** %?",
        target = org_tasks .. "/tasks/recurring.org",
        headline = "List of Recurring Tasks",
      },
    },
  },
  l = {
    description = "List",
    subtemplates = {
      p = {
        description = "Purchase List",
        template = "** %<%Y%m%d> - %^{List Title}\n:PROPERTIES:\n:CREATED_ON: %<%y%m%d>\n:END:\n%?",
        target = org_lists .. "/lists/purchase.org",
        headline = "Purchase Lists",
      },
      l = {
        description = "Location List",
        template = "** %^{Enter Location Name}",
        target = org_lists .. "/lists/location.org",
        headline = "Location List",
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
local backlog = {
  {
    type = "tags",
    match = "/PEND|OUTL",
    org_agenda_overriding_header = "Document Tasks",
    org_agenda_span = "week",
  },
}

local rtf_export = {
  label = "Export to RTF format",
  action = function(exporter)
    local current_file = vim.api.nvim_buf_get_name(0)
    local target = vim.fn.fnamemodify(current_file, ":p:r") .. ".rtf"
    local command = { "pandoc", current_file, "-o", target }
    local on_success = function(output)
      print("Success!")
      vim.api.nvim_echo({ { table.concat(output, "\n") } }, true, {})
    end
    local on_error = function(err)
      print("Error!")
      vim.api.nvim_echo({ { table.concat(err, "\n"), "ErrorMsg" } }, true, {})
    end
    return exporter(command, target, on_success, on_error)
  end,
}

local custom_exports = {
  n = { label = "Add a new khal item", action = khalorg.new },
  d = { label = "Delete a khal item", action = khalorg.delete },
  e = { label = "Edit properties of a khal item", action = khalorg.edit },
  E = { label = "Edit properties & dates of a khal item", action = khalorg.edit_all },
  f = rtf_export,
}

roam.setup({
  directory = base_dir,
  org_files = { "~/Journal/**/*.org" },
  extensions = { dailies = { directory = zettel_dir .. "/" .. ".daily" } },
  database = {
    path = "/home/whammou/.roamdb.json",
    persist = true,
    update_on_save = false,
  },
  templates = {
    z = {
      description = "Zettelkasten",
      template = [[#+OPTIONS: title:nil tags:nil todo:nil ^:nil f:t
#+LATEX_HEADER: \renewcommand\maketitle{} \usepackage[scaled]{helvet} \renewcommand\familydefault{\sfdefault}
%?]],
      target = "vault/%^{Insert node|draft|%(return vim.fn.expand('%:t:r'))|" .. _get_filename(zettel_dir) .. "}.org",
    },
    n = {
      description = "New Document",
      template = [[#+OPTIONS: title:nil tags:nil todo:nil ^:nil f:t num:t pri:nil toc:t
#+LATEX_HEADER: \renewcommand\maketitle{} \usepackage[scaled]{helvet} \renewcommand\familydefault{\sfdefault}
#+TODO: TODO(t) (e) DOING(d) PEND(p) OUTL(o) RESEARCH(s) FEEDBACK(b) WAITING(w) NEXT(n) | IDEA(i) ABORTED(a) PARTIAL(r) REVIEW(v) DONE(f)
%?]],
      target = org_doc_dirs .. "/%[slug].org",
    },
    d = {
      description = "Documents",
      subtemplates = {
        c = {
          description = "Capture Document",
          template = "** %?",
          target = base_dir .. "/%^{Topic|" .. _get_file_path(base_dir, "draft.org") .. "}/draft.org",
          headline = "Document Drafts",
        },
      },
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
  win_split_mode = "99new",
  org_agenda_text_search_extra_files = { "agenda-archives" },
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
    l = {
      description = "Backlog",
      types = backlog,
    },
  },
  ui = {
    menu = {
      handler = function(data)
        Menu:new({
          window = {
            margin = { 1, 0, 1, 0 },
            padding = { 0, 1, 0, 1 },
            title_pos = "center",
            border = "single",
            zindex = 1000,
          },
          icons = {
            separator = "➜",
          },
        }):open(data)
      end,
    },
  },
})
