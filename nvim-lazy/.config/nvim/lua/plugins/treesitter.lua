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
      "neovim-treesitter/treesitter-parser-registry",
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

      -- Defer activation so orgmode can set up folds first
      local function activate()
        vim.schedule(function()
          require("otter").activate()
        end)
      end

      local augroup = vim.api.nvim_create_augroup("otter_org", { clear = true })
      vim.api.nvim_create_autocmd("FileType", {
        group = augroup,
        pattern = "org",
        callback = activate,
      })

      -- Activate for the current buffer if already in an org file
      if vim.bo.filetype == "org" then
        activate()
      end
    end,
  },
}
