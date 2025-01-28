return {
  {
    "willchao612/vim-diagon",
    lazy = true,
    ft = "markdown",
  },

  {
    "whammou/vim-grip",
    lazy = true,
    event = "VeryLazy",
    ft = "markdown",
  },

  {
    "tadmccorkle/markdown.nvim",
    lazy = true,
    ft = "markdown",
    opts = {
      mappings = {
        link_follow = "gm",
      },
    },
  },

  {
    "MeanderingProgrammer/render-markdown.nvim",
    lazy = true,
    ft = "markdown",
    opts = {},
  },
}
