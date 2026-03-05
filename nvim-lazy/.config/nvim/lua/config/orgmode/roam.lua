local dir = require("config.orgmode.directories")
local capture = require("config.orgmode.templates")

local base_dir = dir.base_dir
local zettel_dir = dir.zettel_dir

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
    },
  },
  bindings = {
    capture = "<leader>od",
  },
  templates = capture.roam,
})
