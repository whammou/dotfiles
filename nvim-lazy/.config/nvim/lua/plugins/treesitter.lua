return {
  {
    "nvim-treesitter/nvim-treesitter",
    opts = {
      ensure_installed = {
        "html",
        "latex",
        "markdown",
        "markdown_inline",
        "python",
        "bash",
        "fish",
        "vim",
        "vimdoc",
        "toml",
        "yaml",
      },
      ignore_install = { "org" },
      highlight = {
        enable = true,
        additional_vim_regex_highlighting = { "org" },
      },
    },
  },
}
