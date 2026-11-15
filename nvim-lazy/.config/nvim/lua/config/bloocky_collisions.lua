local M = {}

local applied = false

-- bloocky renders an hour slot as one line of text and picks a single block for
-- it: `occ_at` in views/day.lua returns the earliest-starting match plus a count,
-- and the count is all you ever see (" (+2)"). The other events are not drawn
-- anywhere, so a slot with three meetings reads as one meeting and a number.
--
-- A slot has `cwidth` cells and nothing else is using them, so collisions are
-- laid out as real side-by-side columns: the cell is split across the blocks
-- that intersect the row, one column each, separated by the grid bar. Slots with
-- zero or one block keep bloocky's own output byte for byte.
--
-- `occ_at` is a file-local in the view, so the seam is the module's `render`
-- field: ui.lua holds the same module table and dispatches through it.

-- Narrower than icon + "09:30 " + a title, a column shows slivers, so the slot
-- packs differently instead.
local MIN_COL = 10

-- Narrower than this a column cannot carry icon, start time and enough of a
-- title to tell two events apart, which is the whole point of splitting a slot.
-- Below it the slot stacks vertically instead of splitting.
local LEGIBLE = 16

-- Rows the all-day section keeps when it competes with the hour grid for height.
-- Stacking a slot costs lines, and those lines come from somewhere.
local MIN_TOP = 2

-- Every block intersecting [row_s, row_e), in the order state.blocks_for_date
-- sorted them: all-day first, then by start_min.
local function occ_all(blocks, row_s, row_e)
	local out = {}
	for _, block in ipairs(blocks) do
		if block.start_min < row_e and (block.start_min + block.duration_min) > row_s then
			table.insert(out, block)
		end
	end
	return out
end

local function spans_at(block, min)
	return block.start_min < min and (block.start_min + block.duration_min) > min
end

-- Column widths for a slot, or nil when the cell is too narrow to split. The
-- separator cells come out of the budget first, so columns cover cwidth exactly.
local function columns(cwidth, n)
	if n <= 1 then
		return { cwidth }
	end
	local usable = cwidth - (n - 1)
	if usable < n * MIN_COL then
		return nil
	end
	return require("bloocky.utils").share(usable, n)
end

-- One group per column, and never the same one twice in a row. bloocky picks a
-- block's colour from its calendar or from a hash of its id, so unrelated events
-- routinely share a palette entry -- and a split slot then reads as one wide bar
-- in one colour, which is what makes collisions unreadable in the first place.
-- The palette cannot separate more events than it has entries, so past that the
-- rotation gives up and repeats.
local function slot_groups(ncols, slot)
	local highlights = require("bloocky.highlights")
	local groups, used = {}, {}
	for i = 1, ncols do
		local block = slot[i]
		local group = block and highlights.block_group(block) or nil
		local index = group and tonumber(group:match("^BloockyBlock(%d+)$"))
		if index then
			for _ = 1, highlights.palette_size do
				if not used[group] then
					break
				end
				index = index % highlights.palette_size + 1
				group = "BloockyBlock" .. index
			end
		end
		if group then
			used[group] = true
		end
		groups[i] = group
	end
	return groups
end

-- Compact label for a collision column: start time plus title. The full
-- "start–end title (duration)" form does not survive a quarter-width cell, and
-- the end time is on the block's last row anyway. A block that began on an
-- earlier row keeps its title, so every row of a column identifies itself
-- instead of reading as an anonymous bar.
local function column_text(block, row_s, cfg)
	if block.start_min < row_s then
		return require("bloocky.marks").icon(block) .. " " .. block.title
	end
	local text = require("bloocky.marks").icon(block)
		.. require("bloocky.utils").format_hhmm(block.start_min)
		.. " "
		.. block.title
	if block.recurrence then
		text = text .. " " .. cfg.icons.recurring
	end
	return text
end

-- bloocky's original single-block label, unchanged so non-colliding slots look
-- exactly as they did before this patch.
local function single_text(block, row_s, cfg)
	local utils = require("bloocky.utils")
	if block.start_min < row_s then
		return require("bloocky.marks").icon(block)
	end
	local text = require("bloocky.marks").icon(block)
		.. utils.format_hhmm(block.start_min)
		.. "–"
		.. utils.format_hhmm(block.start_min + block.duration_min)
		.. " "
		.. block.title
		.. " ("
		.. utils.format_duration(block.duration_min)
		.. ")"
	if block.recurrence then
		text = text .. " " .. cfg.icons.recurring
	end
	if block.notes and block.notes ~= "" then
		text = text .. " — " .. block.notes:gsub("\n", " ")
	end
	return text
end

