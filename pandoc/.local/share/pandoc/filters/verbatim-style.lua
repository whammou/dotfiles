local function escape_latex(text)
  -- backslash first: must escape \ before other chars it prefixes
  text = text:gsub("\\", "\\textbackslash{}")
  text = text:gsub("{", "\\{")
  text = text:gsub("}", "\\}")
  text = text:gsub("%%", "\\%%")
  text = text:gsub("%$", "\\$")
  text = text:gsub("&", "\\&")
  text = text:gsub("#", "\\#")
  text = text:gsub("_", "\\_")
  text = text:gsub("~", "\\textasciitilde{}")
  text = text:gsub("%^", "\\textasciicircum{}")
  return text
end

function Code(elem)
  return pandoc.RawInline('latex', '\\code{' .. escape_latex(elem.text) .. '}')
end