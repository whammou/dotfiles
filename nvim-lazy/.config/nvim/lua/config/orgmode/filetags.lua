-- filetags.lua — Interactive filetags search + Auto-FILETAGS inference
-- Use `OrgFiletags` command or `<leader>oF` to find files by `#+FILETAGS:`.
-- Requires fzf-lua to be installed (comes with fzf-org.nvim).
--
-- Auto-FILETAGS: a compile hook (registered by monkey-patching Template.new)
-- injects or replaces the `#+FILETAGS:` line at capture time, after the
-- target path is fully resolved (including user-chosen topic). The hook
-- calls combine() with the resolved path to determine the correct tags.

---@diagnostic disable: undefined-global

local M = {}

-- Hook: inject or replace `#+FILETAGS:` line using the resolved capture
-- target. Runs as an on_compile hook for `content_type == "content"`,
-- at which point `self.target` already holds the fully resolved file path
-- (see Template:compile() — target is compiled first, then content).
-- Also sets `whole_file = true` when the target doesn't exist yet, so the
-- full preamble (FILETAGS, OPTIONS, TODO) is used to create the new file
-- instead of only refiling the captured headline.
local function inject_filetags_hook(self, content, content_type)
  if content_type ~= "content" then
    return content
  end

  -- For new files, ensure the entire compiled template becomes the file content
  if self.target and vim.fn.filereadable(vim.fn.expand(self.target)) == 0 then
    self.whole_file = true
  end

  local filetags = M.combine(self.target)
  if not filetags then
    return content
  end

  local filetags_line = "#+FILETAGS: " .. filetags

  if content:match("#%+FILETAGS:") then
    return content:gsub("#%+FILETAGS: [^\n]*", filetags_line)
  end

  -- No existing FILETAGS — insert after #+TODO: line, or else prepend
  local _, after_todo = content:match("()#%+TODO: [^\n]*")
  if after_todo then
    local before = content:sub(1, after_todo)
    local after = content:sub(after_todo + 1)
    return before .. "\n" .. filetags_line .. after
  end

  return filetags_line .. "\n" .. content
end

-- Monkey-patch Template.new so every capture/roam template gets our hook.
-- The hook runs during `_compile()` AFTER dates are resolved but BEFORE
-- expansions/expressions/prompts. At this point, `self.target` is already
-- the fully resolved file path (for content_type == "content").
do
  local patched = false
  local function try_patch()
    if patched then
      return
    end
    local ok, Template = pcall(require, "orgmode.capture.template")
    if ok and Template then
      local orig_new = Template.new
      Template.new = function(cls, opts)
        local t = orig_new(cls, opts)
        t:on_compile(function(content, content_type)
          return inject_filetags_hook(t, content, content_type)
        end)
        return t
      end
      patched = true
    end
  end
  try_patch()
  if not patched then
    vim.schedule(try_patch)
  end
end

-- Path → FILETAGS rules.
local rules = {
  -- Capture templates: subdirectory-prefixed paths
  { pattern = "/dev/bug%.org$",        tags = ":typDev:catBug:" },
  { pattern = "/dev/issue%.org$",      tags = ":typDev:catIssue:" },
  { pattern = "/dev/enhancement%.org$", tags = ":typDev:catEnhancement:" },
  { pattern = "/dev/refactor%.org$",   tags = ":typDev:catRefactor:" },
  { pattern = "/milestones/major%.org$", tags = ":typMilestone:catMajor:" },
  { pattern = "/milestones/minor%.org$", tags = ":typMilestone:catMinor:" },
  { pattern = "/tasks/oneoff%.org$",   tags = ":typTask:catOneoff:" },
  { pattern = "/tasks/incidental%.org$", tags = ":typTask:catIncidental:" },
  { pattern = "/tasks/coordinated%.org$", tags = ":typTask:catCoordinated:" },
  { pattern = "/tasks/planned%.org$",  tags = ":typTask:catPlanned:" },
  { pattern = "/tasks/recurring%.org$", tags = ":typTask:catRecurring:" },
  { pattern = "/lists/purchase%.org$", tags = ":typList:catPurchase:" },
  { pattern = "/lists/location%.org$", tags = ":typList:catLocation:" },
  { pattern = "/draft%.org$",          tags = ":typDoc:catDraft:" },
  { pattern = "/capture%.org$",        tags = ":typJournal:catCapture:" },
  -- Roam templates: filename-only paths (less specific)
  { pattern = "/bug%.org$",            tags = ":typDev:catBug:" },
  { pattern = "/issue%.org$",          tags = ":typDev:catIssue:" },
  { pattern = "/enhancement%.org$",    tags = ":typDev:catEnhancement:" },
  { pattern = "/refactor%.org$",       tags = ":typDev:catRefactor:" },
  { pattern = "/minor%.org$",          tags = ":typMilestone:catMinor:" },
  { pattern = "/major%.org$",          tags = ":typMilestone:catMajor:" },
}

