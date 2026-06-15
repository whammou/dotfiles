local dir = require("config.orgmode.directories")
local utils = require("config.orgmode.utils")

local base_dir = dir.base_dir
local zettel_dir = dir.zettel_dir

local roam_templates = {
  z = {
    description = "Zettelkasten",
    template = [[#+OPTIONS: title:nil tags:nil todo:nil ^:nil f:t
#+FILETAGS:
%?]],
    target = "topics/vault/%^{Insert node|draft|%(return vim.fn.expand('%:t:r'))|" .. utils.get_filename(
      base_dir .. zettel_dir
    ) .. "}.org",
  },
  n = {
    description = "New Document",
    template = [[#+TODO: TODO(t) (e) DOIN(d) PROG(g) PEND(p) OUTL(o) EXPL(x) FDBK(b) WAIT(w) NEXT(n) IDEA(i) | ABRT(a) PRTL(r) RVIW(v) DONE(f)
#+OPTIONS: title:nil tags:nil todo:nil ^:nil f:t num:t pri:nil toc:t
#+FILETAGS:
%?]],
    target = "%^{Topic|" .. utils.get_dir_path(base_dir, "docs") .. "}" .. "/%[slug].org",
  },
}

require("org-roam").setup({
  directory = base_dir,
  org_files = { base_dir .. "/topics/**/*.org" },
  extensions = { dailies = { directory = zettel_dir .. "/" .. ".daily" } },
  database = {
    path = vim.fn.expand("~/.roamdb.json"),
    persist = true,
    update_on_save = false,
  },
  ui = {
    node_buffer = {
      show_keybindings = false,
      focus_on_toggle = false,
      highlight_previews = true,
      open = function()
        local width = math.floor(vim.o.columns / 4)
        local height = math.floor(vim.o.lines)

        vim.api.nvim_open_win(0, true, {
          split = "right",
          width = width,
          height = height,
        })
      end,
    },
  },
  bindings = {
    capture = "<leader>od",
  },
  templates = roam_templates,
})
