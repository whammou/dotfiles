---External handler for opening org nodes by ID.
---Called from `orgmode-open-id` shell script via nvim --remote-send.
---Usage (in terminal): xdg-open id:<uuid>
---@param id string - The UUID, optionally prefixed with "id:"
function _G.OpenOrgId(id)
  -- Strip 'id:' prefix if present (from xdg-open id:<uuid>)
  if vim.startswith(id, 'id:') then
    id = id:sub(4)
  end

  -- Strip optional ::*Target suffix (from [[id:uuid::*Title]] link format)
  local idx = id:find('::')
  if idx then
    id = id:sub(1, idx - 1)
  end

  id = vim.trim(id)
  if id == '' then
    vim.notify('OpenOrgId: no ID provided', vim.log.levels.ERROR)
    return
  end

  -- Get the running orgmode singleton instance
  local ok, org = pcall(function()
    return require('orgmode').instance()
  end)
  if not ok then
    vim.notify(
      string.format('OpenOrgId: orgmode not loaded: %s. Open an org file first.', tostring(org)),
      vim.log.levels.ERROR
    )
    return
  end
  if not org or not org.files then
    vim.notify('OpenOrgId: orgmode files not initialized yet. Try again.', vim.log.levels.ERROR)
    return
  end

  -- Search for file-level :ID: property (#+PROPERTY: id <uuid>)
  local files = org.files:find_files_with_property('id', id)
  if #files > 0 then
    if #files > 1 then
      vim.notify(
        string.format('OpenOrgId: %d files found with id %s, opening first', #files, id),
        vim.log.levels.WARN
      )
    end
    vim.cmd('edit ' .. vim.fn.fnameescape(files[1].filename))
    vim.cmd([[normal! zx]])  -- recalculate folds for new buffer
    vim.notify(string.format('Opened file with id: %s', id), vim.log.levels.INFO)
    return
  end

  -- Search for headline-level :ID: property (in :PROPERTIES: drawer)
  local headlines = org.files:find_headlines_with_property('id', id)
  if #headlines == 0 then
    vim.notify(string.format('OpenOrgId: no node found with id: %s', id), vim.log.levels.WARN)
    return
  end

  if #headlines > 1 then
    vim.notify(
      string.format('OpenOrgId: %d headlines found with id %s, opening first', #headlines, id),
      vim.log.levels.WARN
    )
  end

  local hl = headlines[1]
  vim.cmd('edit ' .. vim.fn.fnameescape(hl.file.filename))
  vim.cmd([[normal! zx]])   -- recalculate folds for new buffer
  vim.fn.cursor({ hl:get_range().start_line, 1 })
  vim.cmd([[normal! zv]])   -- open fold at cursor
  vim.notify(string.format('Opened headline with id: %s', id), vim.log.levels.INFO)
end
