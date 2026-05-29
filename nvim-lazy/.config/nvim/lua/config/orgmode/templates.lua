local dir = require("config.orgmode.directories")
local utils = require("config.orgmode.utils")
local base_dir = dir.base_dir
local zettel_dir = dir.zettel_dir

-- local org_doc_dirs = "%^{Topic|" .. utils.get_dir_path(base_dir, "docs") .. "}"
local org_tasks = base_dir .. "%^{Topic|" .. utils.get_file_path(base_dir, "tasks") .. "}"
local org_dev = base_dir .. "%^{Topic|" .. utils.get_file_path(base_dir, "dev") .. "}"
local org_milestone = base_dir .. "%^{Topic|" .. utils.get_file_path(base_dir, "milestones") .. "}"
local org_lists = base_dir .. "%^{Topic|" .. utils.get_file_path(base_dir, "lists") .. "}"

local task_template = "** %?\n:PROPERTIES:\n:ID: %(return vim.fn.system('uuidgen')):END:"
local capture_templates = {
  c = { description = "Capture", template = "* %?", target = "~/Journal/capture.org" },

  m = {
    description = "Milestone Capture",
    subtemplates = {
      M = {
        description = "Major milestone capture",
        template = task_template,
        target = org_milestone .. "/milestones/major.org",
      },
      m = {
        description = "Minor milestone capture",
        template = task_template,
        target = org_milestone .. "/milestones/minor.org",
      },
    },
  },

  d = {
    description = "Document Capture",
    template = task_template,
    target = base_dir .. "%^{Topic|" .. utils.get_file_path(base_dir, "draft.org") .. "}/draft.org",
  },

  e = {
    description = "New development",
    subtemplates = {
      b = {
        description = "Bug report",
        template = task_template,
        target = org_dev .. "/dev/bug.org",
      },
      i = {
        description = "Issue capture",
        template = task_template,
        target = org_dev .. "/dev/issue.org",
      },
      e = {
        description = "Enhancement capture",
        template = task_template,
        target = org_dev .. "/dev/enhancement.org",
      },
      r = {
        description = "Refactor capture",
        template = task_template,
        target = org_dev .. "/dev/refactor.org",
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
      },
      i = {
        description = "Incidental Tasks",
        template = task_template,
        target = org_tasks .. "/tasks/incidental.org",
      },
      c = {
        description = "Coordinated Tasks",
        template = task_template,
        target = org_tasks .. "/tasks/coordinated.org",
      },
      p = {
        description = "Planned Tasks",
        template = task_template,
        target = org_tasks .. "/tasks/planned.org",
      },
      r = {
        description = "Recurring Tasks",
        template = task_template,
        target = org_tasks .. "/tasks/recurring.org",
      },
    },
  },

  l = {
    description = "List capture",
    subtemplates = {
      p = {
        description = "Purchase List",
        template = "** %<%Y%m%d> - %^{List Title}\n:PROPERTIES:\n:CREATED_ON: %<%y%m%d>\n:END:\n%?",
        target = org_lists .. "/lists/purchase.org",
      },
      l = {
        description = "Location List",
        template = "** %^{Enter Location Name}",
        target = org_lists .. "/lists/location.org",
      },
    },
  },
}

local roam_template = {
  b = {
    description = "Report bug",
    template = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: OPEN(y) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
#+FILETAGS: :typDev:catBug:
%?]],
    target = "%^{Topic|" .. utils.get_dir_path(base_dir, "dev") .. "}" .. "/bug.org",
  },
  i = {
    description = "New issue",
    template = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: OPEN(y) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
#+FILETAGS: :typDev:catIssue:
%?]],
    target = "%^{Topic|" .. utils.get_dir_path(base_dir, "dev") .. "}" .. "/issue.org",
  },
  e = {
    description = "New enhancement",
    template = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: OPEN(y) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
#+FILETAGS: :typDev:catEnhancement:
%?]],
    target = "%^{Topic|" .. utils.get_dir_path(base_dir, "dev") .. "}" .. "/enhancement.org",
  },
  r = {
    description = "Refactor Tickets",
    template = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: OPEN(y) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
#+FILETAGS: :typDev:catRefactor:
%?]],
    target = "%^{Topic|" .. utils.get_dir_path(base_dir, "dev") .. "}" .. "/refactor.org",
  },
  m = {
    description = "Minor Milestone",
    template = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: TODO (t) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
#+FILETAGS: :typMilestone:catMinor:
%?]],
    target = "%^{Topic|" .. utils.get_dir_path(base_dir, "milestones") .. "}" .. "/minor.org",
  },
  M = {
    description = "Major Milestone",
    template = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: TODO (t) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
#+FILETAGS: :typMilestone:catMajor:
%?]],
    target = "%^{Topic|" .. utils.get_dir_path(base_dir, "milestones") .. "}" .. "/major.org",
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
#+TODO: TODO(t) (e) DOIN(d) PROG(g) PEND(p) OUTL(o) EXPL(x) FDBK(b) WAIT(w) NEXT(n) IDEA(i) | ABRT(a) PRTL(r) RVIW(v) DONE(f)
%?]],
    target = "%^{Topic|" .. utils.get_dir_path(base_dir, "docs") .. "}" .. "/%[slug].org",
  },
}

local templates = {
  roam = roam_template,
  capture = capture_templates,
}
return templates
