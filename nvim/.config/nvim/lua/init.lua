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

require'image'.setup({
    backend = 'kitty',
    processor = 'magick_cli',
    integrations = {
        markdown = {
            enabled = true,
            clear_in_insert_mode = true,
            only_render_image_at_cursor = true,
            filtypes = { "markdown", "html" },
        },
        html = {
            enabled = true,
            clear_in_insert_mode = true,
            only_render_image_at_cursor = true,
            filetypes = { "markdown" },
        },
    },
    max_width_window_percentage = 80,
    max_height_window_percentage = 80,
})

require'marks'.setup()
