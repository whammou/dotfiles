return {
  {
    "MeanderingProgrammer/render-markdown.nvim",
    lazy = true,
    ft = "markdown",
    dependencies = {
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
    opts = {
      completions = { blink = { enabled = true } },
      paragraph = {
        enabled = true,
        left_margin = 0,
        indent = 0,
      },
      heading = {
        position = "overlay",
        border = true,
        border_virtual = true,
      },
      indent = {
        enabled = true,
        skip_heading = true,
        per_level = 1,
        skip_level = 0,
        icon = "",
      },

      latex = {
        enabled = true,
      },

      html = {
        enabled = true,
      },
    },
  },
}
