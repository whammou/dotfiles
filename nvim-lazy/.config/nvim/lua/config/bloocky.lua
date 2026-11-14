local M = {}

local ok, secrets = pcall(require, "config.secrets")
if not ok or type(secrets) ~= "table" then
  secrets = {}
end

local google = secrets.google or {}

-- The calendar set lives in tracked config so every machine syncs the same one;
-- only credentials and the account address stay in the untracked secrets file.
local calendars = google.calendars
  or {
    { name = "Timeblocks", mode = "rw", default = true },
    -- { name = "Work", mode = "ro" },
    -- { name = "Work", mode = "ro" },
  }

-- Google names the primary calendar after the account address, so it can only
-- be matched once the secrets file supplies that address.
if type(google.email) == "string" and google.email ~= "" then
  table.insert(calendars, { name = google.email, mode = "ro" })
end

local sync_enabled = type(google.client_id) == "string" and google.client_id ~= ""

M.opts = {
  week_start = "monday",
  hours = { start = 6, ["end"] = 22 },
  window = { mode = "float", border = "single" },
  keymaps = { toggle = false, toggle_sidebar = false },
  sync = {
    enabled = sync_enabled,
    accounts = {},
    window = { past_days = 14, future_days = 120 },
  },
}

if sync_enabled then
  M.opts.sync.accounts = {
    {
      id = "gcal",
      provider = "google",
      client_id = google.client_id,
      client_secret = google.client_secret,
      client_secret_cmd = google.client_secret_cmd,
      calendars = calendars,
    },
  }
end

return M.opts