--- Infer filetags from a capture target path string.
--- The path may still contain `%^{...}` prompt placeholders — the static
--- suffix is sufficient for disambiguation.
--- @param target_path string
--- @return string|nil  e.g. ":typDev:catBug:", or nil when no rule matches
function M.infer(target_path)
  if not target_path then
    return nil
  end
  for _, r in ipairs(rules) do
    if target_path:match(r.pattern) then
      return r.tags
    end
  end
  return nil
end

--- Format a hypenated topic name into `topX@subY` style.
--- "teaching-course-en101" → "topTeaching@subCourse@subEn101"
local function format_topic(raw)
  local parts = vim.split(raw, "-")
  for i, part in ipairs(parts) do
    local prefix = i == 1 and "top" or "sub"
    parts[i] = prefix .. part:sub(1, 1):upper() .. part:sub(2)
  end
  return table.concat(parts, "@")
end

--- Infer a topics tag from the target path.
--- @param target_path string
--- @return string|nil  e.g. "topTeaching@subCourse", or nil when no topics match
function M.infer_topic(target_path)
  if not target_path then
    return nil
  end

  -- Case 1: full path with /topics/<topic>/
  local topic = target_path:match("/topics/([^/|]+)")
  if topic then
    return format_topic(topic)
  end

  -- Case 2: relative path prefixed with "topics/"
  local topic = target_path:match("^topics/([^/]+)")
  if topic then
    return format_topic(topic)
  end

  -- Case 3: relative path where first component IS the topic name
  local first = target_path:match("^([^/]+)/")
  if first then
    return format_topic(first)
  end

  return nil
end

--- Combine all tag sources (topic + type) into a single FILETAGS value.
--- @param target_path string
--- @return string|nil  e.g. ":topOPSYS:typDev:catIssue:", or nil if nothing matches
function M.combine(target_path)
  local topic = M.infer_topic(target_path)
  local typ = M.infer(target_path)

  if not topic and not typ then
    return nil
  end

  local parts = {}
  if topic then
    table.insert(parts, topic)
  end
  if typ then
    local inner = typ:match("^:(.+):$")
    if inner then
      for tag in inner:gmatch("[^:]+") do
        table.insert(parts, tag)
      end
    end
  end

  return ":" .. table.concat(parts, ":") .. ":"
end

--- Wrap a template string. The actual FILETAGS injection is handled at
--- capture time by `inject_filetags_hook` (registered via the monkey-patched
--- Template.new). This function is kept as a no-op for backward compatibility
--- with existing callers in templates.lua.
--- @param template_text string  The original template content (unchanged)
--- @return string  The template as-is
function M.wrap_template(template_text)
  return template_text
end

local function OrgFiletags(query)
  local orgmode = require('orgmode')
  local items = {}

  -- Collect files with their filetags (uses internal OrgFile API directly)
  for _, file in ipairs(orgmode.files:all()) do
    if not file:is_archive_file() then
      local filetags = file:get_filetags()
      if #filetags > 0 then
        local title = file:get_title() or vim.fn.fnamemodify(file.filename, ':t:r')
        local tags_str = ':' .. table.concat(filetags, ':') .. ':'
        -- Encode: filepath|display text (| is the delimiter for fzf display)
        table.insert(items, file.filename .. '|' .. title .. '  ' .. tags_str)
      end
    end
  end

  if #items == 0 then
    vim.notify('No files with #+FILETAGS found', vim.log.levels.INFO)
    return
  end

  -- Set up fzf_opts: if a query was given directly (e.g. `:OrgFiletags +project`),
  -- pre-fill the FZF search box with it
  local fzf_opts = {
    ['--delimiter'] = '|',
    ['--with-nth'] = '2..',
  }
  if query and query ~= '' then
    fzf_opts['--query'] = query
  end

  require('fzf-lua').fzf_exec(items, {
    prompt = 'Filetags> ',
    fzf_opts = fzf_opts,
    actions = {
      ['default'] = function(selected)
        if selected and selected[1] then
          local path = selected[1]:match('^(.-)|')
          if path then
            vim.cmd('edit ' .. vim.fn.fnameescape(path))
          end
        end
      end,
    },
  })
end

M.OrgFiletags = OrgFiletags

return M
