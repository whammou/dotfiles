local dir = require("config.orgmode.directories")
local utils = require("config.orgmode.utils")
local ft = require("config.orgmode.filetags")
local base_dir = dir.base_dir

--- Shared suffix: heading + UUID drawer.
local heading_drawer = "\n\n* %?\n:PROPERTIES:\n:ID: %(return vim.fn.system('uuidgen')):END:"

--- Task preamble: DOIN/PROG/NEXT/WAIT state sequence. Order matches actual task/*.org.
local task_preamble =
  [[#+TODO: TODO(t) (e) DOIN(d) PROG(g) PEND(p) OUTL(o) EXPL(x) FDBK(b) WAIT(w) NEXT(n) IDEA(i) | ABRT(a) PRTL(r) RVIW(v) DONE(f)
#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+FILETAGS:]]

--- Recurring adds RECR before TODO.
local task_preamble_recurring = task_preamble:gsub("#%+TODO: ", "#+TODO: RECR(l) ")

--- Dev preamble: OPEN/PROG/NEXT state sequence.
local dev_preamble = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: OPEN(y) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
#+FILETAGS:]] .. heading_drawer

--- Milestone preamble: TODO state sequence.
local milestone_preamble = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil
#+TODO: TODO (t) (e) PROG(g) INTR(q) NEXT(n) | ABRT(a) DONE(f) CLSD(c)
#+FILETAGS:]] .. heading_drawer

--- List preamble: different TODO with EXPL(s), TARGET(g), IDEA(i) + title:nil.
local list_preamble = [[#+OPTIONS: todo:t tags:nil tasks:t ^:nil toc:nil title:nil
#+TODO: TODO(t) (e) DOIN(d) PROG(g) PEND(p) OUTL(o) EXPL(s) FDBK(b) NEXT(n) TARGET(g) | IDEA(i) ABRT(a) PRTL(r) RVIW(v) DONE(f)
#+FILETAGS:]]

--- Draft preamble: uses same full TODO as tasks, with draft-specific OPTIONS.
--- Matches actual docs/draft.org (minus TITLE, which is file-specific).
local draft_preamble =
  [[#+TODO: TODO(t) (e) DOIN(d) PROG(g) PEND(p) OUTL(o) EXPL(x) FDBK(b) WAIT(w) NEXT(n) IDEA(i) | ABRT(a) PRTL(r) RVIW(v) DONE(f)
#+OPTIONS: title:nil tags:nil todo:nil ^:nil f:t num:t pri:nil toc:t
#+FILETAGS:]]

-- Always list topic directories for capture completion, auto-append subdirectory.
local topic_target = base_dir .. "/%^{Topic|" .. utils.get_topic_dirs() .. "}"

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
        template = milestone_preamble,
        target = topic_target .. "/milestones/major.org",
      },
      m = {
        description = "Minor milestone",
        template = milestone_preamble,
        target = topic_target .. "/milestones/minor.org",
      },
    },
  },

  d = {
    description = "Document capture",
    template = draft_preamble .. heading_drawer,
    target = topic_target .. "/docs/draft.org",
  },

  e = {
    description = "New development",
    subtemplates = {
      b = {
        description = "Bug report",
        template = dev_preamble,
        target = topic_target .. "/dev/bug.org",
      },
      i = {
        description = "New issue",
        template = dev_preamble,
        target = topic_target .. "/dev/issue.org",
      },
      e = {
        description = "New enhancement",
        template = dev_preamble,
        target = topic_target .. "/dev/enhancement.org",
      },
      r = {
        description = "Refactor tickets",
        template = dev_preamble,
        target = topic_target .. "/dev/refactor.org",
      },
    },
  },

  t = {
    description = "Task note capture",
    subtemplates = {
      o = {
        description = "Oneoff tasks",
        template = task_preamble .. heading_drawer,
        target = topic_target .. "/tasks/oneoff.org",
      },
      i = {
        description = "Incidental tasks",
        template = task_preamble .. heading_drawer,
        target = topic_target .. "/tasks/incidental.org",
      },
      c = {
        description = "Coordinated tasks",
        template = task_preamble .. heading_drawer,
        target = topic_target .. "/tasks/coordinated.org",
      },
      p = {
        description = "Planned tasks",
        template = task_preamble .. heading_drawer,
        target = topic_target .. "/tasks/planned.org",
      },
      r = {
        description = "Recurring tasks",
        template = task_preamble_recurring .. heading_drawer,
        target = topic_target .. "/tasks/recurring.org",
      },
    },
  },

  l = {
    description = "List capture",
    subtemplates = {
      p = {
        description = "Purchase list",
        template = list_preamble .. "\n** %<%Y%m%d> - %^{List Title}\n:PROPERTIES:\n:CREATED_ON: %<%y%m%d>\n:END:\n%?",
        target = topic_target .. "/lists/purchase.org",
      },
      l = {
        description = "Location list",
        template = list_preamble .. "\n** %^{Enter Location Name}",
        target = topic_target .. "/lists/location.org",
      },
    },
  },
}

return { capture = capture_templates }
