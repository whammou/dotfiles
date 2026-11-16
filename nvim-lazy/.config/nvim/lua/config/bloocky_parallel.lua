-- Parallel calendar pull for bloocky, applied at runtime.
--
-- The plugin pulls calendars one after another, so a sync with 26 subscribed
-- calendars waits on 26 network round trips in sequence (about 0.5 s each).
-- Wrapping the providers here starts every calendar at once on the first fetch
-- of a run; the plugin's sequential loop then reads finished results from a
-- cache. Nothing under lazy/bloocky is modified, so :Lazy update cannot drop
-- it, and the per-calendar error reporting stays with the plugin.

local M = {}

local async = require("bloocky.sync.async")
local oauth = require("bloocky.sync.oauth")
local providers = require("bloocky.sync.providers")
local store = require("bloocky.sync.store")

local WRAPPED = "bloocky_parallel_pull"

-- account id -> { [calendar href] = { result, err } } for the current run
local runs = {}
-- account id -> calendars reported by the last discover
local discovered = {}

local function subscribed(account, calendars)
	if not account.calendars or #account.calendars == 0 then
		return calendars
	end
	local out = {}
	for _, wanted in ipairs(account.calendars) do
		for _, calendar in ipairs(calendars) do
			local same = (wanted.href and wanted.href == calendar.href)
				or (wanted.name and calendar.name:lower() == wanted.name:lower())
			if same then
				table.insert(out, calendar)
				break
			end
		end
	end
	return out
end

local function fan_out(account, calendars, window, fetch)
	local results, pending, wake = {}, 0, nil
	-- One refresh before the fan-out: the token call is awaitable and a group
	-- of calendars racing it would spend the same refresh token in parallel.
	oauth.access_token(account)

	local function settle(calendar, result, err)
		results[calendar.href] = { result, err }
		pending = pending - 1
		if pending == 0 and wake then
			wake()
		end
	end

	for _, calendar in ipairs(calendars) do
		pending = pending + 1
		local cursor = store.calendar_cursor(account.id, calendar.href)
		local co = coroutine.create(function()
			local ok, result, err = pcall(fetch, account, calendar, cursor, window)
			if ok then
				settle(calendar, result, err)
			else
				settle(calendar, nil, tostring(result))
			end
		end)
		local resumed, err = coroutine.resume(co)
		if not resumed then
			settle(calendar, nil, tostring(err))
		end
	end

	if pending > 0 then
		async.await(function(cb)
			wake = cb
		end)
	end
	return results
end

function M.apply()
	for _, name in ipairs(providers.names()) do
		local ok, module = pcall(providers.for_account, { provider = name })
		if ok and module.discover and module.fetch and not module[WRAPPED] then
			local discover, fetch = module.discover, module.fetch
			module[WRAPPED] = true

			module.discover = function(account, ...)
				local calendars, err = discover(account, ...)
				discovered[account.id] = calendars
				runs[account.id] = nil
				return calendars, err
			end

			module.fetch = function(account, calendar, cursor, window)
				local results = runs[account.id]
				if not results then
					local calendars = subscribed(account, discovered[account.id] or {})
					if #calendars == 0 then
						return fetch(account, calendar, cursor, window)
					end
					results = fan_out(account, calendars, window, fetch)
					runs[account.id] = results
				end
				local hit = results[calendar.href]
				if not hit then
					return fetch(account, calendar, cursor, window)
				end
				results[calendar.href] = nil
				return hit[1], hit[2]
			end
		end
	end
	return M
end

return M
