local ls = require("luasnip")

require("snippets.org")

local s = ls.snippet
local t = ls.text_node
local i = ls.insert_node

ls.add_snippets("lua", {
  s("fn", {
    t("local function "),
    i(1, "name"),
    t("("),
    i(2, "params"),
    t(")"),
    t({ "", "  " }),
    i(0),
    t({ "", "end" }),
  }, {
    desc = "Lua local function",
  }),
  s("req", {
    t("local "),
    i(1, "name"),
    t(" = require(\""),
    i(2, "module"),
    t("\")"),
  }, {
    desc = "Lua require statement",
  }),
})

ls.add_snippets("markdown", {
  s("code", {
    t("```"),
    i(1, "language"),
    t({ "", "" }),
    i(0),
    t({ "", "```" }),
  }, {
    desc = "Fenced code block",
  }),
  s("link", {
    t("["),
    i(1, "text"),
    t("]("),
    i(2, "url"),
    t(")"),
  }, {
    desc = "Markdown link",
  }),
})

ls.add_snippets("lua", {
  s("log", {
    t({ "console.log(\"" }),
    i(1, "message"),
    t("\")" ),
    i(0),
  }, {
    desc = "Console log",
  }),
})

ls.add_snippets("javascript", {
  s("log", {
    t({ "console.log(\"" }),
    i(1, "message"),
    t("\")" ),
    i(0),
  }, {
    desc = "Console log",
  }),
})

ls.add_snippets("typescript", {
  s("log", {
    t({ "console.log(\"" }),
    i(1, "message"),
    t("\")" ),
    i(0),
  }, {
    desc = "Console log",
  }),
})

ls.add_snippets("python", {
  s("log", {
    t("print(\""),
    i(1, "message"),
    t("\")" ),
    i(0),
  }, {
    desc = "Print statement",
  }),
})
