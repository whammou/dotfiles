vim.opt.foldlevel = 1
vim.opt.foldminlines = 1
vim.opt.wrap = true
vim.opt.spell = true

vim.opt.breakindent = true
vim.opt.linebreak = true -- Remap for dealing with word wrap
vim.opt.breakindentopt = "list:-1"
vim.opt.formatlistpat = [[^\s*\%([-+*]\s\+\|\d\+\.\s\+\|[a-zA-Z]\+\.\s\+\)]]
vim.opt.showbreak = ""
--vim.opt.formatlistpat = [[^\s*[-*+]\s*\|\^\s*\d\+[.)]\s*]]
--vim.opt.formatlistpat = [[^\s*\%([-+*]\s\|\d\+\.\s\|[a-zA-Z]\+\.\s\)]]

--vim.opt.showbreak = string.rep(" ", 2) -- Make it so that long lines wrap smartly

vim.opt.conceallevel = 2
vim.opt.concealcursor = "nc"

local org_roam_augroup = vim.api.nvim_create_augroup("OrgRoamFileTypeGroup", { clear = true })

vim.api.nvim_create_autocmd("BufReadPost", {
  group = org_roam_augroup,
  pattern = "*", -- Apply to all files, then filter by filetype in the callback
  callback = function()
    if vim.bo.filetype == "org-roam-node-buffer" then
      vim.bo.filetype = "org"
      -- vim.notify("Org-roam buffer detected, filetype changed to 'org'.", vim.log.levels.INFO)
    end
  end,
  desc = "Change org-roam-node-buffer filetype to org on buffer read",
})

vim.api.nvim_create_autocmd("BufEnter", {
  group = org_roam_augroup,
  pattern = "*", -- Apply to all files, then filter by filetype in the callback
  callback = function()
    if vim.bo.filetype == "org-roam-node-buffer" then
      vim.bo.filetype = "org"
      -- vim.notify("Org-roam buffer detected, filetype changed to 'org' on buffer enter.", vim.log.levels.INFO)
    end
  end,
  desc = "Change org-roam-node-buffer filetype to org on buffer enter",
})
