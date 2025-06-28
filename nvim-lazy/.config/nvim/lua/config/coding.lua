local blink = require("blink.cmp")

blink.setup({
  --enabled = function()
  --  local buftype = vim.api.nvim_get_option_value("buftype", { buf = 0 })
  --  if buftype == "nofile" then
  --    return false
  --  end
  --  -- ... handling other conditions
  --end,
  snippets = { preset = "luasnip" },
  sources = {
    default = { "lsp", "path", "snippets", "buffer" },
    per_filetype = {
      org = { "lsp", "path", "snippets", "orgmode" },
      markdown = { "lsp", "path", "snippets" },
    },
    providers = {
      snippets = {
        name = "luasnip",
        enabled = true,
      },
      orgmode = {
        name = "Orgmode",
        module = "orgmode.org.autocompletion.blink",
        -- fallbacks = { "buffer" },
      },
    },
  },
  keymap = {
    preset = "default",
    -- ["<C-Cr>"] = { "select_and_accept" },
  },
})
