local dir = require("config.orgmode.directories")
local utils = require("config.orgmode.utils")
local base_dir = dir.base_dir
local zettel_dir = dir.zettel_dir

local org_tasks = base_dir .. "%^{Topic|" .. utils.get_file_path(base_dir, "tasks") .. "}"
local org_dev = base_dir .. "%^{Topic|" .. utils.get_file_path(base_dir, "dev") .. "}"
local org_doc_dirs = "%^{Topic|" .. utils.get_dir_path(base_dir, "docs") .. "}"
local org_lists = base_dir .. "%^{Topic|" .. utils.get_file_path(base_dir, "lists") .. "}"

local task_template = "** %?\n:PROPERTIES:\n:ID: %(return vim.fn.system('uuidgen')):END:"
local capture_templates = {
  c = { description = "Capture", template = "* %?", target = "~/Journal/capture.org" },
  e = {
    description = "New development",
    subtemplates = {
      b = {
        description = "Bug report",
        template = task_template,
        target = org_dev .. "/dev/bug.org",
        headline = "Bug List",
      },
      i = {
        description = "Issue capture",
        template = task_template,
        target = org_dev .. "/dev/issue.org",
        headline = "Issues List",
      },
      e = {
        description = "Enhancement capture",
        template = task_template,
        target = org_dev .. "/dev/enhancement.org",
        headline = "Enhancement List",
      },
    },
  },
  t = {
    description = "Task note capture",
    subtemplates = {
      o = {
        description = "Oneoff Tasks",
        template = task_template,
        target = org_tasks .. "/tasks/oneoff.org",
        headline = "List of Oneoff Tasks",
      },
      i = {
        description = "Incidental Tasks",
        template = task_template,
        target = org_tasks .. "/tasks/incidental.org",
        headline = "List of Incidental Tasks",
      },
      c = {
        description = "Coordinated Tasks",
        template = task_template,
        target = org_tasks .. "/tasks/coordinated.org",
        headline = "List of Coordinated Tasks",
      },
      p = {
        description = "Planned Tasks",
        template = task_template,
        target = org_tasks .. "/tasks/planned.org",
        headline = "List of Planned Tasks",
      },
      r = {
        description = "Recurring Tasks",
        template = task_template,
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

local roam_template = {
  b = {
    description = "Report bug",
    template = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: OPEN(y) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
* Bugs List :typDev:catBug:meta:
%?]],
    target = "%^{Topic|" .. utils.get_dir_path(base_dir, "dev") .. "}" .. "/bug.org",
  },
  i = {
    description = "New issue",
    template = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: OPEN(y) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
* Issues List :typDev:catIssue:meta:
%?]],
    target = "%^{Topic|" .. utils.get_dir_path(base_dir, "dev") .. "}" .. "/issue.org",
  },
  e = {
    description = "New enhancement",
    template = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: OPEN(y) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
* Enhancements List :typDev:catEnhancement:meta:
%?]],
    target = "%^{Topic|" .. utils.get_dir_path(base_dir, "dev") .. "}" .. "/enhancement.org",
  },
  z = {
    description = "Zettelkasten",
    template = [[#+OPTIONS: title:nil tags:nil todo:nil ^:nil f:t
%?]],
    target = "topics/vault/%^{Insert node|draft|%(return vim.fn.expand('%:t:r'))|" .. utils.get_filename(
      base_dir .. zettel_dir
    ) .. "}.org",
  },
  n = {
    description = "New Document",
    template = [[#+OPTIONS: title:nil tags:nil todo:nil ^:nil f:t num:t pri:nil toc:t
#+TODO: TODO(t) (e) DOIN(d) PEND(p) OUTL(o) EXPL(x) FDBK(b) WAIT(w) NEXT(n) IDEA(i) | ABRT(a) PRTL(r) RVIW(v) DONE(f)
%?]],
    target = "%^{Topic|" .. utils.get_dir_path(base_dir, "docs") .. "}" .. "/%[slug].org",
  },
  d = {
    description = "Documents",
    subtemplates = {
      c = {
        description = "Capture Document",
        template = "** %?",
        target = "%^{Topic|" .. utils.get_file_path(base_dir, "draft.org") .. "}/draft.org",
        headline = "Document Drafts",
      },
    },
  },
}

local templates = {
  roam = roam_template,
  capture = capture_templates,
}
return templates
