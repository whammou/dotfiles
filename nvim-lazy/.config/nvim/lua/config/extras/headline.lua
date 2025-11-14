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
      "ColorColumn",
    },
  },
})
