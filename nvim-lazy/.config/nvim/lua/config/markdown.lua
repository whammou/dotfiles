local markdown = require("render-markdown")
local headlines = require("headlines")

markdown.setup({
  anti_conceal = {
    enabled = true,
    ignore = {},
  },
  -- Prevent the plugin from overriding concealcursor to '' (which disables cursor-line conceal)
  win_options = {
    conceallevel = {
      default = 3,
      rendered = 3,
    },
    concealcursor = {
      rendered = "nc",
      default = "nc",
    },
  },
  completions = {
    blink = { enabled = true },
    lsp = { enabled = true },
  },
  paragraph = {
    enabled = true,
    left_margin = 0,
    indent = 0,
  },
  heading = {
    enabled = false,
    position = "inline",
    border = false,
    border_virtual = false,
  },
  indent = {
    enabled = false,
    skip_heading = true,
    per_level = 1,
    skip_level = 0,
    icon = "",
  },

  latex = {
    enabled = true,
  },

  html = {
    enabled = true,
  },
})

vim.cmd([[highlight MarkdownHeadline1 guifg=#56b6c2 gui=bold guibg=#2b3c44]])
vim.cmd([[highlight MarkdownHeadline2 guifg=#c678dd gui=bold guibg=#393247]])
vim.cmd([[highlight MarkdownHeadline3 guifg=#61afef gui=bold guibg=#2c3949]])
vim.cmd([[highlight MarkdownHeadline4 guifg=#e5c07b gui=bold guibg=#3d3c39]])
vim.cmd([[highlight MarkdownHeadline5 guifg=#98c379 gui=bold guibg=#333d39]])
vim.cmd([[highlight MarkdownHeadline6 guifg=#e86671 gui=bold guibg=#3e323a]])
vim.cmd([[highlight Dash gui=bold]])

headlines.setup({
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
