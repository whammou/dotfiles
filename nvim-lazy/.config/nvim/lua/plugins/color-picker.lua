return {
  {
    "ibhagwan/fzf-lua",
    keys = {
      {
        "<leader>Cg",
        function()
          require("custom.color-picker").pick()
        end,
        desc = "Colorscheme Color Picker",
      },
    },
  },
}
