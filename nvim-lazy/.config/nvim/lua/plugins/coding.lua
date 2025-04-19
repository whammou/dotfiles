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
        providers = {
          snippets = {
            name = "luasnip",
            enabled = true,
          },
        },
      },
    },
  },

  -- {
  --   "L3MON4D3/LuaSnip",

  --   config = function()
  --     require("luasnip.loaders.from_lua").load({ path = "~/.config/nvim/snippets/" })
  --   end,
  -- },
}
