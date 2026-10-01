----------------------
-- #example ytdl_preload.conf
-- # make sure lines do not have trailing whitespace
-- # ytdl_opt has no sanity check and should be formatted exactly how it would appear in yt-dlp CLI, they are split into a key/value pair on whitespace
-- # at least on Windows, do not escape '\' in temp, just us a single one for each divider

-- #temp=R:\ytdltest
-- #subLangs = "en",
-- #ytdl_opt1=-r 50k
-- #ytdl_opt2=-N 5
-- #ytdl_opt#=etc
----------------------
local nextIndex
local caught = true
-- local pop = false
local ytdl = "yt-dlp"
local utils = require("mp.utils")
local msg = require("mp.msg")

local function notify(level, text, osd_seconds)
	if level == "error" then
		msg.error(text)
	elseif level == "warn" then
		msg.warn(text)
	elseif level == "info" then
		msg.info(text)
	else
		msg.verbose(text)
	end
	if osd_seconds then
		mp.osd_message("ytdl-preload: " .. text, osd_seconds)
	end
end

local options = require("mp.options")
local opts = {
	temp = "/tmp/ytdl-preload",
	subLangs = "en",
	format = mp.get_property("ytdl-format"),
	ytdl_opt1 = "",
	ytdl_opt2 = "",
	ytdl_opt3 = "",
	ytdl_opt4 = "",
	ytdl_opt5 = "",
	ytdl_opt6 = "",
	ytdl_opt7 = "",
	ytdl_opt8 = "",
	ytdl_opt9 = "",
}
options.read_options(opts, "ytdl_preload")
-- print(opts.temp)
local additionalOpts = {}
for k, v in pairs(opts) do
	if k:find("ytdl_opt%d") and v ~= "" then
		additionalOpts[k] = v
		-- print("entry")
		-- print(k .. v)
	end
end
local cachePath = opts.temp
-- ensure cache directory exists (fixes Lua error: ftd nil when dir missing)
os.execute("mkdir -p '" .. cachePath .. "'")

local restrictFilenames = "--no-restrict-filenames"
local chapter_list = {}
local json = ""
local filesToDelete = {}

local function exists(file)
	local ok, err, code = os.rename(file, file)
	if not ok then
		if code == 13 then -- Permission denied, but it exists
			return true
		end
	end
	return ok, err
end
local function useNewLoadfile()
	for _, c in pairs(mp.get_property_native("command-list")) do
		if c["name"] == "loadfile" then
			for _, a in pairs(c["args"]) do
				if a["name"] == "index" then
					return true
				end
			end
		end
	end
end
--from ytdl_hook
local function time_to_secs(time_string)
	local ret
	local a, b, c = time_string:match("(%d+):(%d%d?):(%d%d)")
	if a ~= nil then
		ret = (a * 3600 + b * 60 + c)
	else
		a, b = time_string:match("(%d%d?):(%d%d)")
		if a ~= nil then
			ret = (a * 60 + b)
		end
	end
	return ret
end
local function extract_chapters(data, video_length)
	local ret = {}
	for line in data:gmatch("[^\r\n]+") do
		local time = time_to_secs(line)
		if time and (time < video_length) then
			table.insert(ret, { time = time, title = line })
		end
	end
	table.sort(ret, function(a, b)
		return a.time < b.time
	end)
	return ret
end
local function chapters()
	if json.chapters then
		for i = 1, #json.chapters do
			local chapter = json.chapters[i]
			local title = chapter.title or ""
			if title == "" then
				title = string.format("Chapter %02d", i)
			end
			table.insert(chapter_list, { time = chapter.start_time, title = title })
		end
	elseif not (json.description == nil) and not (json.duration == nil) then
		chapter_list = extract_chapters(json.description, json.duration)
	end
