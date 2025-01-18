return {

    {
        'navarasu/onedark.nvim',
        lazy = false,
        priority = 1000,
        opts = {
            style = 'deep',
        },
    },

    {
        'folke/tokyonight.nvim',
        lazy = false,
        priority = 1000,
        opts ={
            style = 'night',
        }
    },

    {
        'nvim-lualine/lualine.nvim',
        opts = {
            always_show_tabline = true,
            tabline = {
                lualine_a = {'buffers'},
            },
        },
    },

--    'vim-airline/vim-airline',
--    'vim-airline/vim-airline-themes',

}
