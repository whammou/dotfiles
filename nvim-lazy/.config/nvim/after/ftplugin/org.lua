vim.opt_local.formatoptions:remove({ "c", "r", "o" })
vim.opt_local.foldlevel = 1
vim.opt_local.foldlevelstart = 98
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

-- Binding org-meta-return
vim.api.nvim_create_autocmd("FileType", {
  pattern = "org",
  callback = function()
    vim.keymap.set("i", "<S-CR>", '<cmd>lua require("orgmode").action("org_mappings.meta_return")<CR>', {
      silent = true,
      buffer = true,
    })
  end,
})

-- via an autocmd
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
  desc = "Change org-roam-node-buffer filetype to org on buffer read",
})

vim.api.nvim_create_autocmd("BufEnter", {
  group = org_roam_augroup,
  pattern = "*",
  callback = function()
    if vim.bo.filetype == "org-roam-node-buffer" then
      vim.bo.filetype = "org"
    end
  end,
  desc = "Change org-roam-node-buffer filetype to org on buffer enter",
})
