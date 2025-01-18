return {
    {
        'nvim-treesitter/nvim-treesitter',
        config = function()
            require('nvim-treesitter.configs').setup({
                ensure_installed = { 'org', 'html', 'latex', 'markdown', 'python', 'bash', 'fish', 'vim', 'vimdoc'},
                highlight = { enable = true },
            })
        end,
    }
}