end
--end ytdl_hook
local title = ""
local fVideo = ""
local fAudio = ""
local function load_files(dtitle, destination, audio, wait)
	if wait then
		if exists(destination .. ".mka") then
			msg.verbose("audio found after wait, loading with separate audio")
			audio = "audio-file=" .. destination .. ".mka,"
		else
			notify("warn", "audio missing after wait, loading video-only", 4)
		end
	end
	-- if audio ~= "" then
	-- 	table.insert(filesToDelete, destination .. ".mka")
	-- end
	-- table.insert(filesToDelete, destination .. ".mkv")
	dtitle = dtitle:gsub("-" .. ("[%w_-]"):rep(11) .. "$", "")
	dtitle = dtitle:gsub("^" .. ("%d"):rep(10) .. "%-", "")
	if useNewLoadfile() then
		mp.commandv(
			"loadfile",
			destination .. ".mkv",
			"append",
			-1,
			audio .. 'force-media-title="' .. dtitle .. '",demuxer-max-back-bytes=1MiB,demuxer-max-bytes=3MiB,ytdl=no'
		)
	else
		mp.commandv(
			"loadfile",
			destination .. ".mkv",
			"append",
			audio .. 'force-media-title="' .. dtitle .. '",demuxer-max-back-bytes=1MiB,demuxer-max-bytes=3MiB,ytdl=no'
		) --,sub-file="..destination..".en.vtt") --in case they are not set up to autoload
	end
	mp.commandv("playlist_move", mp.get_property("playlist-count") - 1, nextIndex)
	mp.commandv("playlist_remove", nextIndex + 1)
	caught = true
	title = ""
	-- pop = true
end

local listenID = ""
local swapped = false
local function on_destination(destination)
	if swapped then
		return
	end
	if not (destination and string.find(destination, string.gsub(cachePath, "~/", ""), 1, true)) then
		return
	end
	swapped = true
	mp.unregister_event(listener)
	_, title = utils.split_path(destination)
	local audio = ""
	if fAudio == "" then
		load_files(title, destination, audio, false)
	else
		if exists(destination .. ".mka") then
			audio = "audio-file=" .. destination .. ".mka,"
			load_files(title, destination, audio, false)
		else
			notify("warn", "separate audio not ready yet, retrying shortly", 3)
			mp.add_timeout(2, function()
				load_files(title, destination, audio, true)
			end)
		end
	end
end
local function listener(event)
	if not caught and event.prefix == mp.get_script_name() and string.find(event.text, listenID, 1, true) then
		local destination = string.match(event.text, "%[download%] Destination: (.+).mkv")
			or string.match(event.text, "%[download%] (.+).mkv has already been downloaded")
		-- if destination then print("---"..cachePath) end;
		on_destination(destination)
	end
end
local function find_destination(output)
	if not output or output == "" then
		return nil
	end
	return string.match(output, "%[download%] Destination: (.+).mkv")
		or string.match(output, "%[download%] (.+).mkv has already been downloaded")
