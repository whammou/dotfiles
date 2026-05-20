ps.sub("ind-app-title", function(args)
	args.value = tostring(cx.active.current.cwd) .. " - yazi"
	return args
end)

local orange = "#DD9046"

th.git = th.git or {}
th.git.modified = ui.Style():fg(orange):bold() --orange
th.git.deleted = ui.Style():fg("red"):bold()
th.git.added = ui.Style():fg("green"):bold()
th.git = th.git or {}
th.git.modified_sign = ""
th.git.deleted_sign = "✖"
th.git.added_sign = "✚"

require("git"):setup({
	order = 1500,
})

require("starship"):setup()
require("mime-ext"):setup({
	with_exts = {
		org = "text/org",
		target = "text/x-systemd-unit",
		service = "text/x-systemd-unit",
		timer = "text/x-systemd-unit",
	},
})

--require("gvfs"):setup({
--	which_keys = "1234567890qwertyuiopasdfghjklzxcvbnm-=[]\\;',./!@#$%^&*()_+{}|:\"<>?",
--	blacklist_devices = { { name = "Wireless Device", scheme = "mtp" }, { scheme = "file" }, "Device Name" },
--	save_path = os.getenv("HOME") .. "/.config/yazi/gvfs.private",
--	input_position = { "center", y = 0, w = 60 },
--	password_vault = "keyring",
--	key_grip = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
--	save_password_autoconfirm = true,
--})
