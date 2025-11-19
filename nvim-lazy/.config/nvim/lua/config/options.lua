-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

local opt = vim.opt

vim.opt.title = true
vim.opt.titlelen = 0 -- do not shorten title
vim.opt.titlestring = "%t - "

opt.autochdir = true
opt.sessionoptions = "blank,buffers,curdir,folds,globals,help,tabpages,winsize,winpos,terminal,localoptions,resize"

--opt.foldmethod = "indent"
--opt.foldtext = ""

--opt.foldmethod = "expr"
--opt.foldexpr = "v:vim.treesitter.foldexpr()"
opt.foldlevel = 99
opt.fillchars = [[diff:╱,eob: ,fold: ,foldclose: ,foldopen:,foldsep: ]]

vim.o.shell = "fish"
-- opts.rocks.hererocks = false

-- Animation
vim.g.snacks_animate = false -- Turn off snacks animation

-- Markdown
vim.g.markdown_folding = 0 -- Disable built-in markdown folding
