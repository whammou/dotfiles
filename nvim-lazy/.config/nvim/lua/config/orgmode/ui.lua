local Menu = require("org-modern.menu")

require("orgmode").setup({
  ui = {
    agenda = {
      preview_window = {
        wrap = true,
        border = "single",
      },
    },
    menu = {
      handler = function(data)
        Menu:new({
          window = {
            margin = { 1, 0, 1, 0 },
            padding = { 0, 1, 0, 1 },
            title_pos = "center",
            border = "single",
            zindex = 1000,
          },
          icons = {
            separator = "➜",
          },
        }):open(data)
      end,
    },
  },
})
