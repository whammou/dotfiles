local orgmode = vim.fn.stdpath("data") .. "/lazy/orgmode"
vim.opt.runtimepath:append(orgmode)
-- If you are using Packer or any other package manager that uses built-in package manager, do this:
--vim.cmd("packadd orgmode")

-- Run the orgmode cron
require("orgmode").cron({
  org_agenda_files = "~/Journal/**/*",
  org_default_notes_file = "~/Journal/capture.org",
  notifications = {
    enabled = true,
    cron_enabled = true,
    reminder_time = { 0, 10 },
    repeater_reminder_time = false,
    deadline_warning_reminder_time = false,
    deadline_reminder = true,
    scheduled_reminder = true,
    cron_notifier = function(tasks)
      for _, task in ipairs(tasks) do
        local subtitle = string.format("<b>%s</b> %s [%s]", task.todo, task.title, tostring(task.level))
        local date = string.format("<b>%s</b>: %s", task.type, task.time:to_string())
        local title = string.format("%s (%s)", task.category, task.humanized_duration)

        --if vim.fn.executable("notify-send") == 1 then
        --  vim.system({
        --    "notify-send",
        --    "--icon=/path/to/orgmode/assets/nvim-orgmode-small.png",
        --    "--app-name=orgmode",
        --    title,
        --    string.format("%s\n%s", subtitle, date),
        --  })
        --end

        vim.system({
          "notify-send",
          "org_cron",
          string.format("%s\n%s\n%s", subtitle, date, title),
        })
      end
    end,
  },
})
