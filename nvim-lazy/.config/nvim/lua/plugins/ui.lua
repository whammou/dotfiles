return {
  {
    "akinsho/bufferline.nvim",
    opts = {
      options = {
        hover = {
          enabled = true,
          delay = 200,
          reveal = { "close" },
        },
        always_show_bufferline = true,
      },

      highlights = {
        close_button_selected = {
          fg = "#1a212e",
        },
        fill = {
          bg = "#21283b",
        },
      },
    },
  },
}
