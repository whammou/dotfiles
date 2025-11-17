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
