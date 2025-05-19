local orgmode = vim.fn.stdpath("data") .. "/lazy/orgmode"
vim.opt.runtimepath:append(orgmode)
-- If you are using Packer or any other package manager that uses built-in package manager, do this:
--vim.cmd("packadd orgmode")

-- Run the orgmode cron
require("orgmode").cron({
  org_agenda_files = "~/notes/**/*",
  org_default_notes_file = "~/notes/capture.org",
  notifications = {
    reminder_time = { 0, 10 },
  },
})
