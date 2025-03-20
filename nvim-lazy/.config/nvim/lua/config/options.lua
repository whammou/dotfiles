-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

local opt = vim.opt

-- Vim
opt.autochdir = true
-- opts.rocks.hererocks = false

-- Animation
vim.g.snacks_animate = false -- Turn off snacks animation

-- Markdown
vim.g.markdown_folding = 1
