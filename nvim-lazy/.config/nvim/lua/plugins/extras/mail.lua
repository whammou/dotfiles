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
    -- lazy = true,
    -- event = { "FileType markdown", "FileType mail" },
    ft = { "markdown", "mail" },
    config = function()
      require("config.mail")
    end,
  },
  {
    "Konfekt/vim-notmuch-addrlookup",
    ft = { "mail", "markdown", "org" },
    init = function()
      vim.g.notmuch_filter = 1
      vim.g.notmuch_filetypes = { "mail", "markdown", "org" }
    end,
  },
}
