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
      {
        "MunifTanjim/nui.nvim",
      },

      { 
        "rcarriga/nvim-notify",
        opts = {
          stages = "static",
        },
      }
    },
  },
}
