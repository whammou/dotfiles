local dir = require("config.orgmode.directories")
local base_dir = dir.base_dir
local Snacks = require("snacks")

require("orgmode").setup({
  org_agenda_files = { base_dir .. "**/*.org", base_dir .. "**/.logs/**/*.org" },
})

vim.api.nvim_create_autocmd("BufWinEnter", {
  pattern = "orgagenda",
  once = true,
  callback = function()
    vim.defer_fn(function()
      Snacks.bufdelete.other()
      vim.cmd.only()
      vim.cmd("set foldmethod=indent")
    end, 0)
  end,
})
