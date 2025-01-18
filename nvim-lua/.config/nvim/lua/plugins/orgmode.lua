return {
    {
        'nvim-orgmode/orgmode',
        ft = 'org',
        opts = {
            org_agenda_files = { '~/notes/**/*', '~/notes/git/*' },
            org_default_notes_file = '~/notes/quick.org',
            org_archive_location = './archive/log.org::ARCHIVED',
            org_split_mode = { 'auto' },
            org_hide_leading_stars = false,
            org_adapt_indentaion = false,
            org_startup_indented = true,
            org_use_tag_inheritance = true,
            org_tags_column = 0,
            org_todo_keywords = { 'TODO(t)','PENDING(p)' , 'DOING(d)', '|', 'DONE(f)', 'ABORTED(a)' },
            mappings = {
              org = {
                  org_cycle = false,
              },
            },
            ui = {
              folds = {
                  colored = false,
              }
            },
        },
    },


    {
        'lukas-reineke/headlines.nvim',
        ft = 'org',
        opts = {},
    },


    {
        'nvim-orgmode/org-bullets.nvim',
        ft = 'org',
        opts = {},
    },
}
