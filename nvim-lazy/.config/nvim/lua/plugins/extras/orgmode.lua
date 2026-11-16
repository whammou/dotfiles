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
  -- Timeblocks live in bloocky; the org agenda stays in nvim-orgmode.
  -- Credentials: lua/config/secrets.lua (see secrets.example.lua).
  (function()
    local opts = require("config.bloocky")
    local keys = {
      { "<leader>oB", "<cmd>Bloocky<CR>", desc = "Bloocky calendar" },
      { "<leader>oBs", "<cmd>BloockySidebarToggle<CR>", desc = "Bloocky sidebar" },
      { "<leader>oBd", "<cmd>Bloocky day<CR>", desc = "Bloocky day calendar" },
      { "<leader>oBw", "<cmd>Bloocky week<CR>", desc = "Bloocky week calendar" },
      { "<leader>oBm", "<cmd>Bloocky month<CR>", desc = "Bloocky day calendar" },
    }
    if opts.sync.enabled then
      keys[#keys + 1] = { "<leader>oBy", "<cmd>BloockySync<CR>", desc = "Bloocky sync now" }
      -- keys[#keys + 1] = { "<leader>oBd", "<cmd>BloockySyncStatus<CR>", desc = "Bloocky sync status" }
    end
    return {
      "atiladefreitas/bloocky",
      lazy = true,
      dependencies = { "nvim-orgmode/orgmode" },
      cmd = { "Bloocky", "BloockyToggle", "BloockySidebar", "BloockySidebarToggle" },
      keys = keys,
      opts = opts,
      config = function(_, o)
        require("bloocky").setup(o)
        require("config.bloocky_parallel").apply()
        require("config.bloocky_guard").apply()
        require("config.bloocky_collisions").apply()
        require("config.bloocky_cursor").apply()
      end,
    }
  end)(),

  {
    "BartSte/nvim-khalorg",
    lazy = true,
    ft = { "org" },
    dependencies = { "nvim-orgmode/orgmode" },
    main = "khalorg",
    opts = (function()
      local calendars = require("config.orgmode.calendars").load()
      local opts = { calendar = calendars.default, calendars = {} }
      for calendar, areas in pairs(calendars.by_calendar) do
        opts.calendars[calendar] = {
          org_file = "~/.local/share/orgmode/" .. areas[1] .. "/tasks/planned.org",
        }
      end
      return opts
    end)(),
    config = function(_, o)
      require("khalorg").setup(o)
      vim.api.nvim_create_user_command("OrgSync", function()
        local calendar = require("config.orgmode.calendars").for_file(0)
        require("khalorg").sync({ calendar = calendar })
      end, { desc = "Sync this org file to its area calendar" })
    end,
  },
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
