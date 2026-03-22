local ls = require("luasnip")

local s = ls.snippet
local t = ls.text_node
local i = ls.insert_node
local f = ls.function_node

local function uuid()
  return f(function()
    return vim.fn.systemlist("uuidgen")[1]
  end, {})
end

local function current_date(format)
  return f(function()
    return os.date(format or "%Y-%m-%d")
  end, {})
end

local function current_time(format)
  return f(function()
    return os.date(format or "%H:%M")
  end, {})
end

ls.add_snippets("org", {
  s("*1", {
    t("* "),
    i(1, "Title"),
    t({ "", ":PROPERTIES:", ":ID: " }),
    uuid(),
    t({ "", ":END:", "" }),
    i(0),
  }, { desc = "Level 1 header" }),

  s("*2", {
    t("** "),
    i(1, "Title"),
    t({ "", ":PROPERTIES:", ":ID: " }),
    uuid(),
    t({ "", ":END:", "" }),
    i(0),
  }, { desc = "Level 2 header" }),

  s("*3", {
    t("*** "),
    i(1, "Title"),
    t({ "", ":PROPERTIES:", ":ID: " }),
    uuid(),
    t({ "", ":END:", "" }),
    i(0),
  }, { desc = "Level 3 header" }),

  s("*4", {
    t("**** "),
    i(1, "Title"),
    t({ "", ":PROPERTIES:", ":ID: " }),
    uuid(),
    t({ "", ":END:", "" }),
    i(0),
  }, { desc = "Level 4 header" }),

  s("*5", {
    t("***** "),
    i(1, "Title"),
    t({ "", ":PROPERTIES:", ":ID: " }),
    uuid(),
    t({ "", ":END:", "" }),
    i(0),
  }, { desc = "Level 5 header" }),

  s("*6", {
    t("****** "),
    i(1, "Title"),
    t({ "", ":PROPERTIES:", ":ID: " }),
    uuid(),
    t({ "", ":END:", "" }),
    i(0),
  }, { desc = "Level 6 header" }),

  s("*OB", {
    t("*OBJECTIVE:* "),
    i(0),
  }, { desc = "OBJECTIVE" }),

  s("*Id", {
    t("*Idea:* /"),
    i(1, "idea"),
    t("/ "),
    i(0),
  }, { desc = "Idea" }),

  s("*Vi", {
    t("*Visit:* "),
    i(0),
  }, { desc = "Visit" }),

  s("*Re", {
    t("*Reference:* "),
    i(0),
  }, { desc = "Reference" }),

  s("*Im", {
    t("*Implemented:* "),
    i(0),
  }, { desc = "Implemented" }),

  s("*Ch", {
    t("*Check-out:* "),
    i(0),
  }, { desc = "Check-out" }),

  s("*Ke", {
    t("*Keypoint:* "),
    i(0),
  }, { desc = "Keypoint" }),

  s("*Wo", {
    t("*Workaround:* "),
    i(0),
  }, { desc = "Workaround" }),

  s("*So", {
    t("*Solution:* "),
    i(0),
  }, { desc = "Solution" }),

  s("*Is", {
    t("*Issue:* "),
    i(0),
  }, { desc = "Issue" }),

  s("*Cp", {
    t("*Checkpoint:* "),
    i(0),
  }, { desc = "Checkpoint" }),

  s("*FM", {
    t("*FMI:* "),
    i(0),
  }, { desc = "FMI" }),

  s("+", {
    t("+"),
    i(1, "property"),
    t(": "),
    i(0),
  }, { desc = "Property" }),

  s("+[ ]", {
    t("- [ ] "),
    i(0),
  }, { desc = "Checkbox" }),

  s("+-", {
    t("- "),
    i(0),
  }, { desc = "List item" }),

  s("+1.", {
    t("1. "),
    i(0),
  }, { desc = "Numbered list" }),

  s("+HL", {
    t("-----"),
    i(0),
  }, { desc = "Horizontal line" }),

  s(":PROP", {
    t({ ":PROPERTIES:", ":ID: " }),
    uuid(),
    t({ "", ":END:", "" }),
    i(0),
  }, { desc = "Property drawer" }),

  s(":ID", {
    t(":ID: "),
    uuid(),
    i(0),
  }, { desc = "ID property" }),

  s(":", {
    t(":"),
    i(1, "PROPERTY"),
    t(": "),
    i(0),
  }, { desc = "Property" }),

  s(".", {
    t("."),
    i(0),
  }, { desc = "Date/time" }),

  s(".S", {
    t("SCHEDULED: <"),
    current_date("%Y-%m-%d"),
    t(">"),
    i(0),
  }, { desc = "Scheduled" }),

  s(".D", {
    t("DEADLINE: <"),
    current_date("%Y-%m-%d"),
    t(">"),
    i(0),
  }, { desc = "Deadline" }),

  s("[[", {
    t("[["),
    i(1, "link"),
    t("]["),
    i(2, "desc"),
    t("]]"),
    i(0),
  }, { desc = "Hyperlink" }),

  s("#", {
    t("#"),
    i(1, "TODO"),
    t(" "),
    i(0),
  }, { desc = "TODO keyword" }),

  s("#+BEGIN", {
    i(1, "type"),
    t({ "", "" }),
    i(2),
    t({ "", "#+END_" }),
    i(3, "type"),
    i(0),
  }, { desc = "Begin/end block" }),

  s("#+BEGIN_QUOTE", {
    t({ "#+BEGIN_QUOTE", "" }),
    i(1),
    t({ "", "#+END_QUOTE", "" }),
    i(0),
  }, { desc = "Quote block" }),

  s("#+BEGIN_SRC", {
    t("#+BEGIN_SRC "),
    i(1, "language"),
    t({ "", "" }),
    i(2),
    t({ "", "#+END_SRC", "" }),
    i(0),
  }, { desc = "Source block" }),

  s("#+BEGIN_EXAMPLE", {
    t({ "#+BEGIN_EXAMPLE", "" }),
    i(1),
    t({ "", "#+END_EXAMPLE", "" }),
    i(0),
  }, { desc = "Example block" }),

  s("#+HTML", {
    t({ "#+begin_html html", "" }),
    i(1),
    t({ "", "#+end_html", "" }),
    i(0),
  }, { desc = "HTML block" }),

  s("#+HTML_IMG", {
    t({ "#+begin_html html", "" }),
    t('<img src="'),
    i(1, "URL"),
    t('" style="'),
    i(2, "width:50%;"),
    t('"/>'),
    t({ "", "#+end_html" }),
    i(0),
  }, { desc = "HTML image" }),

  s("#+NAME", {
    t("#+NAME: "),
    i(0),
  }, { desc = "Named block" }),

  s("#+FILETAGS", {
    t("#+FILETAGS: "),
    i(0),
  }, { desc = "File tags" }),

  s("#+TITLE", {
    t("#+TITLE: "),
    i(0),
  }, { desc = "Title" }),

  s("#+LOGBOOK", {
    t({
      "#+NAME:LOGBOOK",
      "#+HTML:<details>",
      "#+HTML:<summary>LOGBOOK</summary>",
      ":LOGBOOK:",
      ":END:",
      "#+HTML:</details>",
    }),
    i(0),
  }, { desc = "Logbook" }),

  s("#+NOTE", {
    t({ "-----", "" }),
    t("- Note taken on ["),
    current_date("%Y-%m-%d"),
    t(" "),
    current_time("%H:%M"),
    t({ "]: ", "" }),
    i(0),
    t({ "", "-----", "" }),
  }, { desc = "Dated note" }),

  s("#+TASK", {
    i(1, "Title"),
    t({ "", "- *OBJECTIVE:* " }),
    i(2),
    t({ "", "-----", "" }),
    t({
      "#+NAME:LOGBOOK",
      "#+HTML:<details>",
      "#+HTML:<summary>LOGBOOK</summary>",
      ":LOGBOOK:",
      ":END:",
      "#+HTML:</details>",
      "-----",
      "",
    }),
    i(0),
  }, { desc = "Recurring task" }),

  s("GN", {
    t({ "", "#+NAME:" }),
    i(1, "Block"),
    t({ "", "#+BEGIN_QUOTE markdown", "[!NOTE]", "" }),
    i(2),
    t({ "", "#+END_QUOTE" }),
    i(0),
  }, { desc = "GitHub NOTE" }),

  s("GW", {
    t({ "", "#+NAME:" }),
    i(1, "Block"),
    t({ "", "#+BEGIN_QUOTE markdown", "[!WARNING]", "" }),
    i(2),
    t({ "", "#+END_QUOTE" }),
    i(0),
  }, { desc = "GitHub WARNING" }),

  s("GI", {
    t({ "", "#+NAME:" }),
    i(1, "Block"),
    t({ "", "#+BEGIN_QUOTE markdown", "[!IMPORTANT]", "" }),
    i(2),
    t({ "", "#+END_QUOTE" }),
    i(0),
  }, { desc = "GitHub IMPORTANT" }),

  s("GT", {
    t({ "", "#+NAME:" }),
    i(1, "Block"),
    t({ "", "#+BEGIN_QUOTE markdown", "[!TIP]", "" }),
    i(2),
    t({ "", "#+END_QUOTE" }),
    i(0),
  }, { desc = "GitHub TIP" }),

  s("GC", {
    t({ "", "#+NAME:" }),
    i(1, "Block"),
    t({ "", "#+BEGIN_QUOTE markdown", "[!CAUTION]", "" }),
    i(2),
    t({ "", "#+END_QUOTE" }),
    i(0),
  }, { desc = "GitHub CAUTION" }),

  s("details", {
    t({ "#+NAME:" }),
    i(1, "Details"),
    t({ "", "#+html:<details>", "#+html:<summary><b>" }),
    i(2, "Summary"),
    t({ "</b></summary>", "" }),
    i(3),
    t({ "", "#+html:</details>", "" }),
    i(0),
  }, { desc = "Collapsible" }),

  s("zh", {
    t({ "#+TITLE: " }),
    i(1, "Title"),
    t({ "", "#+FILETAGS: :ZK:" }),
    i(2, "Tags"),
    t({ ":", "" }),
    t({ "#+HTML:<details>", "" }),
    t("* "),
    i(3, "Title"),
    t({ " :ZK:" }),
    i(4, "Tags"),
    t({ ":", "" }),
    t({ "", "#+HTML:</details>", "" }),
    i(0),
  }, { desc = "Zettelkasten" }),

  s("dh", {
    t("#+FILETAGS: :typDoc:meta:"),
    i(2, "Tags"),
    t({ ":", "" }),
    t({ "#+HTML:<details>", "" }),
    t("* "),
    i(1, "Title"),
    t({ " :DOC:META:" }),
    i(3, "Tags"),
    t({ ":", "" }),
    t({ "", "#+HTML:</details>", "" }),
    i(0),
  }, { desc = "Doc header" }),

  s("$$", {
    t("$$"),
    i(1),
    t("$$ "),
    i(0),
  }, { desc = "Inline LaTeX" }),

  s("\\[", {
    t({ "\\[", "" }),
    i(1),
    t({ "", "\\]" }),
    i(0),
  }, { desc = "Display LaTeX" }),
})
