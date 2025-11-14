vim.cmd([[highlight Headline1 guibg=#1e2718]])
vim.cmd([[highlight Headline2 guibg=#21262d]])
vim.cmd([[highlight CodeBlock guibg=#1c1c1c]])
vim.cmd([[highlight Dash guibg=#D19A66 gui=bold]])

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
      "@org.headline.level1.org",
      "@org.headline.level2.org",
      "@org.headline.level3.org",
      "@org.headline.level4.org",
      "@org.headline.level5.org",
      "@org.headline.level6.org",
    },
  },
})
