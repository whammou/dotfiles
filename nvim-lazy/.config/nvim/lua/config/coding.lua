local blink = require("blink.cmp")
local luasnip = require("luasnip")

require("snippets.snippets")

vim.keymap.set({ "i", "s" }, "<C-n>", function()
  if luasnip.choice_active() then
    luasnip.change_choice(1)
  end
end)

vim.keymap.set({ "i", "s" }, "<C-p>", function()
  if luasnip.choice_active() then
    luasnip.change_choice(-1)
  end
end)

blink.setup({
  fuzzy = { implementation = "rust" },
  cmdline = { enabled = false },
  snippets = {
    preset = "luasnip",
  },
  completion = {
    trigger = {
      show_on_keyword = false,
      show_on_trigger_character = true,
    },
    ghost_text = {
      enabled = true,
      show_with_selection = true,
      show_without_selection = true,
      show_with_menu = true,
    },
  },
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
        opts = {
          use_label_description = true,
        },
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
  },
})
