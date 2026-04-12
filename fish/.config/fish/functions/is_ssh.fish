function is_ssh
    # Check if any SSH environment variable is set
    # Returns 0 (success) if in SSH session, 1 if local
    if set -q SSH_TTY
        return 0
    else if set -q SSH_CONNECTION
        return 0
    else if set -q SSH_CLIENT
        return 0
    end
    return 1
end