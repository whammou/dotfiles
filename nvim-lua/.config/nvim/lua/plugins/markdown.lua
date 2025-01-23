return {
    {
        'willchao612/vim-diagon',
        event = "VeryLazy",
        ft = markdown,
    },

    {
        'whammou/vim-grip',
        event = "VeryLazy",
        ft = markdown,
    },

    {
        'tadmccorkle/markdown.nvim',
        event = "VeryLazy",
        ft = markdown,
        opts = {
          mappings = {
            link_follow = "gm",
          },
        },
    },

    {
        'MeanderingProgrammer/render-markdown.nvim',
        event = "VeryLazy",
        ft = markdown,
        opts = {},
    },

}
