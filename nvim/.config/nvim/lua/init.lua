-- init.lua

require('orgmode').setup({
  org_agenda_files = {'~/orgmode/*'},
  org_default_notes_file = '~/orgmode/notes.org',
  org_hide_leading_stars = false,
  org_tags_column = 0,
  org_use_tag_inheritance = true,
})