-- A stacked slot gives each live event a whole line, so the start time fits even
-- when the end time and duration do not. A block that began earlier names itself
-- without repeating the time.
local function stacked_text(block, row_s, cfg)
	if block.start_min < row_s then
		return require("bloocky.marks").icon(block) .. " " .. block.title
	end
	return single_text(block, row_s, cfg)
end

-- Greedy interval-graph colouring over the day's blocks, which state sorts by
-- start time. A block takes the first column whose last block has already
-- finished, and a run of overlapping blocks forms a cluster whose width is the
-- most columns it needed. Widths therefore stay fixed for the whole cluster:
-- the bars do not jump between one hour row and the next.
local function assign_columns(blocks)
	local layout = {}
	local cluster, column_end, cluster_end = {}, {}, nil
	local clusters = 0

	local function flush()
		if #cluster == 0 then
			return
		end
		local cols = 0
		for _, member in ipairs(cluster) do
			cols = math.max(cols, member.col + 1)
		end
		clusters = clusters + 1
		for _, member in ipairs(cluster) do
			layout[member.block] = { col = member.col, cols = cols, cluster = clusters }
		end
		cluster, column_end, cluster_end = {}, {}, nil
	end

	for _, block in ipairs(blocks) do
		local start_min = block.start_min
		local end_min = start_min + block.duration_min
		if cluster_end ~= nil and start_min >= cluster_end then
			flush()
		end
		cluster_end = cluster_end and math.max(cluster_end, end_min) or end_min

		local col = 1
		while column_end[col] and column_end[col] > start_min do
			col = col + 1
		end
		column_end[col] = end_min
		table.insert(cluster, { block = block, col = col - 1 })
	end
	flush()

	return layout
end

