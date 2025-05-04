return {
  {
    "akinsho/bufferline.nvim",
    opts = {
      options = {
        always_show_bufferline = true,
        hover = {
          enabled = true,
          delay = 200,
          reveal = { "close" },
        },
      },
      highlights = {
        close_button_selected = {
          fg = "#1a212e",
        },
        fill = {
          bg = "#283347",
        },
      },
    },
  },
  {
    "nvim-lualine/lualine.nvim",
    opts = {
      sections = {
        lualine_z = { "lsp_status" },
      },
    },
  },
}
