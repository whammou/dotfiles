local dir = require("config.orgmode.directories")
local capture = require("config.orgmode.templates")

local base_dir = dir.base_dir
local zettel_dir = dir.zettel_dir

require("org-roam").setup({
  directory = base_dir,
  extensions = { dailies = { directory = "/topics/vault/" .. ".daily" } },
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
  templates = capture.roam,
})
