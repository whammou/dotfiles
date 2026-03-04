return {
  require("config.orgmode.server"),
  require("config.orgmode.highlights"),
  require("config.orgmode.ui"),
  require("config.orgmode.options"),
  require("config.orgmode.roam"),
  require("config.orgmode.editor"),
  require("config.orgmode.hyperlinks"),
  require("config.orgmode.exports"),
  require("config.orgmode.agenda"),

  --  vim.api.nvim_create_autocmd("FileType", {
  --    pattern = "org",
  --    callback = function()
  --      vim.cmd("Org agenda")
  --    end,
  --  }),
}
