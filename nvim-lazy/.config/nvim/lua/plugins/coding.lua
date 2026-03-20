return {
  {
    "L3MON4D3/LuaSnip",
    lazy = true,
    config = function()
      require("config.coding")
    end,
  },
  {
    "saghen/blink.cmp",
    lazy = true,
    dependencies = {
      "L3MON4D3/LuaSnip",
    },
  },
  {
    "bfredl/nvim-luadev",
  },
}
