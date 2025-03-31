return {
  {
    "nvim-treesitter/nvim-treesitter",
    opts = {
      ensure_installed = {
        "html",
        "latex",
        "markdown",
        "python",
        "bash",
        "fish",
        "vim",
        "vimdoc",
        "toml",
        "yaml",
      },
      ignore_install = { "org" },
    },
  },
}
