-- org-priority.lua
-- Controls rendering of org priority cookies ([#A] [#B] [#C]) in pandoc PDF
-- export via the eisvogel template.
--
-- Reads #+OPTIONS: pri:  from the raw org file (pandoc consumes #+OPTIONS:
-- during parsing, so we read the source file directly).
--
-- Priority:
--   1. --metadata=pri:t|nil  (CLI override)
--   2. #+OPTIONS: pri:t|nil  in org file
--   3. Default: pri:t (always show)
--
-- pri=t / true / yes / on   → wrap in \orgpriority{LEVEL} colored markup
-- pri=nil / false / no / off → strip priority cookies from all headers
--
-- Also sets doc.meta["pri"] so the eisvogel template can use $if(pri)$
-- to define the \orgpriority command.
--
-- Usage: included via defaults/eisvogel.yaml → no action needed

local PRIORITY_PATTERN = "^%[#([A-C])%]$"

-- Truth table for priority values
local function is_truthy(val)
  if not val then return false end
  local s = val:lower()
  return not (s == "nil" or s == "false" or s == "no" or s == "off" or s == "" or s == "0")
end

--- Read the raw org file and extract #+OPTIONS: pri: value.
--- When piped through stdin (e.g. via eisvogel-pdf), PANDOC_STATE.input_files
--- is empty. In that case fallback to --metadata=org-source-file=<path> which
--- the wrapper script sets to the original filename.
local function read_pri_from_source(doc)
  local files = PANDOC_STATE.input_files

  -- When input is stdin, files contains {"-"} (not empty). Check if all
  -- entries are "-" (stdin indicator) so we fallback to metadata.
  local is_stdin = files and #files >= 1
  if is_stdin then
    for _, f in ipairs(files) do
      if f ~= "-" then is_stdin = false; break end
    end
  end

  if not files or #files == 0 or is_stdin then
    local src_meta = doc and doc.meta and doc.meta["org-source-file"]
    if src_meta then
      local fpath = pandoc.utils.stringify(src_meta)
      files = { fpath }
    else
      return nil
    end
  end

  for _, fpath in ipairs(files) do
    if fpath ~= "-" then
      local f, err = io.open(fpath, "r")
      if f then
        local content = f:read("*all")
        f:close()
        -- Search for #+OPTIONS: line containing pri:
        for line in content:gmatch("[^\r\n]+") do
          if line:match("^#%+OPTIONS:") then
            local pri_val = line:match("pri%s*:%s*(%S+)")
            if pri_val then
              return pri_val
            end
          end
        end
      end
    end
  end
  return nil
end

--- Determine the resolved pri behavior.
local function resolve_pri(doc)
  -- 1. Metadata override (command-line --metadata=pri:t)
  local meta_pri = doc.meta["pri"]
  if meta_pri then
    local s = pandoc.utils.stringify(meta_pri)
    return is_truthy(s), s
  end

  -- 2. Read raw source file for #+OPTIONS: pri:
  local src_pri = read_pri_from_source(doc)
  if src_pri then
    return is_truthy(src_pri), src_pri
  end

  -- 3. Default: pri:t (always show)
  return true, "t"
end

--- Process a header's inline list: strip priority tokens or wrap in LaTeX.
local function process_inlines(inlines, hide, use_markup)
  local result = {}
  local i = 1
  while i <= #inlines do
    local item = inlines[i]

    if item.t == "Str" then
      local level = item.text:match(PRIORITY_PATTERN)
      if level then
        if hide then
          -- Skip the priority Str and any trailing Space
          if i + 1 <= #inlines and inlines[i + 1].t == "Space" then
            i = i + 1
          end
          i = i + 1
          goto continue
        elseif use_markup then
          table.insert(
            result,
            pandoc.RawInline("latex", "\\orgpriority{" .. level .. "} ")
          )
          -- Skip trailing original space (badge emits its own)
          if i + 1 <= #inlines and inlines[i + 1].t == "Space" then
            i = i + 1
          end
          i = i + 1
          goto continue
        end
      end
    end

    table.insert(result, item)
    i = i + 1
    ::continue::
  end
  return result
end

function Pandoc(doc)
  local enabled = resolve_pri(doc)

  -- Process all Header blocks
  for _, blk in ipairs(doc.blocks) do
    if blk.t == "Header" then
      blk.content = process_inlines(blk.content, not enabled, enabled)
    end
  end

  -- Forward pri to template metadata for $if(pri)$ conditional.
  -- NOTE: Must completely remove the key when disabled. In pandoc templates,
  -- $if(pri)$ is falsy ONLY when the variable is absent/false. Setting it
  -- to MetaString("nil") is still a truthy string -- the \orgpriority
  -- command block would always be included.
  if enabled then
    doc.meta["pri"] = pandoc.MetaString("t")
  else
    doc.meta["pri"] = nil
  end

  return doc
end
