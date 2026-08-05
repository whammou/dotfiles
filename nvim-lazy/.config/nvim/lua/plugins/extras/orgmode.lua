return {
  {
    "nvim-orgmode/orgmode",
    lazy = true,
    ft = { "org" },
    cmd = { "Org" },
    config = function()
      require("config.orgmode.init")
      vim.lsp.enable("org")
    end,
    keys = {
      { "<leader>oR", "<cmd>Lazy reload orgmode<CR>", desc = "Org reload" },
      { "<leader>obe", "<cmd>OrgExecute!<CR>", desc = "Org execute current block" },
    },
  },
  {
    "seflue/org-link.nvim",
    lazy = true,
    ft = { "org" },
    dependencies = { "nvim-orgmode/orgmode" },
    opts = {},
  },
  {
    "whammou/orgmode-babel.nvim",
    lazy = true,
    ft = { "org" },
    branch = "feat/cursor-block-execute",
    dependencies = { "nvim-orgmode/orgmode" },
    cmd = { "OrgExecute", "OrgTangle" },
    opts = {
      langs = { "python", "lua", ... },
      load_paths = {},
      extra_evals = {
        "(setq org-id-track-globally nil)",
        '(setq org-babel-python-command "/home/whammou/.local/share/sniprun-venv/bin/python")',
        '(org-babel-make-language-alias "py" "python")',
      },
    },
  },
  {
    "danilshvalov/org-modern.nvim",
    lazy = true,
    ft = { "org" },
    dependencies = { "nvim-orgmode/orgmode" },
  },
  {
    "0xzhzh/fzf-org.nvim",
    lazy = true,
    ft = { "org" },
    dependencies = { "nvim-orgmode/orgmode" },
    keys = {
      {
        "<leader>ozt",
        function()
          require("fzf-org").filetags()
        end,
        desc = "org-titles",
      },
      {
        "<leader>ozg",
        function()
          require("fzf-org").orgmode()
        end,
        desc = "org-browse",
      },
      {
        "<leader>ozf",
        function()
          require("fzf-org").files()
        end,
        desc = "org-files",
      },
      {
        "<leader>ozr",
        function()
          require("fzf-org").refile_to_file()
        end,
        desc = "org-refile",
      },
    },
    opts = {},
  },
  {
    "nvim-orgmode/org-bullets.nvim",
    lazy = true,
    ft = { "org" },
    dependencies = { "nvim-orgmode/orgmode" },
    opts = {
      concealcursor = true,
      symbols = {
        list = "",
      },
    },
  },
  {
    "chipsenkbeil/org-roam.nvim",
    lazy = true,
    ft = { "org" },
    dependencies = { "nvim-orgmode/orgmode" },
    keys = {
      { "<leader>nu", "<Cmd>RoamUpdate<CR>", desc = "Update Roam database" },
      { "<leader>nU", "<Cmd>RoamUpdate!<CR>", desc = "Force update Roam database" },
    },
  },

  --{
  --  "BartSte/nvim-khalorg",
  --  lazy = true,
  --  opts = {
  --    calendar = "private",
  --  },
  --},
  --{
  --  "hamidi-dev/org-super-agenda.nvim",
  --  lazy = true,
  --  opts = {
  --    org_directories = { "/home/whammou/Journal/" },
  --    show_filename = false,
  --    keep_order = true,
  --    window = {
  --      width = 0.8,
  --      height = 0.8,
  --      border = "none",
  --    },
  --    todo_states = {
  --      { name = "TODO", keymap = "ot", color = "#c678dd" },
  --      { name = "DOIN", keymap = "od", color = "#56b6c2" },
  --      { name = "PEND", keymap = "op", color = "#abb2bf" },
  --      { name = "OUTL", keymap = "oo", color = "#abb2bf" },
  --      { name = "IDEA", keymap = "oi", color = "#abb2bf" },
  --      { name = "WAIT", keymap = "ow", color = "#d19a66" },
  --      { name = "EXPL", keymap = "os", color = "#d19a66" },
  --      { name = "FDBK", keymap = "ob", color = "#d19a66" },
  --      { name = "NEXT", keymap = "on", color = "#73b8f1" },
  --      { name = "RVIW", keymap = "ov", color = "#e5c07b" },
  --      { name = "PRTL", keymap = "or", color = "#e5c07b" },
  --      { name = "ABRT", keymap = "oa", color = "#e86671", strike_through = true },
  --      { name = "DONE", keymap = "of", color = "#98c379" },
  --    },
  --    keymaps = {
  --      toggle_other = "oO",
  --      cycle_view = "oV",
  --      filter = "oF",
  --      filter_fuzzy = "oZ",
  --      filter_query = "oQ",
  --      filter_reset = "oA",
  --    },
  --    upcoming_days = 7,
  --    group_format = "* /%s/",
  --    groups = {
  --      {
  --        name = " Oneoff",
  --        matcher = function(i)
  --          return i:has_tag("oneoff") and (i.deadline and i.deadline:is_today())
  --            or (i.scheduled and i.scheduled:is_today())
  --        end,
  --      },
  --      {
  --        name = " Recurring",
  --        matcher = function(i)
  --          return i:has_tag("recurring") and (i.deadline and i.deadline:is_today())
  --            or (i.scheduled and i.scheduled:is_today())
  --        end,
  --      },
  --      {
  --        name = " Incidental",
  --        matcher = function(i)
  --          return i:has_tag("incidental") and (i.deadline and i.deadline:is_today())
  --            or (i.scheduled and i.scheduled:is_today())
  --        end,
  --      },
  --      {
  --        name = " Coordinated",
  --        matcher = function(i)
  --          return i:has_tag("coordinated") and (i.deadline and i.deadline:is_today())
  --            or (i.scheduled and i.scheduled:is_today())
  --        end,
  --      },
  --      {
  --        name = " Planned",
  --        matcher = function(i)
  --          return i:has_tag("planned") and (i.deadline and i.deadline:is_today())
  --            or (i.scheduled and i.scheduled:is_today())
  --        end,
  --      },
  --      {
  --        name = "󱔗 Documents",
  --        matcher = function(i)
  --          return i:has_tag("doc") and (i.deadline and i.deadline:is_today())
  --            or (i.scheduled and i.scheduled:is_today())
  --        end,
  --      },
  --    },
  --  },
  --},
  --{
}
