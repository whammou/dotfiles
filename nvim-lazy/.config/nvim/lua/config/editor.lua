local M = {}

function M.setup_headlines()
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
    query = vim.treesitter.query.parse("org", [[
      (headline (stars) @headline)

      (
        (expr) @dash
        (#match? @dash "^-----+$")
      )

      (block
        name: (expr) @_name
        (#match? @_name "(SRC|src)")
      ) @codeblock

      (paragraph . (expr) @quote
        (#eq? @quote ">")
      )
    ]]),
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
end

function M.setup_baleia()
  local od = require("onedark.colors")
  local kitty_colors = {
    [0] = od.bg_d,
    [1] = od.red,
    [2] = od.green,
    [3] = od.yellow,
    [4] = od.blue,
    [5] = od.purple,
    [6] = od.cyan,
    [7] = od.light_grey,
    [8] = od.bg_d,
    [9] = od.tbg_red,
    [10] = od.tbg_green,
    [11] = od.tbg_yellow,
    [12] = od.tbg_blue,
    [13] = od.tbg_purple,
    [14] = od.tbg_cyan,
    [15] = od.grey,
  }
  for i = 0, 15 do
    vim.g["terminal_color_" .. i] = kitty_colors[i]
  end
  local baleia = require("baleia").setup({ strip_ansi_codes = true, colors = kitty_colors })
  vim.api.nvim_create_user_command("BaleiaColorize", function()
    baleia.once(vim.api.nvim_get_current_buf())
  end, { bang = true, desc = "Colorize ANSI codes via baleia (onedark/kitty palette)" })
  vim.api.nvim_create_autocmd("FileType", {
    pattern = "kitty-scrollback",
    callback = function(args)
      baleia.once(args.buf)
    end,
  })
end

return M
