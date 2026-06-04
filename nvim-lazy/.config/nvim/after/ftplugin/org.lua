vim.opt_local.formatoptions:remove({ "c", "r", "o" })
vim.opt_local.foldlevel = 0
vim.opt_local.foldlevelstart = 1
vim.opt_local.foldminlines = 1
vim.opt_local.cmdheight = 0
vim.opt_local.wrap = true

vim.opt_local.spell = true
vim.opt_local.spelllang = "en"
vim.opt_local.breakindent = true
vim.opt_local.linebreak = true
vim.opt_local.breakindentopt = "list:-1"
vim.opt_local.formatlistpat = [[^\s*\%([-+*]\s\+\|\d\+\.\s\+\|[a-zA-Z]\+\.\s\+\)]]
vim.opt_local.showbreak = "NONE"
vim.opt_local.conceallevel = 3
vim.opt_local.concealcursor = "nc"

vim.keymap.set("n", "<leader>og", function()
  vim.fn.jobstart("qutebrowser_quick http://192.168.0.104:5173", { detach = true })
end, { desc = "org graph" })

vim.api.nvim_create_autocmd("FileType", {
  pattern = "org",
  callback = function()
    vim.keymap.set("i", "<S-CR>", '<cmd>lua require("orgmode").action("org_mappings.meta_return")<CR>', {
      silent = true,
      buffer = true,
    })
  end,
})

vim.api.nvim_create_autocmd("BufEnter", {
  pattern = "org-roam-select",
  callback = function()
    vim.b.completion = false
  end,
})

local org_roam_augroup = vim.api.nvim_create_augroup("OrgRoamFileTypeGroup", { clear = true })

vim.api.nvim_create_autocmd("BufReadPost", {
  group = org_roam_augroup,
  pattern = "*",
  callback = function()
    if vim.bo.filetype == "org-roam-node-buffer" then
      vim.bo.filetype = "org"
    end
  end,
})

vim.api.nvim_create_autocmd("BufEnter", {
  group = org_roam_augroup,
  pattern = "*",
  callback = function()
    if vim.bo.filetype == "org-roam-node-buffer" then
      vim.bo.filetype = "org"
    end
  end,
})

-- OrgFiletags: interactive fzf-lua picker for #+FILETAGS search
vim.api.nvim_create_user_command('OrgFiletags', function(opts)
  require('config.orgmode.filetags').OrgFiletags(opts.args)
end, { nargs = '?', desc = 'Search org files by #+FILETAGS (interactive fzf-lua picker)' })

vim.keymap.set('n', '<leader>oF', ':OrgFiletags<CR>', {
  desc = 'Org Filetags (fzf-lua)',
  buffer = true,
  silent = true,
})

