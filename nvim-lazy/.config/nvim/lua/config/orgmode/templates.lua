local base_dir = vim.fn.expand("~/Journal/")
local zettel_dir = base_dir .. "/topics/vault/"
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
      A = {
        description = "Combined View",
        types = task_doc_agenda,
      },
      l = {
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

local roam_template = {
  roam = {
    z = {
      description = "Zettelkasten",
      template = [[#+OPTIONS: title:nil tags:nil todo:nil ^:nil f:t
#+LATEX_HEADER: \renewcommand\maketitle{} \usepackage[scaled]{helvet} \renewcommand\familydefault{\sfdefault}
%?]],
      target = "topics/vault/%^{Insert node|draft|%(return vim.fn.expand('%:t:r'))|"
        .. _get_filename(zettel_dir)
        .. "}.org",
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
          target = "/%^{Topic|" .. _get_file_path(base_dir, "draft.org") .. "}/draft.org",
          headline = "Document Drafts",
        },
      },
    },
  },
}

return roam_template
