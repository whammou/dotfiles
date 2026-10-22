-- Bulk actions for the org agenda buffer.
--
-- Visual-select any number of agenda entries, then:
--   <prefix>$    archive
--   <prefix>A    toggle ARCHIVE tag
--   <prefix>t    set tags (prompted once for the whole selection)
--   <prefix>+    priority up
--   <prefix>-    priority down
--   <prefix>T    cycle TODO state forwards
--   <prefix>id   set deadline (prompted once)
--   <prefix>is   set schedule (prompted once)
--
-- Entries are deduplicated by headline id (or file + title + start line)
-- because a headline can be rendered in several agenda views; without
-- deduplication a toggle would run twice and cancel itself out. Items are
-- applied bottom-up per file so earlier line numbers stay valid while the
-- buffer is edited.

local Promise = require("orgmode.utils.promise")
local Utils = require("orgmode.utils")

local M = {}

local function get_agenda()
  local ok, org = pcall(require, "orgmode")
  if not ok then
    return nil
  end
  local instance = org.instance()
  local agenda = instance and instance.agenda
  if not agenda or not agenda.views or #agenda.views == 0 then
    Utils.echo_warning("Not in an org agenda buffer")
    return nil
  end
  return agenda
end

local function selection_bounds()
  local start_line = vim.fn.line("v")
  local end_line = vim.fn.line(".")
  if start_line > end_line then
    start_line, end_line = end_line, start_line
  end
  return start_line, end_line
end

local function ref_key(ref)
  if ref.id and ref.id ~= "" then
    return ref.filename .. "|id:" .. ref.id
  end
  return ref.filename .. "|" .. ref.title .. "|" .. ref.start_line
end

