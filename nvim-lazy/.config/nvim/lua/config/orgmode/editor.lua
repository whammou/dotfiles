local fzo = require("fzf-org")
local actions = require("fzf-org.actions")

fzo.setup({
  -- Default options for fzo.orgmode() (all other options inherit from this)
  orgmode = {
    whence = false, -- where we should have started from; false means don't care
    where = "*", -- where to search (options: "*" (all org files), "%" (current file), "." (current headline))
    what = "headline", -- what to search for

    color_icons = true, -- whether to colorize entries
    -- bullet_icons = { "◉", "○", "✸", "✿" }, -- how to display bullets
    bullet_icons = { "󰫃", "󰫄", "󰫅", "󰫆", "󰫇", "󰫈" },
    todo_icons = { -- how to display TODO
      default = "   ",
      TODO = "[ ]",
      NEXT = "[➔]",
      PEND = "[󰒲]",
      OUTL = "[]",
      EXPL = "[]",
      FDBK = "[󰅽]",
      IDEA = "[]",
      RECR = "[󰑖]",
      WAIT = "[…]",
      DOIN = "[~]",
      DONE = "[]",
      PRTL = "[󱍻]",
      RVIW = "[]",
      ABRT = "[⨯]",
    },
    show_tags = true, -- whether to display tags

    -- Other fzf-lua options (see its documentation)
    prompt = "Orgmode ❯ ",
    headers = { "actions" },
    actions = {
      -- Also inherits from fzf.actions.files, e.g., file_edit, file_split, etc.
      ["ctrl-y"] = { actions.yank_link, actions.resume },
    },
  },

  -- Function-specific options; these inherit from orgmode options (above)

  -- fzo.all_headlines()
  all_headlines = {
    -- Same default behavior as fzo.orgmode().
    --
    -- You can add options here to configure the behavior of fzo.all_headlines()
    -- without affecting other functions' inherited options.
  },

  -- fzo.files()
  files = {
    where = "*",
    what = "file",
    prompt = "Org files ❯ ",
  },

  -- fzo.headlines()
  headlines = {
    whence = "file",
    where = "%",
    what = "headline",
    prompt = "Org headlines ❯ ",
  },

  -- fzo.subheadlines()
  subheadlines = {
    whence = "file",
    where = ".",
    what = "headline",
    prompt = "Org headlines ❯ ",
  },

  -- fzo.refile()
  refile = {
    whence = "headline",
    where = "*",
    what = "headline",
    prompt = "Refile to ❯ ",
    actions = {
      ["default"] = actions.refile_headline,
    },
  },

  -- fzo.refile_to_file()
  refile_to_file = {
    whence = "headline",
    where = "*",
    what = "file",
    prompt = "Refile to ❯ ",
    actions = {
      ["default"] = actions.refile_headline,
    },
  },

  -- fzo.refile_to_headline()
  refile_to_headline = {
    whence = "headline",
    where = "*",
    what = "headline",
    prompt = "Refile to ❯ ",
    actions = {
      ["default"] = actions.refile_headline,
    },
  },
})
