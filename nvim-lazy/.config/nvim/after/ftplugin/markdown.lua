local opt = vim.opt
local opt_local = vim.opt_local

vim.opt_local.formatoptions:remove({ "c", "r", "o" })
vim.opt_local.foldlevel = 1
vim.opt_local.foldminlines = 1
vim.opt_local.cmdheight = 0
vim.opt_local.wrap = true

vim.opt_local.spell = true
vim.opt_local.spelllang = "en"
vim.opt_local.breakindent = true
vim.opt_local.linebreak = true
vim.opt_local.breakindentopt = "list:-1"
vim.opt_local.showbreak = "NONE"
vim.opt_local.conceallevel = 3
vim.opt_local.concealcursor = "nc"

function _G.markdown_foldexpr()
  local lnum = vim.v.lnum
  local line = vim.fn.getline(lnum)
  local heading = line:match("^(#+)%s")
  if heading then
    local level = #heading
    if level == 1 then
      -- Special handling for H1
      if lnum == 1 then
        return ">1"
      else
        local frontmatter_end = vim.b.frontmatter_end
        if frontmatter_end and (lnum == frontmatter_end + 1) then
          return ">1"
        end
      end
    elseif level >= 2 and level <= 6 then
      -- Regular handling for H2-H6
      return ">" .. level
    end
  end
  return "="
end

--vim.api.nvim_create_autocmd("BufWinEnter", {
--  callback = function()
--    if vim.bo.filetype == "markdown" then
--      vim.opt_local.formatoptions:remove({ "c", "r", "o" })
--      opt_local.foldlevel = 1
--      opt_local.foldmethod = "expr"
--      opt_local.foldexpr = "v:lua.markdown_foldexpr()"
--      -- opt.foldexpr = "v:lua.vim.treesitter.foldexpr()"
--
--      opt_local.breakindent = true
--      opt_local.breakindentopt = "list:-1"
--      vim.opt_local.showbreak = "NONE"
--      vim.opt_local.conceallevel = 3
--      vim.opt_local.concealcursor = "nc"
--      -- vim.o.formatlistpat = "-"
--    end
--  end,
--})
