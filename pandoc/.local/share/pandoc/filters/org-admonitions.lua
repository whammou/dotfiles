local admonition_map = {
  NOTE = "noteblock",
  TIP = "tipblock", 
  WARNING = "warningblock",
  IMPORTANT = "importantblock",
  CAUTION = "cautionblock",
  INFO = "noteblock",
  ERROR = "cautionblock"
}

-- Helper to convert AST elements to LaTeX while preserving math delimiters
local function to_latex_inline(elem)
  if elem.t == "Math" then
    if elem.mathtype == "DisplayMath" then
      return "$$" .. elem.text .. "$$"
    else
      return "$" .. elem.text .. "$"
    end
  elseif elem.t == "RawInline" and elem.format == "latex" then
    return elem.text
  elseif elem.t == "Str" then
    return elem.text
  elseif elem.t == "Space" then
    return " "
  elseif elem.t == "LineBreak" then
    return "\\newline "
  elseif elem.t == "SoftBreak" then
    return " "
  elseif elem.t == "Emph" then
    local inner = ""
    for _, e in ipairs(elem.c) do
      inner = inner .. to_latex_inline(e)
    end
    return "\\emph{" .. inner .. "}"
  elseif elem.t == "Strong" then
    local inner = ""
    for _, e in ipairs(elem.c) do
      inner = inner .. to_latex_inline(e)
    end
    return "\\textbf{" .. inner .. "}"
  elseif elem.t == "Code" then
    return "\\texttt{" .. elem.text .. "}"
  elseif elem.t == "Link" then
    local inner = ""
    for _, e in ipairs(elem.c) do
      inner = inner .. to_latex_inline(e)
    end
    return string.format("\\href{%s}{%s}", elem.target[1], inner)
  elseif elem.t == "Image" then
    local caption = ""
    for _, e in ipairs(elem.c) do
      caption = caption .. to_latex_inline(e)
    end
    return string.format("\\includegraphics{%s}", elem.src)
  else
    return pandoc.utils.stringify(elem)
  end
end

local function para_to_latex(para)
  local result = {}
  for _, elem in ipairs(para.c) do
    table.insert(result, to_latex_inline(elem))
  end
  local text = table.concat(result, ""):gsub("%[!%a+%]%s*", ""):gsub("^%s+", ""):gsub("%s+$", "")
  return text
end

local function block_to_latex(block)
  if block.t == "Para" then
    return para_to_latex(block)
  elseif block.t == "BulletList" then
    local lines = {}
    for _, item in ipairs(block.c) do
      local item_lines = {}
      for _, subblock in ipairs(item) do
        table.insert(item_lines, "  \\item " .. block_to_latex(subblock))
      end
      table.insert(lines, table.concat(item_lines, "\n"))
    end
    return "\\begin{itemize}\n" .. table.concat(lines, "\n") .. "\n\\end{itemize}"
  elseif block.t == "OrderedList" then
    local lines = {}
    for _, item in ipairs(block.c) do
      local item_lines = {}
      for _, subblock in ipairs(item) do
        table.insert(item_lines, "  \\item " .. block_to_latex(subblock))
      end
      table.insert(lines, table.concat(item_lines, "\n"))
    end
    return "\\begin{enumerate}\n" .. table.concat(lines, "\n") .. "\n\\end{enumerate}"
  elseif block.t == "Plain" then
    return para_to_latex(block)
  elseif block.t == "RawBlock" and block.format == "latex" then
    return block.text
  else
    return pandoc.utils.stringify(block)
  end
end

function BlockQuote(block)
  if #block.c == 0 then
    return block
  end
  
  local first = block.c[1]
  
  if first.t ~= "Para" or #first.c == 0 then
    return block
  end
  
  local first_elem = first.c[1]
  
  if first_elem.t ~= "Str" then
    return block
  end
  
  local ad_name = first_elem.text:match("%[!([A-Z]+)%]")
  
  if not ad_name or not admonition_map[ad_name] then
    return block
  end
  
  local env_name = admonition_map[ad_name]
  local children = {}
  
  local marker_stripped = pandoc.Para({})
  for _, elem in ipairs(block.c[1].c) do
    if elem.t == "Str" then
      local cleaned = elem.text:gsub("%[!([A-Z]+)%]%s*", "")
      if cleaned ~= "" then
        table.insert(marker_stripped.c, pandoc.Str(cleaned))
      end
    else
      table.insert(marker_stripped.c, elem)
    end
  end
  local header_latex = para_to_latex(marker_stripped)
  if header_latex ~= "" then
    table.insert(children, header_latex)
  end
  
  for i = 2, #block.c do
    local content = block_to_latex(block.c[i])
    if content ~= "" then
      table.insert(children, content)
    end
  end
  
  local content = table.concat(children, "\n")
  
  local latex = string.format(
    '\\begin{%s}%s\\end{%s}',
    env_name,
    content,
    env_name
  )
  
  return pandoc.RawBlock("latex", latex)
end