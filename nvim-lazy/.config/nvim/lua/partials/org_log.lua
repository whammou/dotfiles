local dir = require("config.orgmode.directories")
local base_dir = dir.base_dir

require("orgmode").setup({
  org_agenda_files = { base_dir .. "**/*.org", base_dir .. "**/.logs/*.org" },
})
