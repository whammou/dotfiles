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
  {
    "jmbuhr/otter.nvim",
    lazy = true,
    ft = { "org" },
    dependencies = {
      "nvim-treesitter/nvim-treesitter",
    },
    opts = {
      lsp = {
        diagnostic_update_events = { "BufWritePost" },
      },
      buffers = {
        set_filetype = true,
        write_to_disk = false,
      },
      handle_leading_whitespace = true,
    },
    config = function(_, opts)
      require("otter").setup(opts)

      local augroup = vim.api.nvim_create_augroup("otter_org", { clear = true })
      vim.api.nvim_create_autocmd("FileType", {
        group = augroup,
        pattern = "org",
        callback = function()
          require("otter").activate()
        end,
      })

      -- Activate for the current buffer if already in an org file
      if vim.bo.filetype == "org" then
        require("otter").activate()
      end
    end,
  },
}
