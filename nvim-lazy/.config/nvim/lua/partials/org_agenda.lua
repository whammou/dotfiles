vim.api.nvim_create_autocmd("BufWinEnter", {
  pattern = "orgagenda",
  once = true,
  callback = function()
    vim.defer_fn(function()
      -- Wipe empty [No Name] buffers left from `nvim` startup (and `enew` in script)
      -- Snacks.bufdelete.other() creates a fallback [No Name] when current is nobuflisted (orgagenda),
      -- so avoid it and wipe directly
      for _, buf in ipairs(vim.api.nvim_list_bufs()) do
        if buf ~= vim.api.nvim_get_current_buf() and vim.api.nvim_buf_is_valid(buf) then
          local name = vim.api.nvim_buf_get_name(buf)
          local is_empty = name == "" and not vim.bo[buf].modified and vim.api.nvim_buf_line_count(buf) == 1 and vim.fn.getbufline(buf, 1)[1] == ""
          if is_empty then
            pcall(vim.api.nvim_buf_delete, buf, { force = true })
            pcall(vim.cmd, "bwipeout! " .. buf)
          end
        end
      end
      if #vim.api.nvim_list_wins() > 1 then
        pcall(vim.cmd, "only")
      end
      vim.cmd("set foldmethod=indent")
    end, 0)
  end,
})
