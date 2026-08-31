local utils = require("mp.utils")

-- Stable replace-id so the "Fetching…" interim notification gets replaced by
-- the title (success) or the "Failed to load" notification (failure) instead
-- of stacking on top of each other.
local NOTIFY_ID = 31099

local cover_filenames = {
	"cover.png",
	"cover.jpg",
	"cover.jpeg",
	"folder.jpg",
	"folder.png",
	"folder.jpeg",
	"AlbumArtwork.png",
	"AlbumArtwork.jpg",
	"AlbumArtwork.jpeg",
}

function notify(summary, body, options)
	local option_args = {}
	for key, value in pairs(options or {}) do
		table.insert(option_args, string.format("--%s=%s", key, value))
	end
	return mp.command_native({
		"run",
		"notify-send",
		summary,
		body,
		unpack(option_args),
	})
end

function escape_pango_markup(str)
	return string.gsub(str, "([\"'<>&])", function(char)
		return string.format("&#%d;", string.byte(char))
	end)
end

function notify_media(title, origin, thumbnail)
	return notify("Mpv", escape_pango_markup(title), {
		urgency = "low",
		["app-name"] = "mpv-media",
		["replace-id"] = NOTIFY_ID,
		hint = "string:desktop-entry:mpv",
		icon = thumbnail or "mpv",
	})
end

function notify_fetching(url)
	notify("Mpv", "Fetching " .. escape_pango_markup(url) .. "…", {
		urgency = "low",
		["app-name"] = "mpv-media",
		["replace-id"] = NOTIFY_ID,
		icon = "mpv",
	})
end

function notify_failure(subject, err)
	local body = "Failed to load: " .. escape_pango_markup(subject)
	if err and err ~= "" then
		body = body .. "\n" .. escape_pango_markup(err)
	end
	notify("Mpv", body, {
		urgency = "normal",
		["app-name"] = "mpv-media",
		["replace-id"] = NOTIFY_ID,
		icon = "dialog-error",
	})
end

function is_remote_path(path)
	return type(path) == "string" and path:match("^%a[%w+.-]*://") ~= nil
end

function file_exists(path)
	local info, _ = utils.file_info(path)
	return info ~= nil
end

function find_cover(dir)
	-- make dir an absolute path
	if dir[1] ~= "/" then
		dir = utils.join_path(utils.getcwd(), dir)
	end

	for _, file in ipairs(cover_filenames) do
		local path = utils.join_path(dir, file)
		if file_exists(path) then
			return path
		end
	end

	return nil
end

function first_upper(str)
	return (string.gsub(string.gsub(str, "^%l", string.upper), "_%l", string.upper))
end

function notify_current_media()
	local path = mp.get_property_native("path")
	if not path then
		return
	end

	local dir, file = utils.split_path(path)

	local thumbnail, origin
	if is_remote_path(path) then
		-- stream: no local cover, no origin directory (the path is the
		-- resolved CDN URL, which is not meaningful to the user)
		thumbnail, origin = nil, ""
	else
		-- TODO: handle embedded covers and videos?
		-- potential options: mpv's take_screenshot, ffprobe/ffmpeg, ...
		-- hooking off existing desktop thumbnails would be good too
		thumbnail = find_cover(dir)
		origin = dir
	end

	local title = mp.get_property_native("media-title") or file

	local metadata = mp.get_property_native("metadata")
	if metadata then
		function tag(name)
			return metadata[string.upper(name)] or metadata[first_upper(name)] or metadata[name]
		end

		title = tag("title") or title
		origin = tag("artist_credit") or tag("artist") or ""

		local album = tag("album")
		if album then
			origin = string.format("%s — %s", origin, album)
		end

		local year = tag("original_year") or tag("year")
		if year then
			origin = string.format("%s (%s)", origin, year)
		end
	end

	return notify_media(title, origin, thumbnail)
end

-- Track the entry currently trying to load so a fetch failure (file-loaded
-- never firing) can be reported instead of failing silently.
-- end-file reason semantics per https://mpv.io/manual/master/#list-of-events:
--   error    -> an error happened; an error string is present
--   redirect -> yt-dlp resolved the URL to a stream; loading continues (ignore)
--   eof      -> may also mean broken/incomplete network connection
--   stop/quit/unknown -> user action or nothing sensible (stay silent)
local loading_entry, loaded_entry
local fetch_notified = {}
-- Captured at start-file: player properties are cleared again before
-- end-file(error) arrives, so this is what the failure notification shows.
local attempted_subject

mp.register_event("start-file", function(event)
	loading_entry = event.playlist_entry_id
	loaded_entry = nil
	attempted_subject = mp.get_property_native("media-title")
		or mp.get_property_native("path")
		or "unknown media"

	local path = mp.get_property_native("path")
	if is_remote_path(path) and not fetch_notified[loading_entry] then
		fetch_notified[loading_entry] = true
		notify_fetching(path)
	end
end)

mp.register_event("file-loaded", function()
	loaded_entry = loading_entry
	notify_current_media()
end)

mp.register_event("end-file", function(event)
	local reason = event.reason
	if reason == "redirect" then
		-- still resolving; keep waiting for file-loaded or a terminal reason
		return
	end

	local was_loaded = (loaded_entry == loading_entry)
	fetch_notified[loading_entry] = nil

	if reason == "error" then
		notify_failure(attempted_subject or "unknown media", event.file_error or event.error)
	elseif reason == "eof" and not was_loaded then
		-- the load never completed (e.g. connection dropped before playback)
		notify_failure(attempted_subject or "unknown media",
			"Playback ended before the file could be loaded.")
	end

	loading_entry, loaded_entry = nil, nil
end)