return { 
  {
    "folke/noice.nvim",
    event = "VeryLazy",
    opts = {
      presets = {
        long_message_to_split = true,
      },
    },
    dependencies = {
      "MunifTanjim/nui.nvim",
      { 
        "rcarriaga/nvim-notify",
        opts = {
          stages = "static",
        },
      }
    },
  },
}
