-- filetags.lua — Interactive filetags search using fzf-lua
-- Use `OrgFiletags` command or `<leader>oF` to find files by `#+FILETAGS:`.
-- Requires fzf-lua to be installed (comes with fzf-org.nvim).

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

return {
  OrgFiletags = OrgFiletags,
}
