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
    list = {
      selection = {
        preselect = false,
        auto_insert = false,
      },
    },
    trigger = {
      show_on_keyword = false,
      show_on_trigger_character = true,
      show_on_blocked_trigger_characters = {},
      show_on_backspace = true,
      show_on_backspace_in_keyword = false,
      show_on_backspace_after_accept = true,
      show_on_backspace_after_insert_enter = true,
    },
    ghost_text = {
      enabled = false,
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
        fallbacks = { "buffer" },
        opts = { tailwind_color_icon = "██" },
        async = true,
        transform_items = nil,
      },
      omni = {
        module = "blink.cmp.sources.complete_func",
        async = true,
        enabled = function()
          return vim.bo.omnifunc ~= "v:lua.vim.lsp.omnifunc"
        end,
        opts = {
          complete_func = function()
            return vim.bo.omnifunc
          end,
        },
      },
      path = {
        module = "blink.cmp.sources.path",
        async = true,
        score_offset = 5,
        opts = {
          trailing_slash = true,
          label_trailing_slash = true,
          get_cwd = function()
            local buf_dir = vim.fn.expand("%:p:h")
            return buf_dir ~= "" and buf_dir or vim.fn.getcwd()
          end,
          show_hidden_files_by_default = true,
          ignore_root_slash = true,
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
      org = { "lsp", "path", "snippets", "omni" },
      markdown = { "lsp", "path", "snippets", "omni" },
      mail = { "omni" },
    },
  },
  keymap = {
    preset = "default",
    ["<C-j>"] = { "select_next", "fallback" },
    ["<C-k>"] = { "select_prev", "fallback" },
    ["<C-l>"] = { "select_and_accept", "fallback" },
  },
})
