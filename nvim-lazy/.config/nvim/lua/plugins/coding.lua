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
    version = "1.*",
    event = "InsertEnter",
    dependencies = {
      "L3MON4D3/LuaSnip",
    },
  },
  {
    "bfredl/nvim-luadev",
  },
}
