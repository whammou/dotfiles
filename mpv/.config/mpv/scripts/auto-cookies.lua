-- auto-cookies.lua: refresh qutebrowser cookies before yt-dlp runs
-- The exporter lives at ~~ /export-qutebrowser-cookies.py (moved out of scripts/ so mpv
-- doesn't try to load it as a script). We run it early so ~/.cache/qutebrowser-cookies.txt
-- is always fresh, fixing "Sign in to confirm you're not a bot".
local utils = require("mp.utils")
local msg = require("mp.msg")

local function refresh_cookies()
    local script = mp.find_config_file("export-qutebrowser-cookies.py")
    if not script then
        msg.warn("auto-cookies: export-qutebrowser-cookies.py not found in config dir")
        return
    end
    -- Use persistent cache. On thinkpad the local qutebrowser DB is stale (SABR 360p fallback),
    -- so keep the synced good file at ~/.cache and don't overwrite it there. Regenerate to /tmp instead.
    local hostname = (io.popen("uname -n 2>/dev/null"):read("*l") or "")
    local is_thinkpad = hostname:find("thinkpad")
    local out = is_thinkpad and "/tmp/qutebrowser-cookies.txt"
        or (os.getenv("HOME") .. "/.cache/qutebrowser-cookies.txt")
    -- Run synchronously, block briefly (export is <100ms)
    local res = utils.subprocess({
        args = { "python3", script, out },
        cancellable = false,
    })
    if res.status == 0 then
        msg.verbose("auto-cookies: refreshed " .. out)
    else
        msg.warn("auto-cookies: export failed status=" .. tostring(res.status) .. " stderr=" .. (res.stderr or ""))
    end
end

-- Refresh once on startup (covers first file)
refresh_cookies()

-- Also refresh on every ytdl URL before the hook runs. Priority 0 runs before ytdl_hook (which is 10+).
mp.add_hook("on_load", 1, function()
    local path = mp.get_property("path", "")
    if path:find("youtu%.?be") or path:find("youtube%.com") then
        refresh_cookies()
    end
end)
