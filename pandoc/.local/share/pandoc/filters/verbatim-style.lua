function Code(elem)
  return pandoc.RawInline('latex', '\\code{' .. elem.text .. '}')
end