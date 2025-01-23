return {
    {
      'SirVer/ultisnips',
      event = "VeryLazy",
      dependencies = {
        {
          "honza/vim-snippets",
          event = "VeryLazy",
        },
        {
          "ervandew/supertab",
          event = "VeryLazy",
        },
      },
    },

    {
      'neoclide/coc.nvim',
      branch = 'release',
      event = "VeryLazy",
    },
}
