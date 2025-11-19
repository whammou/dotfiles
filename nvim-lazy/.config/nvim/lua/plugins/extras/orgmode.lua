return {
  {
    "nvim-orgmode/orgmode",
    lazy = true,
    ft = { "org" },
    dependencies = {
      {
        "danilshvalov/org-modern.nvim",
        lazy = true,
        event = "VeryLazy",
        ft = { "org" },
      },
      {
        "0xzhzh/fzf-org.nvim",
        lazy = true,
        ft = { "org" },
        keys = {
          -- example keybindings
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
        opts = {},
      },
      {
        "lukas-reineke/headlines.nvim",
        lazy = true,
      },
      {
        "chipsenkbeil/org-roam.nvim",
        lazy = true,
        ft = { "org" },
        keys = {
          { "<leader>nu", "<Cmd>RoamUpdate<CR>", desc = "Update Roam database" },
          { "<leader>nU", "<Cmd>RoamUpdate!<CR>", desc = "Force update Roam database" },
        },
      },
    },
    config = function()
      require("config.orgmode.init")
    end,
    keys = {
      { "<leader>oR", "<cmd>Lazy reload orgmode<CR>", desc = "Org reload" },
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
  --      { name = "TODO", keymap = "ot", color = "#c75ae8" },
  --      { name = "DOIN", keymap = "od", color = "#34bfd0" },
  --      { name = "PEND", keymap = "op", color = "#93a4c3" },
  --      { name = "OUTL", keymap = "oo", color = "#93a4c3" },
  --      { name = "IDEA", keymap = "oi", color = "#93a4c3" },
  --      { name = "WAIT", keymap = "ow", color = "#dd9046" },
  --      { name = "EXPL", keymap = "os", color = "#dd9046" },
  --      { name = "FDBK", keymap = "ob", color = "#dd9046" },
  --      { name = "NEXT", keymap = "on", color = "#54b0fd" },
  --      { name = "RVIW", keymap = "ov", color = "#efbd5d" },
  --      { name = "PRTL", keymap = "or", color = "#efbd5d" },
  --      { name = "ABRT", keymap = "oa", color = "#f65866", strike_through = true },
  --      { name = "DONE", keymap = "of", color = "#8bcd5b" },
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
