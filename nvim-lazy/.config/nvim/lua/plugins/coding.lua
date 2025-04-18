return {
  {
    "saghen/blink.cmp",
    version = "1.*",
    dependencies = { "L3MON4D3/LuaSnip", version = "2.*" },
    opts = {
      snippets = { preset = "luasnip" },
      sources = {
        default = { "lsp", "path", "snippets", "buffer" },
        providers = {
          snippets = {
            name = "luasnip",
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
