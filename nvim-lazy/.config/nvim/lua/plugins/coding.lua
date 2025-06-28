return {
  {
    "saghen/blink.cmp",
    lazy = true,
    dependencies = {
      "L3MON4D3/LuaSnip",
      lazy = true,
    },
    config = function()
      require("config.coding")
    end,
  },
}
