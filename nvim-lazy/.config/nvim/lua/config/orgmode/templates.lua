local dir = require("config.orgmode.directories")
local utils = require("config.orgmode.utils")
local ft = require("config.orgmode.filetags")
local base_dir = dir.base_dir

--- Shared task_template: heading + UUID drawer.
local task_template = "\n\n* %?\n:PROPERTIES:\n:ID: %(return vim.fn.system('uuidgen')):END:"

--- Task preamble: DOIN/PROG/NEXT/WAIT state sequence.
local task_todo = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: TODO(t) (e) DOIN(d) PROG(g) PEND(p) OUTL(o) EXPL(x) FDBK(b) WAIT(w) NEXT(n) IDEA(i) | ABRT(a) PRTL(r) RVIW(v) DONE(f)
#+FILETAGS: :typTask:catOneoff:]]

--- Recurring adds RECR before TODO.
local task_recurring_todo = task_todo:gsub(
  "#%+TODO: ",
  "#+TODO: RECR(l) "
)

--- Dev preamble: OPEN/PROG/NEXT state sequence.
local dev_template = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: OPEN(y) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
#+FILETAGS: :typDev:catBug:]] .. task_template

--- Milestone templates: preamble with TODO state sequence.
local milestone_template = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: TODO (t) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
#+FILETAGS: :typMilestone:catMinor:]] .. task_template

--- List preamble: different TODO with EXPL(s), TARGET(g), IDEA(i) + title:nil.
local list_preamble = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil title:nil
#+TODO: TODO(t) (e) DOIN(d) PROG(g) PEND(p) OUTL(o) EXPL(s) FDBK(b) NEXT(n) TARGET(g) | IDEA(i) ABRT(a) PRTL(r) RVIW(v) DONE(f)
#+FILETAGS: :typList:catPurchase:]]

-- Pre-computed target prefixes for task/list/draft templates
local org_tasks = base_dir .. "%^{Topic|" .. utils.get_file_path(base_dir, "tasks") .. "}"
local org_lists = base_dir .. "%^{Topic|" .. utils.get_file_path(base_dir, "lists") .. "}"

local capture_templates = {
  c = {
    description = "Capture",
    template = ft.wrap_template("* %?", "~/Journal/capture.org"),
    target = "~/Journal/capture.org",
  },

  m = {
    description = "Milestone",
    subtemplates = {
      M = {
        description = "Major milestone",
        template = milestone_template:gsub(":catMinor:", ":catMajor:"),
        target = base_dir .. "%^{Topic|" .. utils.get_dir_path(base_dir, "milestones") .. "}" .. "/major.org",
      },
      m = {
        description = "Minor milestone",
        template = milestone_template,
        target = base_dir .. "%^{Topic|" .. utils.get_dir_path(base_dir, "milestones") .. "}" .. "/minor.org",
      },
    },
  },

  d = {
    description = "Document capture",
    template = ft.wrap_template(
      task_template,
      base_dir .. "%^{Topic|" .. utils.get_file_path(base_dir, "draft.org") .. "}/draft.org"
    ),
    target = base_dir .. "%^{Topic|" .. utils.get_file_path(base_dir, "draft.org") .. "}/draft.org",
  },

  e = {
    description = "New development",
    subtemplates = {
      b = {
        description = "Bug report",
        template = dev_template,
        target = base_dir .. "%^{Topic|" .. utils.get_dir_path(base_dir, "dev") .. "}" .. "/bug.org",
      },
      i = {
        description = "New issue",
        template = dev_template:gsub(":catBug:", ":catIssue:"),
        target = base_dir .. "%^{Topic|" .. utils.get_dir_path(base_dir, "dev") .. "}" .. "/issue.org",
      },
      e = {
        description = "New enhancement",
        template = dev_template:gsub(":catBug:", ":catEnhancement:"),
        target = base_dir .. "%^{Topic|" .. utils.get_dir_path(base_dir, "dev") .. "}" .. "/enhancement.org",
      },
      r = {
        description = "Refactor tickets",
        template = dev_template:gsub(":catBug:", ":catRefactor:"),
        target = base_dir .. "%^{Topic|" .. utils.get_dir_path(base_dir, "dev") .. "}" .. "/refactor.org",
      },
    },
  },

  t = {
    description = "Task note capture",
    subtemplates = {
      o = {
        description = "Oneoff tasks",
        template = task_todo:gsub(":catOneoff:", ":catOneoff:") .. task_template,
        target = org_tasks .. "/tasks/oneoff.org",
      },
      i = {
        description = "Incidental tasks",
        template = task_todo:gsub(":catOneoff:", ":catIncidental:") .. task_template,
        target = org_tasks .. "/tasks/incidental.org",
      },
      c = {
        description = "Coordinated tasks",
        template = task_todo:gsub(":catOneoff:", ":catCoordinated:") .. task_template,
        target = org_tasks .. "/tasks/coordinated.org",
      },
      p = {
        description = "Planned tasks",
        template = task_todo:gsub(":catOneoff:", ":catPlanned:") .. task_template,
        target = org_tasks .. "/tasks/planned.org",
      },
      r = {
        description = "Recurring tasks",
        template = task_recurring_todo:gsub(":catOneoff:", ":catRecurring:") .. task_template,
        target = org_tasks .. "/tasks/recurring.org",
      },
    },
  },

  l = {
    description = "List capture",
    subtemplates = {
      p = {
        description = "Purchase list",
        template = list_preamble .. "\n** %<%Y%m%d> - %^{List Title}\n:PROPERTIES:\n:CREATED_ON: %<%y%m%d>\n:END:\n%?",
        target = org_lists .. "/lists/purchase.org",
      },
      l = {
        description = "Location list",
        template = list_preamble:gsub(":catPurchase:", ":catLocation:") .. "\n** %^{Enter Location Name}",
        target = org_lists .. "/lists/location.org",
      },
    },
  },
}

return { capture = capture_templates }
