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
