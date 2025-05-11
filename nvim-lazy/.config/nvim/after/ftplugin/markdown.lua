local opt = vim.opt

opt.foldlevel = 99
opt.foldmethod = "expr"
opt.foldexpr = "v:lua.require'lazyvim.util'.ui.foldexpr()"
