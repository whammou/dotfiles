require("render-markdown").setup({
  file_types = { "markdown", "org" },
  custom_handlers = {
    org = require("config.orgmode.table_overlay"),
  },
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

-- render-markdown is change-driven, so wrapped tables stay stale after a resize.
local resize_group = vim.api.nvim_create_augroup("markdown_resize_rerender", { clear = true })
vim.api.nvim_create_autocmd({ "WinResized", "VimResized" }, {
  group = resize_group,
  callback = function()
    local seen = {}
    local wins = vim.v.event and vim.v.event.windows
    if not wins or #wins == 0 then
      wins = vim.api.nvim_list_wins()
    end
    for _, win in ipairs(wins) do
      if vim.api.nvim_win_is_valid(win) then
        local buf = vim.api.nvim_win_get_buf(win)
        if not seen[buf] and vim.bo[buf].filetype == "org" then
          seen[buf] = true
          pcall(function()
            require("render-markdown.core.ui").update(buf, win, "WinResized", true)
          end)
        end
      end
    end
  end,
})


