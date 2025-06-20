return {
  {
    "chipsenkbeil/org-roam.nvim",
    lazy = true,
    ft = "org",
    dependencies = {
      {
        "nvim-orgmode/orgmode",
        lazy = true,
        config = function()
          require("config.extras.orgroam")
        end,
      },
      {
        "BartSte/nvim-khalorg",
        lazy = true,
      },
      {
        "nvim-orgmode/org-bullets.nvim",
        lazy = true,
        config = true,
      },
      {
        "lukas-reineke/headlines.nvim",
        lazy = true,
        opts = {
          markdown = {
            headline_highlights = false,
            bullets_highlights = false,
            codeblock_highlight = false,
            dash_highlight = false,
            quote_highlight = false,
          },
          org = {
            headline_highlights = { "Headline" },
          },
        },
      },
    },

    config = function()
      require("config.extras.orgroam")
    end,
  },
}
