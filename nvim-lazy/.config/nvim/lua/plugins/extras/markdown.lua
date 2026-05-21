return {
  {
    "MeanderingProgrammer/render-markdown.nvim",
    lazy = true,
    enabled = true,
    ft = "markdown",
    dependencies = {
      {
        "lukas-reineke/headlines.nvim",
        lazy = true,
        opts = {},
      },
      {
        "willchao612/vim-diagon",
        lazy = true,
      },
      {
        "whammou/vim-grip",
        lazy = true,
        keys = {
          { "<leader>mr", "<cmd>GripStart<cr>", desc = "Render markdown" },
        },
      },
      {
        "tadmccorkle/markdown.nvim",
        lazy = true,
        opts = {
          mappings = {
            link_follow = "gm",
          },
        },
      },
    },
    config = function()
      require("config.markdown")
    end,
  },
}
