return {
  {
    "ibhagwan/fzf-lua",
    keys = {
      {
        "<leader>uC",
        function()
          require("custom.color-picker").pick()
        end,
        desc = "Colorscheme Color Picker",
      },
    },
  },
}
