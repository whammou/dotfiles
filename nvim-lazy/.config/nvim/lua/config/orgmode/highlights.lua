local quote_query = vim.treesitter.query.parse("org", [[
  (block name: (expr) @_name (#eq? @_name "quote")) @block
]])

local function setup_org(bufnr)
  local augroup = vim.api.nvim_create_augroup("org-highlights-" .. bufnr, { clear = true })

  -- vim.treesitter.start() sets syntax='' (highlighter.lua), which also
  -- clears all syntax match items. orgmode's restart_highlights, its
  -- ftplugin, and Snacks.quickfile all call it after we run, so re-assert
  -- on every Syntax event.
  local function assert_regex_syntax()
    if vim.bo[bufnr].syntax == "ON" then
      return
    end
    vim.api.nvim_buf_call(bufnr, function()
      vim.bo[bufnr].syntax = "ON"
      -- Built-in org.vim's orgVerbatimBlock swallows block contents and
      -- blocks nested matches; orgmode's org.vim doesn't define it (E28
      -- when absent, so pcall).
      pcall(vim.cmd, "syntax clear orgVerbatimBlock")
      vim.cmd([[
        syntax match orgAdmonitionWarning '\[!WARNING\]'
        syntax match orgAdmonitionCaution '\[!CAUTION\]'
        syntax match orgAdmonitionImportant '\[!IMPORTANT\]'
        syntax match orgAdmonitionTip '\[!TIP\]'
        syntax match orgAdmonitionNote '\[!NOTE\]'
      ]])
    end)
  end

  assert_regex_syntax()
  vim.api.nvim_create_autocmd("Syntax", {
    buffer = bufnr,
    group = augroup,
    callback = assert_regex_syntax,
  })

  vim.api.nvim_set_hl(0, "orgAdmonitionWarning", { fg = "#d19a66", bold = true })
  vim.api.nvim_set_hl(0, "orgAdmonitionCaution", { fg = "#e86671", bold = true })
  vim.api.nvim_set_hl(0, "orgAdmonitionImportant", { fg = "#c678dd", bold = true })
  vim.api.nvim_set_hl(0, "orgAdmonitionTip", { fg = "#98c379", bold = true })
  vim.api.nvim_set_hl(0, "orgAdmonitionNote", { fg = "#61afef", bold = true })

  vim.schedule(function()
    local ns = vim.api.nvim_create_namespace("org-quote-block")

    local function is_admonition(node)
      local ok, result = pcall(vim.treesitter.get_node_text, node, bufnr)
      if not ok or not result then return false end
      local text = type(result) == "table" and table.concat(result, "\n") or result
      return text:match("%[!NOTE%]") or text:match("%[!WARNING%]")
        or text:match("%[!CAUTION%]") or text:match("%[!IMPORTANT%]")
        or text:match("%[!TIP%]")
    end

    local function refresh()
      vim.api.nvim_buf_clear_namespace(bufnr, ns, 0, -1)
      local ok, parser = pcall(vim.treesitter.get_parser, bufnr, "org")
      if not ok then return end

      local root = parser:parse()[1]:root()
      for id, node in quote_query:iter_captures(root, bufnr) do
        if quote_query.captures[id] == "block" and not is_admonition(node) then
          local ok_r, start_row, _, end_row = pcall(node.range, node)
          if ok_r then
            local bg_start = start_row
            while bg_start > 0 do
              local line = vim.api.nvim_buf_get_lines(bufnr, bg_start - 1, bg_start, false)[1]
              if line and line:match("^#%+") then
                bg_start = bg_start - 1
              else
                break
              end
            end

            vim.api.nvim_buf_set_extmark(bufnr, ns, bg_start, 0, {
              end_row = end_row,
              hl_group = "Quote",
              hl_eol = true,
              priority = 50,
            })
          end
        end
      end
    end

    refresh()
    vim.api.nvim_create_autocmd({ "InsertLeave", "BufWritePost" }, {
      buffer = bufnr,
      group = augroup,
      callback = refresh,
    })
  end)
end

-- Errors here surface inside lazy.nvim's plugin-load chain (which is running
-- during the FileType event), so never let setup_org abort it.
local function guarded_setup(bufnr)
  local ok, err = pcall(setup_org, bufnr)
  if not ok then
    vim.notify("orgmode highlights setup failed: " .. tostring(err), vim.log.levels.WARN)
  end
end

vim.api.nvim_create_autocmd("FileType", {
  pattern = "org",
  callback = function(ev)
    guarded_setup(ev.buf)
  end,
})

-- lazy.nvim loads this module during the FileType event itself (ft = "org"),
-- so the autocmd above is created too late to fire for the current buffer.
-- Set up the current buffer explicitly.
if vim.bo.filetype == "org" then
  vim.schedule(function()
    guarded_setup(vim.api.nvim_get_current_buf())
  end)
end
