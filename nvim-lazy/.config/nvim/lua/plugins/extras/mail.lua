return {
  {
    "neomutt/neomutt.vim",
    lazy = true,
  },
  {
    "martineausimon/nvim-mail-merge",
    lazy = true,
    ft = { "markdown", "mail" },
    config = function()
      require("config.mail")
    end,
  },
}
