return {
  -- {
  --   "L3MON4D3/LuaSnip",

  --   config = function()
  --     require("luasnip.loaders.from_lua").load({ path = "~/.config/nvim/snippets/" })
  --   end,
  -- },

  {
    "saghen/blink.cmp",
    lazy = true,

    dependencies = {
      "L3MON4D3/LuaSnip",
      lazy = true,
      opts = {},
    },

    opts = {
      snippets = { preset = "luasnip" },
      sources = {
        default = { "lsp", "path", "snippets", "buffer" },
      },
    },
  },
}
