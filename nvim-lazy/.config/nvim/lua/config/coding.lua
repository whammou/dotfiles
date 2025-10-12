local blink = require("blink.cmp")
local luasnip = require("luasnip")

blink.setup({
  cmdline = { enabled = false },
  snippets = { preset = "luasnip" },
  sources = {
    providers = {
      path = {
        module = "blink.cmp.sources.path",
        opts = {
          -- ignore_root_slash = true,
        },
      },
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
    default = { "lsp", "path", "snippets", "buffer" },
    per_filetype = {
      org = { "lsp", "path", "snippets", "orgmode" },
      markdown = { "lsp", "path", "snippets" },
    },
  },
  keymap = {
    preset = "default",
    -- ["<C-Cr>"] = { "select_and_accept" },
  },
})

luasnip.setup({
  luasnip.filetype_extend("org", { "tex" }),
})
