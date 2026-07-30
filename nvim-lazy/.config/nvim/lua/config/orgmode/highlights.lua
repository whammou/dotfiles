local quote_query = vim.treesitter.query.parse("org", [[
  (block name: (expr) @_name (#eq? @_name "quote")) @block
]])

vim.api.nvim_create_autocmd("FileType", {
  pattern = "org",
  callback = function()
    vim.cmd([[
      syntax match orgAdmonitionWarning '\[!WARNING\]'
      syntax match orgAdmonitionCaution '\[!CAUTION\]'
      syntax match orgAdmonitionImportant '\[!IMPORTANT\]'
      syntax match orgAdmonitionTip '\[!TIP\]'
      syntax match orgAdmonitionNote '\[!NOTE\]'
      highlight orgAdmonitionWarning guifg=#d19a66 gui=bold
      highlight orgAdmonitionCaution guifg=#e86671 gui=bold
      highlight orgAdmonitionImportant guifg=#c678dd gui=bold
      highlight orgAdmonitionTip guifg=#98c379 gui=bold
      highlight orgAdmonitionNote guifg=#61afef gui=bold
    ]])

    vim.schedule(function()
      local bufnr = vim.api.nvim_get_current_buf()
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
        callback = refresh,
      })
    end)
  end,
})

require("org-bullets").setup({
  concealcursor = true,
  symbols = {
    --list = "»",
    list = "󰨓",
  },
})

require("orgmode").setup({
  org_todo_keyword_faces = {
    TODO = ":foreground #775289 :weight bold :slant italic",
    OPEN = ":foreground #775289 :weight bold :slant italic",
    RECR = ":foreground #775289 :weight bold :slant italic",
    DOIN = ":foreground #3F717B :weight bold :slant italic",
    PROG = ":foreground #607857 :weight bold :slant italic",
    PEND = ":foreground #5c6370 :weight bold :slant italic",
    OUTL = ":foreground #5c6370 :weight bold :slant italic",
    IDEA = ":foreground #5c6370 :weight bold :slant italic",
    INTR = ":foreground #6e594f :weight bold :slant italic",
    WAIT = ":foreground #6e594f :weight bold :slant italic",
    EXPL = ":foreground #6e594f :weight bold :slant italic",
    FDBK = ":foreground #6e594f :weight bold :slant italic",
    TEST = ":foreground #6e594f :weight bold :slant italic",
    NEXT = ":foreground #456E92 :weight bold :slant italic",
    TARGET = ":foreground #775289 :weight bold :slant italic",
    RVIW = ":foreground #e5c07b :weight bold :slant italic",
    PRTL = ":foreground #e5c07b :weight bold :slant italic",
    ABRT = ":foreground #e86671 :weight bold :slant italic",
    DONE = ":foreground #98c379 :weight bold :slant italic",
    CLSD = ":foreground #5c6370 :weight bold :slant italic",
  },
})
