return {
  {
    "saghen/blink.cmp",
    lazy = true,
    dependencies = {
      "L3MON4D3/LuaSnip",
      lazy = true,
    },
    opts = {
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
    },
  },
}
