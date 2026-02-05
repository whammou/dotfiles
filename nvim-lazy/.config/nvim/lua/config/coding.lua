local blink = require("blink.cmp")
local luasnip = require("luasnip")

blink.setup({
  cmdline = { enabled = false },
  snippets = { preset = "luasnip" },
  sources = {
    providers = {
      lsp = {
        name = "LSP",
        module = "blink.cmp.sources.lsp",
        fallbacks = { "path" },
        opts = { tailwind_color_icon = "██" },
        async = true,
        transform_items = nil,
      },
      path = {
        module = "blink.cmp.sources.path",
        async = true,
        opts = {
          trailing_slash = true,
          label_trailing_slash = true,
          get_cwd = function()
            return vim.fn.getcwd()
          end,
          show_hidden_files_by_default = true,
          ignore_root_slash = false,
        },
      },
      snippets = {
        async = true,
        name = "luasnip",
        enabled = true,
      },
      orgmode = {
        async = true,
        name = "Orgmode",
        module = "orgmode.org.autocompletion.blink",
        fallbacks = { "path" },
      },
    },
    default = { "lsp", "path", "snippets", "buffer" },
    per_filetype = {
      org = { "lsp", "path", "snippets" },
      markdown = { "lsp", "path", "snippets" },
    },
  },
  keymap = {
    preset = "default",
    -- ["<C-Cr>"] = { "select_and_accept" },
  },
})

--luasnip.setup({
--  luasnip.filetype_extend("org", { "tex" }),
--})