end
local function find_cached(prefix, ext)
	local files = utils.readdir(cachePath)
	if not files then
		return nil
	end
	for _, f in ipairs(files) do
		if f:sub(1, #prefix) == prefix and f:sub(-#ext) == ext then
			return cachePath .. "/" .. f:sub(1, -#ext - 1)
		end
	end
	return nil
end

--from ytdl_hook
mp.add_hook("on_preloaded", 10, function()
	if string.find(mp.get_property("path"), cachePath) then
		chapters()
		if next(chapter_list) ~= nil then
			mp.set_property_native("chapter-list", chapter_list)
			chapter_list = {}
			json = ""
		end
	end
end)
--end ytdl_hook
function dump(o)
	if type(o) == "table" then
		local s = "{ "
		for k, v in pairs(o) do
			if type(k) ~= "number" then
				k = '"' .. k .. '"'
			end
			s = s .. "[" .. k .. "] = " .. dump(v) .. ","
		end
		return s .. "} "
	else
		return tostring(o)
	end
end

local function addOPTS(old)
	for k, v in pairs(additionalOpts) do
		-- print(k)
		if string.find(v, "%s") then
			for l, w in string.gmatch(v, "([-%w]+) (.+)") do
				table.insert(old, l)
				table.insert(old, w)
			end
		else
			table.insert(old, v)
		end
	end
	-- print(dump(old))
	return old
end

local AudioDownloadHandle = {}
local VideoDownloadHandle = {}
local JsonDownloadHandle = {}
local function download_files(id, success, result, error)
	if not result or result.killed_by_us then
		mp.unregister_event(listener)
		caught = true
		return
	end
	local stderr = result.stderr or ""
	if result.status ~= 0 or success == false or stderr:lower():find("error") then
		if stderr ~= "" then
			msg.error(stderr)
		end
		notify("error", "dump failed, removing entry " .. tostring((nextIndex or 0) + 1) .. " from playlist", 5)
		mp.unregister_event(listener)
		caught = true
		if nextIndex ~= nil then
			mp.commandv("playlist-remove", nextIndex)
		end
		return
	end
	local stdout = result.stdout or ""
	if stdout == "" then
		notify("warn", "empty dump output, skipping preload (entry will stream)", 4)
		mp.unregister_event(listener)
		caught = true
		return
	end
	-- yt-dlp may prepend non-JSON progress lines (e.g. [download]) when
	-- --write-sub fetches subtitles; strip everything before the first '{'
	local json_start = stdout:find("{", 1, true)
	if json_start and json_start > 1 then
		stdout = stdout:sub(json_start)
	end
	local jfile = cachePath .. "/" .. id .. ".json"

	local jfileIO = io.open(jfile, "w")
	if not jfileIO then
		notify("error", "cannot write " .. jfile .. ", skipping preload", 5)
		mp.unregister_event(listener)
		caught = true
		return
	end
	jfileIO:write(stdout)
	jfileIO:close()
	json = utils.parse_json(stdout)
	if json == nil then
		notify("error", "could not parse dump JSON, skipping preload (entry will stream)", 5)
		mp.unregister_event(listener)
		caught = true
		return
	end
	-- print(dump(json))
	local requested = json.requested_downloads and json.requested_downloads[1]
	if requested and requested.requested_formats ~= nil then
		local args = {
			ytdl,
			"--no-continue",
			"-q",
			"-f",
			fAudio,
			restrictFilenames,
			"--no-playlist",
			"--no-part",
			"--no-embed-subs",
			"-o",
			cachePath .. "/" .. id .. "-%(title)s-%(id)s.mka",
			"--load-info-json",
			jfile,
		}
		args = addOPTS(args)
		AudioDownloadHandle = mp.command_native_async({
			name = "subprocess",
			args = args,
			playback_only = false,
		}, function() end)
	else
		fAudio = ""
		fVideo = fVideo:gsub("bestvideo", "best")
		fVideo = fVideo:gsub("bv", "best")
	end

	local args = {
		ytdl,
		"--no-continue",
		"-f",
		fVideo .. "/best",
		restrictFilenames,
		"--no-playlist",
		"--no-part",
		"--no-embed-subs",
		"-o",
		cachePath .. "/" .. id .. "-%(title)s-%(id)s.mkv",
		"--load-info-json",
		jfile,
	}
	args = addOPTS(args)
	VideoDownloadHandle = mp.command_native_async({
		name = "subprocess",
		args = args,
		playback_only = false,
		capture_stdout = true,
		capture_stderr = true,
	}, function(success, result, error)
		if not result or result.killed_by_us then
			return
		end
		local output = (result.stdout or "") .. "\n" .. (result.stderr or "")
		local destination = find_destination(output)
		if not destination then
			destination = find_cached(id .. "-", ".mkv")
		end
		if destination then
			on_destination(destination)
		elseif not swapped then
			notify("warn", "video download left no local file, entry will stream instead", 4)
			mp.unregister_event(listener)
			caught = true
		end
	end)
end

local function DL()
	local index = tonumber(mp.get_property("playlist-pos"))
	if tonumber(mp.get_property("playlist-count")) > 1 and index == tonumber(mp.get_property("playlist-count")) - 1 then
		index = -1
	end
	if
		index >= 0
		and mp.get_property("playlist/" .. index .. "/filename"):find("/videos$")
		and mp.get_property("playlist/" .. index + 1 .. "/filename"):find("/shorts$")
	then
		return
	end
	if tonumber(mp.get_property("playlist-pos-1")) > 0 then
		nextIndex = index + 1
		local nextFile = mp.get_property("playlist/" .. nextIndex .. "/filename")
		if nextFile and caught and nextFile:find("://", 0, false) then
			caught = false
			swapped = false
			notify("info", "preloading playlist entry " .. tostring(nextIndex + 1), 3)
			mp.enable_messages("info")
			mp.register_event("log-message", listener)
			local ytFormat = opts.format or ""
			fVideo = string.match(ytFormat, "([^/+]+)%+") or "bestvideo"
			fAudio = string.match(ytFormat, "%+([^/]+)") or "bestaudio"
			listenID = tostring(os.time()) .. "-" .. tostring(math.random(1000, 9999))
			local args = {
				ytdl,
				"--dump-single-json",
				"--no-simulate",
				"--skip-download",
				"--no-progress",
				restrictFilenames,
				"--no-playlist",
				"--sub-langs",
				opts.subLangs,
				"--write-sub",
				"--no-part",
				"-o",
				cachePath .. "/" .. listenID .. "-%(title)s-%(id)s.%(ext)s",
				nextFile,
			}
			args = addOPTS(args)
			-- print(dump(args))
			table.insert(filesToDelete, listenID)
			JsonDownloadHandle = mp.command_native_async({
				name = "subprocess",
				args = args,
				capture_stdout = true,
				capture_stderr = true,
				playback_only = false,
			}, function(...)
				download_files(listenID, ...)
			end)
		end
	end
end

local function clearCache()
	-- print(pop)

	--if pop == true then
	mp.abort_async_command(AudioDownloadHandle)
	mp.abort_async_command(VideoDownloadHandle)
	mp.abort_async_command(JsonDownloadHandle)
	-- for k, v in pairs(filesToDelete) do
	-- 	print("remove: " .. v)
	-- 	os.remove(v)
	-- end
	os.execute("mkdir -p '" .. cachePath .. "'")
	local ftd = io.open(cachePath .. "/temp.files", "a")
	if not ftd then
		msg.warn("ytdl-preload: could not open temp.files for writing at " .. cachePath)
	else
		for k, v in pairs(filesToDelete) do
			ftd:write(v .. "\n")
			if package.config:sub(1, 1) ~= "/" then
				os.execute('del /Q /F "' .. cachePath .. "\\" .. v .. '*"')
			else
				os.execute("rm -f " .. cachePath .. "/" .. v .. "*")
			end
		end
		ftd:close()
	end
	msg.verbose("clear")
	mp.command("quit")
	--end
end
mp.add_hook("on_unload", 50, function()
	-- mp.abort_async_command(AudioDownloadHandle)
	-- mp.abort_async_command(VideoDownloadHandle)
	mp.abort_async_command(JsonDownloadHandle)
	mp.unregister_event(listener)
	caught = true
	listenID = "resetYtdlPreloadListener"
	-- print(listenID)
end)

local skipInitial
mp.observe_property("playlist-count", "number", function()
	if skipInitial then
		DL()
	else
		skipInitial = true
	end
end)

--from ytdl_hook
local platform_is_windows = (package.config:sub(1, 1) == "\\")
local o = {
	exclude = "",
	try_ytdl_first = false,
	use_manifests = false,
	all_formats = false,
	force_all_formats = true,
	ytdl_path = "",
}
local paths_to_search = { "yt-dlp", "yt-dlp_x86", "youtube-dl" }
--local options = require 'mp.options'
options.read_options(o, "ytdl_hook")

local separator = platform_is_windows and ";" or ":"
if o.ytdl_path:match("[^" .. separator .. "]") then
	paths_to_search = {}
	for path in o.ytdl_path:gmatch("[^" .. separator .. "]+") do
		table.insert(paths_to_search, path)
	end
end

local function exec(args)
	local ret = mp.command_native({
		name = "subprocess",
		args = args,
		capture_stdout = true,
		capture_stderr = true,
	})
	return ret.status, ret.stdout, ret, ret.killed_by_us
end

local command = {}
for _, path in pairs(paths_to_search) do
	-- search for youtube-dl in mpv's config dir
	local exesuf = platform_is_windows and ".exe" or ""
	local ytdl_cmd = mp.find_config_file(path .. exesuf)
	if ytdl_cmd then
		msg.verbose("Found youtube-dl at: " .. ytdl_cmd)
		ytdl = ytdl_cmd
		break
	else
		msg.verbose("No youtube-dl found with path " .. path .. exesuf .. " in config directories")
		--search in PATH
		command[1] = path
		es, json, result, aborted = exec(command)
		if result.error_string == "init" then
			msg.verbose("youtube-dl with path " .. path .. exesuf .. " not found in PATH or not enough permissions")
		else
			msg.verbose("Found youtube-dl with path " .. path .. exesuf .. " in PATH")
			ytdl = path
			break
		end
	end
end
--end ytdl_hook

if platform_is_windows then
	restrictFilenames = "--restrict-filenames"
end

mp.register_event("start-file", DL)
mp.register_event("shutdown", clearCache)
-- cleanup leftover temp files from previous session (guarded against missing dir/file)
do
	local ftd = io.open(cachePath .. "/temp.files", "r")
	if ftd then
		while true do
			local line = ftd:read()
			if line == nil or line == "" then
				ftd:close()
				local w = io.open(cachePath .. "/temp.files", "w")
				if w then w:close() end
				break
			end
			if package.config:sub(1, 1) ~= "/" then
				os.execute('del /Q /F "' .. cachePath .. "\\" .. line .. '*" >nul 2>nul')
			else
				os.execute("rm -f " .. cachePath .. "/" .. line .. "* &> /dev/null")
			end
		end
	end
end
