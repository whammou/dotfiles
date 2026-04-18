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
  local content_parts = {}
  
  for i, para in ipairs(block.c) do
    local para_content = para_to_latex(para)
    if para_content ~= "" then
      table.insert(content_parts, para_content)
    end
  end
  
  local content = table.concat(content_parts, "\\\\\n")
  
  local latex = string.format(
    '\\begin{%s}%s\\end{%s}',
    env_name,
    content,
    env_name
  )
  
  return pandoc.RawBlock("latex", latex)
end