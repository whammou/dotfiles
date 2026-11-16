local M = {}

-- Same groups orgmode itself uses for emphasis inside the buffer
-- (lua/orgmode/colors/highlighter/markup/emphasis.lua), so table cells and
-- ordinary paragraphs render markup identically.
local MARKUP = {
  ['='] = '@org.verbatim',
  ['~'] = '@org.code',
  ['*'] = '@org.bold',
  ['/'] = '@org.italic',
  ['_'] = '@org.underline',
  ['+'] = '@org.strikethrough',
}

local PRE = {
  [' '] = true,
  ['('] = true,
  ['-'] = true,
  ["'"] = true,
  ['"'] = true,
  ['{'] = true,
  ['*'] = true,
  ['/'] = true,
  ['_'] = true,
  ['+'] = true,
}
local POST = {
  [' '] = true,
  [')'] = true,
  ['-'] = true,
  ['}'] = true,
  ['"'] = true,
  ["'"] = true,
  [':'] = true,
  [';'] = true,
  ['!'] = true,
  ['\\'] = true,
  ['['] = true,
  [','] = true,
  ['.'] = true,
  ['?'] = true,
  ['*'] = true,
  ['/'] = true,
  ['_'] = true,
  ['+'] = true,
}

local function is_open_boundary(prev)
  return prev == nil or PRE[prev] == true
end

local function is_close_boundary(nxt)
  return nxt == nil or POST[nxt] == true
end

local function push(segments, text, hl)
  if text == '' then
    return
  end
  local last = segments[#segments]
  if last and last.hl == hl then
    last.text = last.text .. text
    return
  end
  segments[#segments + 1] = { text = text, hl = hl }
end

---@param text string
---@return OrgInlineSegment[]
function M.segments(text)
  local segments = {}
  if text == nil or text == '' then
    return segments
  end

  local chars = vim.fn.split(text, [[\zs]])
  local index = 1
  while index <= #chars do
    local char = chars[index]
    local hl = MARKUP[char]
    local close = nil
    local opens = hl
      and is_open_boundary(chars[index - 1])
      and chars[index + 1] ~= nil
      and not chars[index + 1]:match('%s')
    if opens then
      local scan = index + 2
      while scan <= #chars do
        if
          chars[scan] == char
          and not chars[scan - 1]:match('%s')
          and is_close_boundary(chars[scan + 1])
        then
          close = scan
          break
        end
        scan = scan + 1
      end
    end
    if close then
      push(segments, table.concat(chars, '', index + 1, close - 1), hl)
      index = close + 1
    else
      push(segments, char, nil)
      index = index + 1
    end
  end
  return segments
end

---@param segments OrgInlineSegment[]
---@return string
function M.plain(segments)
  local parts = {}
  for _, segment in ipairs(segments or {}) do
    parts[#parts + 1] = segment.text
  end
  return table.concat(parts)
end

---@param chars table[]
---@param width integer
---@return table[]
local function pieces(chars, width)
  local result = {}
  local piece = {}
  local piece_width = 0
  for _, char in ipairs(chars) do
    local char_width = vim.fn.strdisplaywidth(char.c)
    if piece_width + char_width > width and #piece > 0 then
      result[#result + 1] = piece
      piece = {}
      piece_width = 0
    end
    piece[#piece + 1] = char
    piece_width = piece_width + char_width
  end
  if #piece > 0 then
    result[#result + 1] = piece
  end
  return result
end

---@param chars table[]
---@return OrgInlineSegment[]
local function to_segments(chars)
  local segments = {}
  for _, char in ipairs(chars) do
    push(segments, char.c, char.hl)
  end
  return segments
end

---@param segments OrgInlineSegment[]
---@param width integer
---@return OrgInlineSegment[][]
function M.wrap(segments, width)
  width = math.max(tonumber(width) or 1, 1)

  local words = {}
  local word = nil
  for _, segment in ipairs(segments or {}) do
    for _, char in ipairs(vim.fn.split(segment.text, [[\zs]])) do
      if char:match('%s') then
        if word then
          words[#words + 1] = word
          word = nil
        end
      else
        word = word or {}
        word[#word + 1] = { c = char, hl = segment.hl }
      end
    end
  end
  if word then
    words[#words + 1] = word
  end

  if #words == 0 then
    return { {} }
  end

  local lines = {}
  local current = {}
  local current_width = 0
  local function flush()
    if #current > 0 then
      lines[#lines + 1] = to_segments(current)
      current = {}
      current_width = 0
    end
  end

  for _, word_chars in ipairs(words) do
    for _, piece in ipairs(pieces(word_chars, width)) do
      local piece_width = 0
      for _, char in ipairs(piece) do
        piece_width = piece_width + vim.fn.strdisplaywidth(char.c)
      end
      local space = #current > 0 and 1 or 0
      if current_width + space + piece_width > width and #current > 0 then
        flush()
        space = 0
      end
      if space == 1 then
        current[#current + 1] = { c = ' ', hl = nil }
      end
      for _, char in ipairs(piece) do
        current[#current + 1] = char
      end
      current_width = current_width + space + piece_width
    end
  end
  flush()

  if #lines == 0 then
    return { {} }
  end
  return lines
end

return M
