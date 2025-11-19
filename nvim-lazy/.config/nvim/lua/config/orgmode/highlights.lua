vim.cmd([[highlight Headline1 guibg=#1D313E]])
vim.cmd([[highlight Headline2 guibg=#2B2741]])
vim.cmd([[highlight Headline3 guibg=#1E2E43]])
vim.cmd([[highlight Headline4 guibg=#2F3133]])
vim.cmd([[highlight Headline5 guibg=#253233]])
vim.cmd([[highlight Headline6 guibg=#302734]])

vim.cmd([[highlight Dash gui=bold]])

require("headlines").setup({
  markdown = {
    headline_highlights = false,
    bullets_highlights = false,
    codeblock_highlight = false,
    dash_highlight = false,
    quote_highlight = false,
  },
  org = {
    headline_highlights = {
      "Headline1",
      "Headline2",
      "Headline3",
      "Headline4",
      "Headline5",
      "Headline6",
    },
    -- bullets = { "󰎤", "󰎧", "󰎪", "󰎭", "󰎱", "󰎳" },
    bullets = { "󰫃", "󰫄", "󰫅", "󰫆", "󰫇", "󰫈" },
    codeblock_highlight = "Codeblock",
    dash_highlight = "Comment",
    dash_string = "─",
    fat_headlines = true,
  },
})

require("org-bullets").setup({
  concealcursor = true,
  symbols = {
    list = "»",
  },
})

require("orgmode").setup({
  org_todo_keyword_faces = {
    TODO = ":foreground #c75ae8 :weight bold :slant italic",
    RECR = ":foreground #c75ae8 :weight bold :slant italic",
    DOIN = ":foreground #34bfd0 :weight bold :slant italic",
    PEND = ":foreground #93a4c3 :weight bold :slant italic",
    OUTL = ":foreground #93a4c3 :weight bold :slant italic",
    IDEA = ":foreground #93a4c3 :weight bold :slant italic",
    WAIT = ":foreground #dd9046 :weight bold :slant italic",
    EXPL = ":foreground #dd9046 :weight bold :slant italic",
    FDBK = ":foreground #dd9046 :weight bold :slant italic",
    NEXT = ":foreground #54b0fd :weight bold :slant italic",
    TARGET = ":foreground #c75ae8 :weight bold :slant italic",
    RVIW = ":foreground #efbd5d :weight bold :slant italic",
    PRTL = ":foreground #efbd5d :weight bold :slant italic",
    ABRT = ":foreground #f65866 :weight bold :slant italic",
    DONE = ":foreground #8bcd5b :weight bold :slant italic",
  },
})
