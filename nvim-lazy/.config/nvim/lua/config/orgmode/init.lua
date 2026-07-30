local dir = require("config.orgmode.directories")
local base_dir = dir.base_dir
local date = os.date("%y%m")
local Menu = require("org-modern.menu")

require("orgmode").setup({
  org_agenda_files = { base_dir .. "**/*.org" },
  org_agenda_text_search_extra_files = { "agenda-archives" },
  org_agenda_current_time_string = " now ────────",
  org_agenda_hide_empty_blocks = true,
  org_agenda_remove_tags = true,
  org_default_notes_file = base_dir .. "capture.org",
  org_log_into_drawer = "LOGBOOK",
  org_highlight_latex_and_related = "entities",
  org_use_property_inheritance = true,
  org_archive_location = "./.logs/" .. date .. "/archive_%s",
  org_agenda_time_grid = {
    times = vim.tbl_map(function(x)
      return x * 100
    end, vim.fn.range(24)),
    time_separator = "─────",
    time_label = "──────────────",
  },
  org_return_uses_meta_return = false,
  org_ellipsis = "",
  org_hide_leading_stars = false,
  org_hide_emphasis_markers = true,
  org_adapt_indentation = false,
  org_startup_indented = false,
  org_startup_folded = "inherit",
  win_split_mode = "auto",
  win_border = "single",
  org_id_link_to_org_use_id = true,
  org_use_tag_inheritance = true,
  org_tags_exclude_from_inheritance = { "meta" },
  org_tags_column = 0,
  org_cycle_separator_lines = 0,
  org_blank_before_new_entry = { heading = false, plain_list_item = false },
  org_priority_highest = "A",
  org_priority_default = "D",
  org_priority_lowest = "F",
  org_deadline_warning_days = 7,
  org_todo_repeat_to_state = "RECR",
  org_todo_keywords = {
    "TODO(t)", "OPEN(y)", "DOIN(d)", "PROG(g)", "INTR(q)", "(e)",
    "PEND(p)", "OUTL(o)", "WAIT(w)", "EXPL(x)", "FDBK(b)", "NEXT(n)",
    "TARGET(g)", "IDEA(i)", "TEST(s)", "RECR(l)", "|",
    "PRTL(r)", "DONE(f)", "RVIW(v)", "ABRT(a)", "CLSD(c)",
  },
  input = { use_vim_ui = true },
  folds = { colored = true },

  org_todo_keyword_faces = {
    TODO = ":foreground #775289 :weight bold :slant italic",
    OPEN = ":foreground #775289 :weight bold :slant italic",
    RECR = ":foreground #775289 :weight bold :slant italic",
    DOIN = ":foreground #3F717B :weight bold :slant italic",
    PROG = ":foreground #607857 :weight bold :slant italic",
    PEND = ":foreground #5c6370 :weight bold :slant italic",
    OUTL = ":foreground #5c6370 :weight bold :slant italic",
    IDEA = ":foreground #5c6370 :weight bold :slant italic",
    INTR = ":foreground #6e594f :weight bold :slant italic",
    WAIT = ":foreground #6e594f :weight bold :slant italic",
    EXPL = ":foreground #6e594f :weight bold :slant italic",
    FDBK = ":foreground #6e594f :weight bold :slant italic",
    TEST = ":foreground #6e594f :weight bold :slant italic",
    NEXT = ":foreground #456E92 :weight bold :slant italic",
    TARGET = ":foreground #775289 :weight bold :slant italic",
    RVIW = ":foreground #e5c07b :weight bold :slant italic",
    PRTL = ":foreground #e5c07b :weight bold :slant italic",
    ABRT = ":foreground #e86671 :weight bold :slant italic",
    DONE = ":foreground #98c379 :weight bold :slant italic",
    CLSD = ":foreground #5c6370 :weight bold :slant italic",
  },

  ui = {
    agenda = {
      preview_window = {
        wrap = true,
        border = "single",
        anchor_bias = "above",
        focusable = true,
      },
    },
    menu = {
      handler = function(data)
        Menu:new({
          window = {
            margin = { 1, 0, 1, 0 },
            padding = { 0, 1, 0, 1 },
            title_pos = "center",
            border = "single",
            zindex = 1000,
          },
          icons = {
            separator = "➜",
          },
        }):open(data)
      end,
    },
  },

  mappings = {
    global = {
      org_capture = "<leader>oc",
    },
    org = {
      org_cycle = false,
      org_toggle_checkbox = "<Leader>oC",
      org_return = false,
    },
  },
  agenda = {
    preview_window = {
      border = "single",
    },
  },
})

-- Patch OrgMarkup.has_valid_parent to allow emphasis inside block contents.
-- nvim-orgmode's emphasis highlighter only scans paragraphs, but inside blocks
-- exprs are direct children of (contents). Without this, *bold* /italic/ etc.
-- inside #+begin_quote blocks are plain text, not highlighted.
do
  local ok, OrgMarkup = pcall(require, 'orgmode.colors.highlighter.markup')
  if ok then
    local orig = OrgMarkup.has_valid_parent
    function OrgMarkup:has_valid_parent(item)
      local parent = item.node:parent()
      if not parent then return false end

      parent = parent:parent()
      if not parent then return false end

      if parent:type() == 'paragraph' or parent:type() == 'link_desc' then
        return true
      end

      -- Allow emphasis inside quote/block contents (expr → contents → block)
      if parent:type() == 'contents' then
        local p = parent:parent()
        if p and (p:type() == 'block' or p:type() == 'dynamic_block') then
          return true
        end
      end

      return orig(self, item)
    end
  end
end

return {
  require("config.orgmode.server"),
  require("config.orgmode.highlights"),
  require("config.orgmode.ui"),
  require("config.orgmode.options"),
  require("config.orgmode.roam"),
  require("config.orgmode.editor"),
  require("config.orgmode.goto_id"),
  require("config.orgmode.hyperlinks"),
  require("config.orgmode.exports"),
  require("config.orgmode.agenda"),
}
