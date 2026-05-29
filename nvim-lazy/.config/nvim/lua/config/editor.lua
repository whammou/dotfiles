vim.cmd([[highlight MarkdownHeadline1 guifg=#56b6c2 gui=bold guibg=#2b3c44]])
vim.cmd([[highlight MarkdownHeadline2 guifg=#c678dd gui=bold guibg=#393247]])
vim.cmd([[highlight MarkdownHeadline3 guifg=#61afef gui=bold guibg=#2c3949]])
vim.cmd([[highlight MarkdownHeadline4 guifg=#e5c07b gui=bold guibg=#3d3c39]])
vim.cmd([[highlight MarkdownHeadline5 guifg=#98c379 gui=bold guibg=#333d39]])
vim.cmd([[highlight MarkdownHeadline6 guifg=#e86671 gui=bold guibg=#3e323a]])
vim.cmd([[highlight Dash gui=bold]])

vim.cmd([[highlight Headline1 guibg=#2b3c44]])
vim.cmd([[highlight Headline2 guibg=#393247]])
vim.cmd([[highlight Headline3 guibg=#2c3949]])
vim.cmd([[highlight Headline4 guibg=#3d3c39]])
vim.cmd([[highlight Headline5 guibg=#333d39]])
vim.cmd([[highlight Headline6 guibg=#3e323a]])

require("headlines").setup({
  org = {
    headline_highlights = {
      "Headline1",
      "Headline2",
      "Headline3",
      "Headline4",
      "Headline5",
      "Headline6",
    },
    bullets = { "󰫃", "󰫄", "󰫅", "󰫆", "󰫇", "󰫈" },
    codeblock_highlight = "Codeblock",
    dash_highlight = "Comment",
    dash_string = "─",
    fat_headlines = true,
  },
  markdown = {
    bullet_highlights = {
      "MarkdownHeadline1",
      "MarkdownHeadline2",
      "MarkdownHeadline3",
      "MarkdownHeadline4",
      "MarkdownHeadline5",
      "MarkdownHeadline6",
    },
    headline_highlights = {
      "MarkdownHeadline1",
      "MarkdownHeadline2",
      "MarkdownHeadline3",
      "MarkdownHeadline4",
      "MarkdownHeadline5",
      "MarkdownHeadline6",
    },
    bullets = { "󰫃", "󰫄", "󰫅", "󰫆", "󰫇", "󰫈" },
    codeblock_highlight = "Codeblock",
    dash_highlight = "Comment",
    dash_string = "─",
    fat_headlines = true,
  },
})
