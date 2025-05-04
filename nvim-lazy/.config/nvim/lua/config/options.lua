-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

local opt = vim.opt

-- Vim
opt.autochdir = true
opt.foldmethod = "indent"
vim.o.shell = "fish"
-- opts.rocks.hererocks = false

-- Animation
vim.g.snacks_animate = false -- Turn off snacks animation

-- Markdown
vim.g.markdown_folding = 0 -- Disable built-in markdown folding