local function collect(agenda)
  local start_line, end_line = selection_bounds()
  local seen = {}
  local refs = {}

  for _, view in ipairs(agenda.views) do
    local rendered = view.view
    local lines = rendered and view:get_lines() or nil

    -- Only touch the slice of the view that intersects the selection. A
    -- month/year view can hold thousands of lines; scanning all of them for
    -- every bulk action dominates runtime on large agendas.
    local first, last = 1, lines and #lines or 0
    if lines and rendered.start_line and rendered.end_line then
      if rendered.end_line - 1 < start_line or rendered.start_line > end_line then
        first, last = 1, 0
      else
        local offset = rendered.start_line - 1
        first = math.max(1, start_line - offset)
        last = math.min(#lines, end_line - offset)
      end
    end

    for i = first, last do
      local line = lines[i]
      local headline = line.headline
      if headline then
        local ref = line.headline_ref
        if not ref then
          ref = {
            filename = headline.file.filename,
            id = headline:get_property("id", false),
            title = headline:get_title(),
            start_line = headline:get_range().start_line,
          }
        end

        local key = ref_key(ref)
        if not seen[key] then
          seen[key] = true
          table.insert(refs, {
            filename = ref.filename,
            id = ref.id,
            title = ref.title,
            start_line = ref.start_line,
          })
        end
      end
    end
  end

  table.sort(refs, function(a, b)
    if a.filename ~= b.filename then
      return a.filename < b.filename
    end
    return a.start_line > b.start_line
  end)

  return refs
end

local function collect_and_leave(agenda)
  local refs = collect(agenda)
  pcall(vim.cmd, "normal! \27")
  return refs
end

local function build_resolver(file)
  local by_id, by_title = {}, {}

  for _, headline in ipairs(file:get_headlines()) do
    local id = headline:get_property("id", false)
    if id and id ~= "" then
      by_id[id] = headline
    end

    local title = headline:get_title()
    local bucket = by_title[title]
    if not bucket then
      bucket = {}
      by_title[title] = bucket
    end
    table.insert(bucket, headline)
  end

  return function(ref)
    if ref.id and ref.id ~= "" and by_id[ref.id] then
      return by_id[ref.id]
    end

    local bucket = by_title[ref.title]
    if bucket then
      if #bucket == 1 then
        return bucket[1]
      end
      local best, best_delta
      for _, headline in ipairs(bucket) do
        local delta = math.abs(headline:get_range().start_line - ref.start_line)
        if not best_delta or delta < best_delta then
          best, best_delta = headline, delta
        end
      end
      return best
    end

    for _, headline in ipairs(file:get_headlines()) do
      local range = headline:get_range()
      if range.start_line <= ref.start_line and ref.start_line <= range.end_line then
        return headline
      end
    end
  end
end

local function apply_refs(agenda, refs, opts)
  opts = opts or {}

  if #refs == 0 then
    Utils.echo_warning("No headlines in visual selection")
    return Promise.resolve()
  end

  if not opts.action and not opts.run then
    Utils.echo_warning("No action to apply")
    return Promise.resolve()
  end

  local Org = require("orgmode")
  local done, failed = 0, 0

  local groups, order = {}, {}
  for _, ref in ipairs(refs) do
    local group = groups[ref.filename]
    if not group then
      group = {}
      groups[ref.filename] = group
      table.insert(order, ref.filename)
    end
    table.insert(group, ref)
  end

  local function run_one(headline)
    vim.fn.cursor({ headline:get_range().start_line, 1 })

    local result
    if opts.action then
      result = Promise.resolve(Org.action(opts.action, opts.args))
    else
      result = Promise.resolve(opts.run(headline))
    end

    return result:next(function()
      return true
    end)
  end

  local chain = Promise.resolve()

  for _, filename in ipairs(order) do
    local group = groups[filename]
    chain = chain:next(function()
      local ok, file = pcall(agenda.files.get, agenda.files, filename)
      if not ok or not file then
        failed = failed + #group
        return
      end

      local done_before = done
      local ok_update, update = pcall(file.update, file, function()
        local resolve = build_resolver(file)
        local inner = Promise.resolve()

        for _, ref in ipairs(group) do
          inner = inner:next(function()
            local ok_resolve, headline = pcall(resolve, ref)
            if not ok_resolve or not headline then
              failed = failed + 1
              return
            end
            return run_one(headline):next(
              function()
                done = done + 1
              end,
              function()
                failed = failed + 1
              end
            )
          end)
        end

        return inner
      end)

      if not ok_update then
        failed = failed + (#group - (done - done_before))
        return
      end

      return Promise.resolve(update):next(function() end, function()
        failed = failed + (#group - (done - done_before))
      end)
    end)
  end

  return chain
    :next(function()
      return agenda:redo("agenda", true)
    end)
    :next(function()
      if done > 0 then
        Utils.echo_info(string.format(opts.message or "Applied to %d headlines", done))
      end
      if failed > 0 then
        Utils.echo_warning(string.format("%d headlines could not be updated", failed))
      end
    end)
end

local function apply_name_action(action, message)
  local agenda = get_agenda()
  if not agenda then
    return
  end
  return apply_refs(agenda, collect_and_leave(agenda), {
    action = action,
    message = message,
  })
end

---Apply an action from the `org_mappings` namespace to every selected entry.
---@param action_name string
---@param opts? { args?: any, message?: string }
function M.apply_action(action_name, opts)
  opts = opts or {}
  local agenda = get_agenda()
  if not agenda then
    return
  end
  return apply_refs(agenda, collect_and_leave(agenda), {
    action = action_name,
    args = opts.args,
    message = opts.message,
  })
end

function M.archive()
  return apply_name_action("org_mappings.archive", "Archived %d headlines")
end

function M.toggle_archive_tag()
  return apply_name_action("org_mappings.toggle_archive_tag", "Toggled ARCHIVE tag on %d headlines")
end

function M.todo_next_state()
  return apply_name_action("org_mappings.todo_next_state", "Cycled TODO state on %d headlines")
end

function M.priority_up()
  return apply_name_action("org_mappings.priority_up", "Raised priority on %d headlines")
end

function M.priority_down()
  return apply_name_action("org_mappings.priority_down", "Lowered priority on %d headlines")
end

---Prompt for tags once, then apply them to every selected entry.
function M.set_tags()
  local agenda = get_agenda()
  if not agenda then
    return
  end

  local refs = collect_and_leave(agenda)
  if #refs == 0 then
    Utils.echo_warning("No headlines in visual selection")
    return
  end

  local current = ""
  local headline = agenda:get_headline_at_cursor()
  if headline then
    local ok, own_tags = pcall(function()
      local tags = headline:get_own_tags()
      return tags
    end)
    if ok and own_tags then
      current = Utils.tags_to_string(own_tags)
    end
  end

  local Input = require("orgmode.ui.input")
  return Input.open("Tags: ", current, function(arg_lead)
    return Utils.prompt_autocomplete(arg_lead, agenda.files:get_tags())
  end):next(function(tags)
    if tags == nil then
      return
    end
    return apply_refs(agenda, refs, {
      action = "org_mappings.set_tags",
      args = tags,
      message = "Set tags on %d headlines",
    })
  end)
end

---Prompt for a deadline date once, then apply it to every selected entry.
function M.set_deadline()
  local agenda = get_agenda()
  if not agenda then
    return
  end

  local refs = collect_and_leave(agenda)
  if #refs == 0 then
    Utils.echo_warning("No headlines in visual selection")
    return
  end

  local Date = require("orgmode.objects.date")
  local Calendar = require("orgmode.objects.calendar")

  local date = Date.today()
  local headline = agenda:get_headline_at_cursor()
  if headline then
    local ok, current = pcall(function()
      return headline:get_deadline_date()
    end)
    if ok and current then
      date = current
    end
  end

  return Calendar.new({ date = date, clearable = true, title = "Set deadline" }):open():next(function(new_date, cleared)
    if cleared then
      return apply_refs(agenda, refs, {
        run = function(item)
          return item:remove_deadline_date()
        end,
        message = "Cleared deadline on %d headlines",
      })
    end
    if not new_date then
      return
    end
    return apply_refs(agenda, refs, {
      run = function(item)
        item:remove_closed_date()
        return item:set_deadline_date(new_date)
      end,
      message = "Set deadline on %d headlines",
    })
  end)
end

---Prompt for a scheduled date once, then apply it to every selected entry.
function M.set_schedule()
  local agenda = get_agenda()
  if not agenda then
    return
  end

  local refs = collect_and_leave(agenda)
  if #refs == 0 then
    Utils.echo_warning("No headlines in visual selection")
    return
  end

  local Date = require("orgmode.objects.date")
  local Calendar = require("orgmode.objects.calendar")

  local date = Date.today()
  local headline = agenda:get_headline_at_cursor()
  if headline then
    local ok, current = pcall(function()
      return headline:get_scheduled_date()
    end)
    if ok and current then
      date = current
    end
  end

  return Calendar.new({ date = date, clearable = true, title = "Set schedule" }):open():next(function(new_date, cleared)
    if cleared then
      return apply_refs(agenda, refs, {
        run = function(item)
          return item:remove_scheduled_date()
        end,
        message = "Cleared schedule on %d headlines",
      })
    end
    if not new_date then
      return
    end
    return apply_refs(agenda, refs, {
      run = function(item)
        item:remove_closed_date()
        return item:set_scheduled_date(new_date)
      end,
      message = "Set schedule on %d headlines",
    })
  end)
end

function M.attach(bufnr)
  bufnr = bufnr or vim.api.nvim_get_current_buf()

  local ok, config = pcall(require, "orgmode.config")
  local prefix = ok and config.opts.mappings.prefix or "<Leader>o"

  local opts = { buffer = bufnr, silent = true, nowait = true }
  local function map(lhs, fn, desc)
    local map_opts = vim.tbl_extend("force", opts, { desc = desc })
    vim.keymap.set("x", lhs, fn, map_opts)
  end

  map(prefix .. "$", function()
    M.archive()
  end, "Org bulk archive")
  map(prefix .. "A", function()
    M.toggle_archive_tag()
  end, "Org bulk toggle ARCHIVE tag")
  map(prefix .. "t", function()
    M.set_tags()
  end, "Org bulk set tags")
  map(prefix .. "+", function()
    M.priority_up()
  end, "Org bulk priority up")
  map(prefix .. "-", function()
    M.priority_down()
  end, "Org bulk priority down")
  map(prefix .. "T", function()
    M.todo_next_state()
  end, "Org bulk cycle TODO")
  map(prefix .. "id", function()
    M.set_deadline()
  end, "Org bulk set deadline")
  map(prefix .. "is", function()
    M.set_schedule()
  end, "Org bulk set schedule")
end

M._collect = collect
M._apply_refs = apply_refs

return M
