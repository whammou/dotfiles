return {
  {
    "yousefakbar/notmuch.nvim",
    config = function()
      require("notmuch").setup({
        render_html_body = true,
      })
    end,
  },
  {
    "neomutt/neomutt.vim",
    lazy = true,
  },
  {
    "martineausimon/nvim-mail-merge",
    lazy = true,
    event = { "FileType markdown", "FileType mail" },
    config = function()
      require("config.mail")
    end,
  },
  {
    "Konfekt/vim-notmuch-addrlookup",
    lazy = true,
    event = "FileType mail",
    init = function()
      vim.g.notmuch_filter = 1
    end,
  },
}