function M.render(ctx)
	local utils = require("bloocky.utils")
	local state = require("bloocky.state")
	local dooing = require("bloocky.dooing")
	local highlights = require("bloocky.highlights")
	local marks = require("bloocky.marks")

	local cfg = ctx.config
	local gutter = 8 -- " 05:00 │"
	local cwidth = ctx.width - gutter

	local lines, hls = {}, {}
	local meta = { width = ctx.width }

	local function push(chunks)
		local line, line_hls, spans = utils.compose(chunks)
		table.insert(lines, line)
		local lnum = #lines - 1
		for _, h in ipairs(line_hls) do
			h.line = lnum
			table.insert(hls, h)
		end
		return lnum, spans
	end

	local date = ctx.cursor.date
	local date_str = utils.date_to_str(date)
	-- All-day blocks never enter the hour grid; they get their own section.
	local all_day, blocks = state.split_for_date(date)
	local tasks = dooing.tasks_for_date(date_str)

	-- Everything above the hour grid is collected first: it only gets the rows
	-- the grid does not need, so the whole day always stays on screen.
	local h0, h1 = cfg.hours.start, cfg.hours["end"]
	local top = {}
	local function add(chunks)
		table.insert(top, chunks)
	end

	-- All-day section: a date, not a time, so it cannot be placed on an hour
	if #all_day > 0 then
		add({ { " " .. cfg.icons.all_day .. " All day", "BloockyHeader" } })
		local max_shown = 4
		for i, block in ipairs(all_day) do
			if i > max_shown then
				add({ { "    +" .. (#all_day - max_shown) .. " more", "BloockyMore" } })
				break
			end
			local text = "    " .. marks.icon(block) .. " " .. block.title
			local days = math.ceil((block.duration_min or 1440) / 1440)
			if days > 1 then
				text = text .. "  (" .. days .. " days)"
			end
			add({ { utils.fit(text, ctx.width), highlights.block_group(block), 100 } })
		end
		add({ { string.rep("─", ctx.width), "BloockyGrid" } })
	end

	-- Dooing deadline section
	if #tasks > 0 then
		add({ { " " .. cfg.icons.dooing .. " Due this day", "BloockyHeader" } })
		local max_tasks = 4
		for i, todo in ipairs(tasks) do
			if i > max_tasks then
				add({ { "    +" .. (#tasks - max_tasks) .. " more", "BloockyMore" } })
				break
			end
			local text = "    " .. cfg.icons.dooing .. " " .. todo.text
			if todo.estimated_hours then
				text = text .. "  (≈" .. todo.estimated_hours .. "h)"
			end
			if todo.priorities and type(todo.priorities) == "table" and #todo.priorities > 0 then
				text = text .. "  [" .. table.concat(todo.priorities, ", ") .. "]"
			end
			local grp = "BloockyDooing"
			if todo.done then
				grp = "BloockyDooingDone"
			elseif date_str < utils.date_to_str(ctx.today) then
				grp = "BloockyDooingOverdue"
			end
			add({ { utils.truncate(text, ctx.width), grp } })
		end
		add({ { string.rep("─", ctx.width), "BloockyGrid" } })
	end

	-- Hour grid
	local layout = assign_columns(blocks)
	local rows = utils.hour_layout(h0, h1, math.max(1, ctx.height - #top), ctx.fill)

	-- A cluster whose columns would be too narrow to name their events stacks
	-- instead: one live event per line, full cell width. Deciding per cluster
	-- rather than per row keeps a cluster from alternating between side by side
	-- and stacked as the hours pass, which is what made crowded days unreadable.
	local stack, need, demand, strip_dividers = {}, {}, 0, false
	do
		local order, cols_of = {}, {}
		for _, block in ipairs(blocks) do
			local info = layout[block]
			if info and not cols_of[info.cluster] then
				cols_of[info.cluster] = info.cols
				table.insert(order, info.cluster)
			end
		end
		for _, id in ipairs(order) do
			local widths = columns(cwidth, cols_of[id])
			if cols_of[id] > 1 and (not widths or widths[1] < LEGIBLE) then
				stack[id] = true
			end
		end

		local function engaged()
			for _, on in pairs(stack) do
				if on then
					return true
				end
			end
			return false
		end

		local function measure()
			local total, divs = 0, 0
			local rule = not engaged()
			for i, row in ipairs(rows) do
				local live = occ_all(blocks, row.s, row.e)
				local count = math.max(1, row.lines or 1)
				for _, block in ipairs(live) do
					local info = layout[block]
					if info and stack[info.cluster] then
						count = #live
						break
					end
				end
				need[i] = math.max(count, row.lines or 1)
				total = total + need[i]
				if row.div and rule then
					divs = divs + 1
				end
			end
			return total + divs
		end

		demand = measure()
		-- Stacking spends height, so it has to give some back when the day is
		-- tall: shed whichever cluster saves the most lines until the grid fits
		-- above the all-day floor.
		local floor = math.min(#top, MIN_TOP)
		while demand > ctx.height - floor do
			local worst, saved = nil, 0
			for _, id in ipairs(order) do
				if stack[id] then
					local flat, tall = 0, 0
					for _, row in ipairs(rows) do
						local count = 0
						for _, block in ipairs(occ_all(blocks, row.s, row.e)) do
							if layout[block] and layout[block].cluster == id then
								count = count + 1
							end
						end
						if count > 0 then
							flat = flat + 1
							tall = tall + count
						end
					end
					if tall - flat > saved then
						worst, saved = id, tall - flat
					end
				end
			end
			if not worst then
				break
			end
			stack[worst] = false
			demand = measure()
		end
		strip_dividers = engaged()
	end

	-- Trim the top sections down to what the grid leaves
	local budget = math.max(0, ctx.height - demand)
	if #top > budget then
		local keep = math.max(0, budget - 1)
		local hidden = #top - keep
		for i = #top, keep + 1, -1 do
			table.remove(top, i)
		end
		if budget > 0 then
			add({ { "    +" .. hidden .. " more above", "BloockyMore" } })
		end
	end
	for _, chunks in ipairs(top) do
		push(chunks)
	end

	-- One hour row as side-by-side columns
	local function render_columns(row, intersecting)
		local row_s, row_e = row.s, row.e

		-- A row can hold blocks from more than one cluster, so the row is as wide
		-- as the widest cluster touching it.
		local ncols = 1
		for _, block in ipairs(intersecting) do
			ncols = math.max(ncols, (layout[block] or {}).cols or 1)
		end

		-- Column index within the cluster, so bars stay put from row to row.
		-- `ncols` rather than #slot, so a gap or an empty slot still gets a cell.
		local widths = columns(cwidth, ncols)
		local slot = {}
		if widths then
			for _, block in ipairs(intersecting) do
				slot[((layout[block] or {}).col or 0) + 1] = block
			end
		else
			-- The cluster is taller than this cell can afford. Pack only what is
			-- live in this row: a block spanning most of the day would otherwise
			-- drag every row it touches down to slivers, and rows holding a
			-- single event would show a count instead of that event.
			ncols = #intersecting
			widths = columns(cwidth, ncols)
			if widths then
				for _, block in ipairs(intersecting) do
					table.insert(slot, block)
				end
			end
		end
		if not widths then
			ncols = 1
			slot = { intersecting[1] }
			widths = { cwidth }
		end

		local groups = slot_groups(ncols, slot)

		local function cell_chunks(i, r)
			local block = slot[i]
			local w = widths[i]
			if not block then
				return { string.rep(" ", w) }
			end
			if r > 1 then
				-- A tall slot keeps its label on the first line; the rest carries
				-- the block's colour on so it reads as one bar
				return { string.rep(" ", w), groups[i], 100 }
			end
			local text
			if ncols > 1 then
				text = column_text(block, row_s, cfg)
			elseif #intersecting > 1 then
				-- Too narrow to split. bloocky appends "(+N)", which utils.fit
				-- truncates away at exactly these widths, so it leads instead.
				text = "+" .. (#intersecting - 1) .. " " .. column_text(block, row_s, cfg)
			else
				text = single_text(block, row_s, cfg)
			end
			return { utils.fit(text, w), groups[i], 100 }
		end

		local on_cursor = ctx.cursor.min >= row_s and ctx.cursor.min < row_e
		for r = 1, row.lines do
			local chunks = {
				{ (r == 1) and row.label or string.rep(" ", gutter - 1), (r == 1) and "BloockyTime" or nil },
				{ "│", "BloockyGrid" },
			}
			for i = 1, ncols do
				if i > 1 then
					table.insert(chunks, { "│", "BloockyGrid" })
				end
				table.insert(chunks, cell_chunks(i, r))
			end
			local lnum, spans = push(chunks)
			if on_cursor then
				-- The body is every chunk past the gutter and its bar
				local span = { s = spans[3].s, e = spans[#spans].e }
				table.insert(hls, { line = lnum, s = span.s, e = span.e, group = "BloockyCursor", prio = 200 })
				meta.cursor_line = meta.cursor_line or (lnum + 1)
			end
		end

		-- Dotted divider between hours; blocks spanning the boundary stay solid.
		-- It reuses this row's columns so the bars line up with the block above.
		if row.div and not strip_dividers then
			local chunks = {
				{ string.rep(" ", gutter - 1) },
				{ "│", "BloockyGrid" },
			}
			for i = 1, ncols do
				if i > 1 then
					table.insert(chunks, { "│", "BloockyGrid" })
				end
				local block = slot[i]
				local w = widths[i]
				if block and spans_at(block, row_e) then
					table.insert(chunks, { string.rep(" ", w), groups[i], 100 })
				else
					table.insert(chunks, { string.rep("┄", w), "BloockyGrid" })
				end
			end
			push(chunks)
		end
	end

	-- One hour row as a stack, one live event per line
	local function render_stacked(row, intersecting, count)
		local row_e = row.e
		local on_cursor = ctx.cursor.min >= row.s and ctx.cursor.min < row_e
		for r = 1, count do
			local block = intersecting[r]
			local chunks = {
				{ (r == 1) and row.label or string.rep(" ", gutter - 1), (r == 1) and "BloockyTime" or nil },
				{ "│", "BloockyGrid" },
			}
			if block then
				local text = utils.fit(stacked_text(block, row.s, cfg), cwidth)
				table.insert(chunks, { text, highlights.block_group(block), 100 })
			else
				table.insert(chunks, { string.rep(" ", cwidth) })
			end
			local lnum, spans = push(chunks)
			if on_cursor then
				local span = { s = spans[3].s, e = spans[#spans].e }
				table.insert(hls, { line = lnum, s = span.s, e = span.e, group = "BloockyCursor", prio = 200 })
				meta.cursor_line = meta.cursor_line or (lnum + 1)
			end
		end

		-- The divider is one cell here, so it stays solid while any live event
		-- continues past the hour, in the colour of the first one that does.
		if row.div and not strip_dividers then
			local spanning
			for _, block in ipairs(intersecting) do
				if spans_at(block, row_e) then
					spanning = block
					break
				end
			end
			local chunks = {
				{ string.rep(" ", gutter - 1) },
				{ "│", "BloockyGrid" },
			}
			if spanning then
				table.insert(chunks, { string.rep(" ", cwidth), highlights.block_group(spanning), 100 })
			else
				table.insert(chunks, { string.rep("┄", cwidth), "BloockyGrid" })
			end
			push(chunks)
		end
	end

	for i, row in ipairs(rows) do
		local intersecting = occ_all(blocks, row.s, row.e)
		local stacked
		for _, block in ipairs(intersecting) do
			local info = layout[block]
			if info and stack[info.cluster] then
				stacked = true
				break
			end
		end
		if stacked then
			render_stacked(row, intersecting, need[i])
		else
			render_columns(row, intersecting)
		end
	end
	meta.title = string.format(
		" 󰃭 %s, %s %02d %d — Day ",
		utils.WDAYS_LONG[utils.wday(date)],
		utils.MONTHS[date.month],
		date.day,
		date.year
	)
	return lines, hls, meta
end

function M.apply()
	if applied then
		return
	end
	applied = true

	local day = require("bloocky.views.day")
	day.render = M.render
end

return M
