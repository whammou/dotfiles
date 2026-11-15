local M = {}

local applied = false

-- bloocky's own resolver takes every timed block that *overlaps* the hour, plus
-- every all-day block of the day, so <CR> offers all-day chores and week-long
-- spans beside the meetings the row is actually drawing. The cursor means the
-- hour it is on: the candidates are the timed blocks occupying that hour -- the
-- same set the row splits into -- and all-day blocks never enter that list.
--
-- When no block occupies the hour (or only a block that started earlier, like
-- 07:00 under a 06:00-18:00 block, which draws one cell and not a split row),
-- <CR> has nothing local to act on and falls back to the whole day, so a long
-- block is still reachable. Creating a block stays on `a`.
--
-- `hits_at_cursor` is file-local in ui.lua, but the two public functions built on
-- it are what the keymaps bind, so those are the seam.

-- Half-open interval test: showing in [s, e) iff it starts before e and ends after s.
local function occupy(day, minute)
	local s = minute
	local e = s + 60
	local out, starting = {}, 0
	for _, block in ipairs(day) do
		if not block.all_day and block.start_min and block.duration_min then
			if block.start_min < e and block.start_min + block.duration_min > s then
				table.insert(out, block)
				if block.start_min >= s then
					starting = starting + 1
				end
			end
		end
	end
	return out, starting
end

local function resolve(ui)
	local day = require("bloocky.state").blocks_for_date(ui.cursor.date)
	if ui.view == "month" then
		return day
	end
	local blocks, starting = occupy(day, ui.cursor.min)
	if starting == 0 and #blocks < 2 then
		return day
	end
	return blocks
end

local function pick(blocks, callback)
	if #blocks == 1 then
		callback(blocks[1])
		return
	end
	local utils = require("bloocky.utils")
	vim.ui.select(blocks, {
		prompt = "Which block?",
		format_item = function(block)
			if block.all_day then
				return "All day " .. block.title
			end
			return utils.format_hhmm(block.start_min) .. " " .. block.title
		end,
	}, function(choice)
		if choice then
			callback(choice)
		end
	end)
end

-- The window the dialog hands focus back to. The calendar window is current
-- while the key is being handled, so it needs no lookup inside the plugin.
local function return_win()
	return vim.api.nvim_get_current_win()
end

local function edit_block(ui)
	local state = require("bloocky.state")
	local blocks = resolve(ui)
	if #blocks == 0 then
		ui.add_block()
		return
	end
	local back = return_win()
	pick(blocks, function(block)
		require("bloocky.dialog").open({
			block = block,
			return_win = back,
			on_save = function(fields)
				state.update_block(block.id, fields)
				ui.render()
				ui.schedule_sync()
			end,
		})
	end)
end

local function delete_block(ui)
	local state = require("bloocky.state")
	local blocks = resolve(ui)
	if #blocks == 0 then
		vim.notify("Bloocky: no block in this slot", vim.log.levels.INFO)
		return
	end
	pick(blocks, function(block)
		local label = block.title
		-- vim.NIL, not just nil: a block written with an explicit
		-- `"recurrence": null` by another writer is still a one-off, and must
		-- not get the scary whole-series warning.
		if block.recurrence and block.recurrence ~= vim.NIL then
			label = label .. " (recurring — the whole series will be deleted)"
		end
		if vim.fn.confirm('Delete "' .. label .. '"?', "&Yes\n&No", 2) == 1 then
			state.delete_block(block.id)
			ui.render()
			ui.schedule_sync()
		end
	end)
end

function M.apply()
	if applied then
		return
	end
	applied = true

	local ok, ui = pcall(require, "bloocky.ui")
	if not ok then
		return
	end

	-- ui.lua binds these two into the buffer keymaps at open time, so replacing
	-- the fields before the first open is what takes effect.
	ui.edit_block = function()
		edit_block(ui)
	end
	ui.delete_block = function()
		delete_block(ui)
	end
end

return M
