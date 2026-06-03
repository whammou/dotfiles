# fish completions for org — unified orgmode CLI
# Install: copy to ~/.config/fish/completions/org.fish

# Subcommands: {{{

complete --command org --exclusive --condition __fish_use_subcommand --arguments agenda        --description "Open Org Agenda"
complete --command org --exclusive --condition __fish_use_subcommand --arguments backlog       --description "Open Org Backlog/Log view"
complete --command org --exclusive --condition __fish_use_subcommand --arguments browse        --description "Open fzf org-mode file browser"
complete --command org --exclusive --condition __fish_use_subcommand --arguments capture       --description "Open Org capture dialog"
complete --command org --exclusive --condition __fish_use_subcommand --arguments search        --description "Open Org agenda sparse tree search"
complete --command org --exclusive --condition __fish_use_subcommand --arguments super-agenda  --description "Open OrgSuperAgenda"
complete --command org --exclusive --condition __fish_use_subcommand --arguments tracker       --description "Open Org agenda sticky view"
complete --command org --exclusive --condition __fish_use_subcommand --arguments roam-capture  --description "Open org-roam capture"
complete --command org --exclusive --condition __fish_use_subcommand --arguments draft         --description "Create draft document template for a project"
complete --command org --exclusive --condition __fish_use_subcommand --arguments list          --description "Create list template for a project"
complete --command org --exclusive --condition __fish_use_subcommand --arguments task          --description "Create task templates (5 types) for a project"
complete --command org --exclusive --condition __fish_use_subcommand --arguments server        --description "Start inotify-based file watcher on a directory"
complete --command org --exclusive --condition __fish_use_subcommand --arguments update-flag   --description "Update an org file in a running nvim instance"
complete --command org --exclusive --condition __fish_use_subcommand --arguments cron          --description "Run headless orgmode notification check"
complete --command org --exclusive --condition __fish_use_subcommand --arguments help          --description "Show help"

# }}}

# Subcommand flags: {{{

complete --command org --exclusive --condition "__fish_seen_subcommand_from list"     --short-option n --long-option type     --description "List type (e.g. todo, review, backlog)"
complete --command org --exclusive --condition "__fish_seen_subcommand_from update-flag" --short-option a --long-option agenda  --description "Trigger full agenda redo after update"
complete --command org --exclusive --condition "__fish_seen_subcommand_from update-flag" --short-option c --long-option create  --description "Treat file as newly created (badd + checktime)"

# }}}

# Argument completions: {{{

complete --command org --condition "__fish_seen_subcommand_from draft"       --no-files --arguments '(__fish_complete_directories)'
complete --command org --condition "__fish_seen_subcommand_from server"      --arguments '(__fish_complete_directories)'
complete --command org --condition "__fish_seen_subcommand_from update-flag" --arguments '(__fish_complete_suffix .org)'

# }}}
