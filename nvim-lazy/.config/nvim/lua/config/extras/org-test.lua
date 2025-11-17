-- init.lua or a dedicated module (e.g., lua/myconfig/org.lua)

-- Dummy functions for demonstration. Replace with your actual implementation.
local function _get_file_path(base, name)
  return base .. "/" .. name .. ".org"
end

-- Define your base directory (e.g., where your org files are)
-- This could be dynamic or a fixed path.
local base_dir = vim.fn.stdpath("config") .. "/org"

-- 1. Create a function to calculate `org_tasks`
-- This makes it easy to re-run the calculation.
local function get_org_tasks_path()
  -- Ensure base_dir is accessible or passed as an argument
  return base_dir .. "%^{Topic|" .. _get_file_path(base_dir, "tasks") .. "}"
end

-- Initialize org_tasks with its initial value
local org_tasks_path = get_org_tasks_path()

-- 2. Create a function to define/update your capture templates
-- This function will use the *current* value of `org_tasks_path`.
local function setup_org_capture_templates()
  local current_org_tasks_path = get_org_tasks_path() -- Recalculate or use the updated value

  local capture_templates = {
    t = {
      description = "Task",
      subtemplates = {
        o = {
          description = "Oneoff Tasks",
          template = "** %?",
          -- IMPORTANT: Use the current_org_tasks_path here
          target = current_org_tasks_path .. "/tasks/oneoff.org",
          headline = "List of Oneoff Tasks",
        },
        -- ... other templates
      },
    },
    -- ... other template types
  }

  -- If you're using `nvim-orgmode`, this is where you'd pass the updated templates:
  require("orgmode").setup({
    -- ... other orgmode settings
    org_capture_templates = capture_templates,
  })

  vim.notify("Orgmode capture templates reloaded. org_tasks_path: " .. current_org_tasks_path, vim.log.levels.INFO)
end

-- 3. Initial setup when Neovim starts
-- Call the setup function to configure orgmode for the first time.
setup_org_capture_templates()

-- 4. Create a Neovim User Command to trigger the update
-- This command will call the `setup_org_capture_templates` function.
vim.api.nvim_create_user_command("ReloadOrgConfig", setup_org_capture_templates, {
  desc = "Reloads Orgmode capture templates and related configuration",
})

-- You might also want a command to update the base_dir if it's dynamic
vim.api.nvim_create_user_command("SetOrgBaseDir", function(opts)
  if opts.fargs[1] then
    base_dir = opts.fargs[1]
    vim.notify("Org Base Directory set to: " .. base_dir .. ". Reloading config...", vim.log.levels.INFO)
    setup_org_capture_templates() -- Immediately reload templates with new base_dir
  else
    vim.notify("Usage: :SetOrgBaseDir <path>", vim.log.levels.WARN)
  end
end, { nargs = 1, complete = "dir", desc = "Set the base directory for Org files" })
