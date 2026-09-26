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
  signature = { enabled = false },
  completion = {
    list = {
      max_items = 50,
      selection = {
        preselect = false,
        auto_insert = false,
      },
    },
    trigger = {
      prefetch_on_insert = true,
      show_on_keyword = false,
      show_on_trigger_character = true,
      show_on_blocked_trigger_characters = { " ", "\n", "\t" },
      show_on_x_blocked_trigger_characters = { "'", '"', "(" },
      show_on_insert = false,
      show_on_backspace = false,
      show_on_backspace_in_keyword = false,
      show_on_backspace_after_accept = false,
      show_on_backspace_after_insert_enter = false,
      show_on_accept_on_trigger_character = true,
      show_on_insert_on_trigger_character = true,
    },
    documentation = {
      auto_show = false,
      auto_show_delay_ms = 500,
      treesitter_highlighting = false,
    },
    ghost_text = {
      enabled = false,
    },
    accept = {
      auto_brackets = { enabled = false },
    },
    menu = {
      max_height = 10,
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
        min_keyword_length = 1,
        transform_items = nil,
      },
      buffer = {
        max_items = 5,
        min_keyword_length = 3,
        opts = {
          get_bufnrs = function()
            return vim.tbl_filter(function(b)
              return vim.bo[b].buflisted
            end, vim.api.nvim_list_bufs())
          end,
        },
      },
      omni = {
        module = "blink.cmp.sources.complete_func",
        async = true,
        min_keyword_length = 2,
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
        min_keyword_length = 0,
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
        min_keyword_length = 1,
        opts = {
          use_label_description = true,
        },
      },
      orgmode = {
        async = true,
        name = "Orgmode",
        module = "orgmode.org.autocompletion.blink",
        fallbacks = { "path" },
        min_keyword_length = 2,
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
