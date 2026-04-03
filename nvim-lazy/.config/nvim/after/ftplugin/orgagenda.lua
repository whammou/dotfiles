vim.opt_local.formatoptions:remove({ "c", "r", "o" })
vim.opt_local.foldlevel = 1
vim.opt_local.foldminlines = 1
vim.opt_local.cmdheight = 0
vim.opt_local.wrap = true
vim.opt_local.spell = true
vim.opt_local.breakindent = true
vim.opt_local.linebreak = true
vim.opt_local.breakindentopt = "list:-1"
vim.opt_local.formatlistpat = [[^\s*\%([-+*]\s\+\|\d\+\.\s\+\|[a-zA-Z]\+\.\s\+\)]]
vim.opt_local.showbreak = "NONE"
vim.opt_local.conceallevel = 3
vim.opt_local.concealcursor = "nc"
