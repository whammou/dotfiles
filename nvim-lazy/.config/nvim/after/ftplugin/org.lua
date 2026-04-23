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

vim.api.nvim_create_autocmd("FileType", {
  pattern = "org",
  callback = function()
    vim.cmd([[
      syntax match orgAdmonitionWarning '\[!WARNING\]'
      syntax match orgAdmonitionCaution '\[!CAUTION\]'
      syntax match orgAdmonitionImportant '\[!IMPORTANT\]'
      syntax match orgAdmonitionTip '\[!TIP\]'
      syntax match orgAdmonitionNote '\[!NOTE\]'
      highlight link orgAdmonitionWarning WarningMsg
      highlight link orgAdmonitionCaution Error
      highlight link orgAdmonitionImportant Title
      highlight link orgAdmonitionTip String
      highlight link orgAdmonitionNote Identifier
    ]])
  end,
})
