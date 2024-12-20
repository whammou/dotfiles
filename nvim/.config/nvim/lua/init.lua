-- init.lua
require('orgmode').setup({
  org_agenda_files = {'~/notes/**/*', '~/notes/git/*'},
  org_default_notes_file = '~/notes/quick.org',
  org_archive_location = './archive/%s_archive::',
  org_split_mode = {'auto'},
  org_hide_leading_stars = false,
  org_adapt_indentaion = false,
  org_startup_indented = true,
  org_use_tag_inheritance = true,
  org_tags_column = 0,
  org_todo_keywords = {'TODO(t)','PENDING(p)' , 'DOING(d)', '|', 'DONE(f)', 'ABORTED(a)'},

  mappings = {
      org = {
          org_cycle = false,
      },
  },

  ui = {
      folds = {
          colored = false
      }
  },
})

require('markdown').setup({
    mappings = {
        link_follow = "gm",
    },
})
require'marks'.setup()
-- require('mkdnflow').setup()
