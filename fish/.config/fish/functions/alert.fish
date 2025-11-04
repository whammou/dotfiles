function alert
    #set -l token (cat ~/.ntfy_token)
    #set -l status_icon (test $exit_status -eq 0 && echo magic_wand || echo warning)
    set -l exit_status $status
    set -l last_command (echo (status current-commandline) | sed -e 's/^[[:space:]]*[0-9]\{1,\}[[:space:]]*//' -e 's/[;&|][[:space:]]*alert$//')

    #-H "Authorization: Bearer $token" \
    #-H "Tags: $status_icon" \
    curl -s -X POST "https://ntfy.sh/whammou_alert" \
        -H "Title: Terminal" \
        -H "X-Priority: 3" \
        -d "$hostname - Command: $last_command(Exit: $exit_status)"

    #echo "Tags: $status_icon"
    #echo "$last_command (Exit: $exit_status)"
end
