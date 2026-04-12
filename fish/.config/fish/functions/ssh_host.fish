function ssh_host
    # Extract client IP from SSH_CONNECTION or SSH_CLIENT
    # Output: client IP/hostname (first field), or empty if not in SSH
    if set -q SSH_CONNECTION
        printf '%s\n' (string split ' ' "$SSH_CONNECTION")[1]
        return 0
    else if set -q SSH_CLIENT
        printf '%s\n' (string split ' ' "$SSH_CLIENT")[1]
        return 0
    end
    # Not in SSH session
    printf '%s\n' ''
    return 1
end