require("render-markdown").setup({
  anti_conceal = {
    enabled = true,
    ignore = {},
  },
  -- Prevent the plugin from overriding concealcursor to '' (which disables cursor-line conceal)
  win_options = {
    conceallevel = {
      default = 3,
      rendered = 3,
    },
    concealcursor = {
      rendered = "nc",
      default = "nc",
    },
  },
  completions = {
    blink = { enabled = true },
    lsp = { enabled = true },
  },
  paragraph = {
    enabled = true,
    left_margin = 0,
    indent = 0,
  },
  heading = {
    enabled = false,
    position = "inline",
    border = false,
    border_virtual = false,
  },
  indent = {
    enabled = false,
    skip_heading = true,
    per_level = 1,
    skip_level = 0,
    icon = "",
  },

  latex = {
    enabled = true,
  },

  html = {
    enabled = true,
  },
})


