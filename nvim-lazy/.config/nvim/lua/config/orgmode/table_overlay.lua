-- Renders org tables in render-markdown.nvim's overlay style. Tables that fit
-- the window are drawn as one overlay per row; wider tables get their columns
-- shrunk and their cell text reflowed into extra virtual lines, mirroring
-- render-markdown's pipe_table wrap behavior.

local M = {}

local inline = require('config.orgmode.inline')

local border = {
  top = { '┌', '┬', '┐' },
  mid = { '├', '┼', '┤' },
  bot = { '└', '┴', '┘' },
  vert = '│',
  hor = '─',
}

local HL = {
  head = 'RenderMarkdownTableHead',
  row = 'RenderMarkdownTableRow',
}

local MIN_WIDTH = 3

local function width(text)
  return vim.fn.strdisplaywidth(text)
end

local function cell_text(cell_node, buf)
  for child in cell_node:iter_children() do
    if child:type() == 'contents' then
      return (vim.treesitter.get_node_text(child, buf):gsub('%s*\n%s*', ' '))
    end
  end
  return ''
end

local function parse_table(table_node, buf)
  local rows = {}
  for child in table_node:iter_children() do
    local kind = child:type()
    if kind == 'row' or kind == 'hr' then
      local row = { type = kind, line = child:range(), cells = {} }
      for node in child:iter_children() do
        if node:type() == 'cell' then
          row.cells[#row.cells + 1] = cell_text(node, buf)
        end
      end
      rows[#rows + 1] = row
    end
  end
  return rows
end

local function col_widths(rows, ncols)
  local widths = {}
  for i = 1, ncols do
    widths[i] = 1
  end
  for _, row in ipairs(rows) do
    for i, text in ipairs(row.cells) do
      widths[i] = math.max(widths[i] or 1, width(text))
    end
  end
  return widths
end

local function total_widths(widths)
  local total = 0
  for _, w in ipairs(widths) do
    total = total + w
  end
  return total
end

local function rendered_width(widths)
  return 1 + 3 * #widths + total_widths(widths)
end

local function allocate(desired, budget)
  if total_widths(desired) <= budget then
    return desired
  end

  local minimum = {}
  for i in ipairs(desired) do
    minimum[i] = math.min(MIN_WIDTH, desired[i])
  end

  local lo, hi, cap = 1, 0, nil
  for _, w in ipairs(desired) do
    hi = math.max(hi, w)
  end
  while lo <= hi do
    local mid = math.floor((lo + hi) / 2)
    local sum = 0
    for i, w in ipairs(desired) do
      sum = sum + math.max(minimum[i], math.min(w, mid))
    end
    if sum <= budget then
      cap = mid
      lo = mid + 1
    else
      hi = mid - 1
    end
  end

  local widths = {}
  for i, w in ipairs(desired) do
    widths[i] = cap and math.max(minimum[i], math.min(w, cap)) or minimum[i]
  end
  return widths
end

local function rule_chunks(widths, indent, glyphs, hl)
  local chunks = { { indent .. glyphs[1], hl } }
  for i, w in ipairs(widths) do
    chunks[#chunks + 1] = { string.rep(border.hor, w + 2), hl }
    chunks[#chunks + 1] = { i < #widths and glyphs[2] or glyphs[3], hl }
  end
  return chunks
end

local function chunk_width(chunks)
  local total = 0
  for _, chunk in ipairs(chunks) do
    total = total + width(chunk[1])
  end
  return total
end

local function pad_chunks(chunks, target, hl)
  local fill = target - chunk_width(chunks)
  if fill > 0 then
    chunks[#chunks + 1] = { string.rep(' ', fill), hl }
  end
  return chunks
end

local function row_fragments(row, widths, indent, hl)
  local wrapped = {}
  local height = 1
  for i, w in ipairs(widths) do
    wrapped[i] = inline.wrap(inline.segments(row.cells[i] or ''), w)
    height = math.max(height, #wrapped[i])
  end

  local fragments = {}
  for fragment = 1, height do
    local chunks = { { indent .. border.vert, hl } }
    for i, w in ipairs(widths) do
      local line = wrapped[i][fragment] or {}
      local text = inline.plain(line)
      chunks[#chunks + 1] = { ' ', hl }
      for _, segment in ipairs(line) do
        chunks[#chunks + 1] = { segment.text, segment.hl or hl }
      end
      chunks[#chunks + 1] = { string.rep(' ', math.max(w - width(text), 0) + 1), hl }
      chunks[#chunks + 1] = { border.vert, hl }
    end
    fragments[#fragments + 1] = chunks
  end
  return fragments
end

local function window_width(buf)
  local win = vim.fn.bufwinid(buf)
  if win == -1 then
    return vim.o.columns
  end
  local info = vim.fn.getwininfo(win)[1]
  return vim.api.nvim_win_get_width(win) - (info and info.textoff or 0)
end

local function render(table_node, buf)
  local marks = {}
  local rows = parse_table(table_node, buf)
  if #rows == 0 then
    return marks
  end

  local ncols = 0
  for _, row in ipairs(rows) do
    ncols = math.max(ncols, #row.cells)
  end
  if ncols == 0 then
    return marks
  end

  local start_row, start_col = table_node:range()
  local indent = string.rep(' ', start_col)
  local last = rows[#rows]

  local widths = col_widths(rows, ncols)
  local available = window_width(buf) - start_col
  local wrapping = rendered_width(widths) > available
  if wrapping then
    widths = allocate(widths, available - 3 * ncols - 1)
  end

  local header = {}
  for i, row in ipairs(rows) do
    if row.type == 'row' and rows[i + 1] and rows[i + 1].type == 'hr' then
      header[row.line] = true
    end
  end

  local by_line = {}
  for _, row in ipairs(rows) do
    by_line[row.line] = row
  end

  local function overlay(line, chunks, hl)
    local text = vim.api.nvim_buf_get_lines(buf, line, line + 1, false)[1] or ''
    local target = math.max(width(text), chunk_width(chunks))
    marks[#marks + 1] = {
      conceal = true,
      start_row = line,
      start_col = 0,
      opts = {
        end_row = line,
        end_col = #text,
        virt_text = pad_chunks(chunks, target, hl),
        virt_text_pos = 'overlay',
        priority = 100,
      },
    }
  end

  local function flow(line, fragments)
    local text = vim.api.nvim_buf_get_lines(buf, line, line + 1, false)[1] or ''
    marks[#marks + 1] = {
      conceal = true,
      start_row = line,
      start_col = 0,
      opts = {
        end_row = line,
        end_col = #text,
        conceal_lines = '',
        priority = 100,
      },
      replace = fragments,
    }
  end

  local planned = {}
  for line = start_row, last.line do
    local row = by_line[line]
    if row then
      if row.type == 'hr' then
        local chunks = rule_chunks(widths, indent, border.mid, HL.head)
        local source = vim.api.nvim_buf_get_lines(buf, line, line + 1, false)[1] or ''
        planned[#planned + 1] = {
          line = line,
          chunks = chunks,
          fragments = { chunks },
          hl = HL.head,
          flow = width(source) > chunk_width(chunks),
        }
      else
        local hl = header[line] and HL.head or HL.row
        local fragments = row_fragments(row, widths, indent, hl)
        local source = vim.api.nvim_buf_get_lines(buf, line, line + 1, false)[1] or ''
        planned[#planned + 1] = {
          line = line,
          fragments = fragments,
          hl = hl,
          flow = #fragments > 1 or width(source) > chunk_width(fragments[1]),
        }
      end
    end
  end

  local function virtual_rule(line, chunks, above)
    marks[#marks + 1] = {
      conceal = true,
      start_row = line,
      start_col = 0,
      opts = {
        virt_lines = { chunks },
        virt_lines_above = above,
        priority = 100,
      },
    }
  end

  local first = planned[1]
  local trailing = planned[#planned]
  local top = rule_chunks(widths, indent, border.top, HL.head)
  local bot = rule_chunks(widths, indent, border.bot, HL.row)

  if first and first.flow then
    table.insert(first.fragments, 1, top)
  else
    virtual_rule(start_row, top, true)
  end

  if trailing and trailing.flow then
    trailing.fragments[#trailing.fragments + 1] = bot
  else
    virtual_rule(last.line, bot, false)
  end

  for _, item in ipairs(planned) do
    if item.flow then
      flow(item.line, item.fragments)
    elseif item.fragments then
      overlay(item.line, item.fragments[1], item.hl)
    else
      overlay(item.line, item.chunks, item.hl)
    end
  end

  return marks
end

function M.render_table(table_node, buf)
  return render(table_node, buf)
end

function M.parse(ctx)
  local ok, query = pcall(vim.treesitter.query.parse, 'org', '(table) @table')
  if not ok then
    return {}
  end
  local marks = {}
  for _, node in query:iter_captures(ctx.root, ctx.buf) do
    vim.list_extend(marks, render(node, ctx.buf))
  end
  return marks
end

return M
