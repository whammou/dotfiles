return {
  {
    "saghen/blink.cmp",
    lazy = true,
    config = function()
      require("config.coding")
    end,
    dependencies = {
      "L3MON4D3/LuaSnip",
      lazy = true,
      config = function()
        require("config.coding")
      end,
    },
  },
}
