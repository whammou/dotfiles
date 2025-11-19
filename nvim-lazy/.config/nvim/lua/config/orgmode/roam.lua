local dir = require("config.orgmode.directories")
local capture = require("config.orgmode.templates")

local base_dir = dir.base_dir
local zettel_dir = dir.zettel_dir

local function setup_roam_template()
  require("org-roam").setup({
    directory = base_dir,
    org_files = { base_dir .. "**/*.org" },
    extensions = { dailies = { directory = zettel_dir .. "/" .. ".daily" } },
    database = {
      path = vim.fn.expand("~/.roamdb.json"),
      persist = true,
      ui = {
        node_buffer = {
          show_keybindings = false,
          focus_on_toggle = false,
          highlight_previews = true,
        },
      },
      update_on_save = false,
    },
    templates = capture.roam,
  })
end

setup_roam_template()

vim.api.nvim_create_user_command("ReloadRoamConfig", setup_roam_template, {
  desc = "Reloads Orgmode capture templates and related configuration",
})
