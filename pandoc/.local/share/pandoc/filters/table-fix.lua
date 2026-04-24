function Table(tbl)
  if FORMAT:match 'latex' then
    local n = #tbl.colspecs
    if n == 0 then return tbl end
    
    local width = 1.0 / n
    
    tbl.colspecs = tbl.colspecs:map(function(colspec, i)
      return {colspec[1], width}
    end)
    
    if tbl.widths then
      for i = 1, n do
        tbl.widths[i] = width
      end
    end
    
    return tbl
  end
  return tbl
end