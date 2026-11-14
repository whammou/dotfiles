-- Copy to lua/config/secrets.lua (untracked) and fill in.
return {
  google = {
    -- Desktop-app OAuth client from Google Cloud Console.
    client_id = "<PROJECT>.apps.googleusercontent.com",
    -- Optional: omit and Google's PKCE flow works without a client secret.
    -- client_secret_cmd = { "secret-tool", "lookup", "service", "bloocky", "key", "google-client-secret" },
    -- Your Google address. The primary calendar is named after it, so it is
    -- listed read-only under that name once supplied here.
    email = "<you>@gmail.com",
    -- Optional: overrides the calendar list in lua/config/bloocky.lua.
    -- calendars = {
    --   { name = "Timeblocks", mode = "rw", default = true },
    --   { name = "<you>@gmail.com", mode = "ro" },
    -- },
  },
}
