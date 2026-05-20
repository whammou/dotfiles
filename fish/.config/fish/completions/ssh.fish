# Custom SSH completions — includes all built-in flags + remote path completion
#
# Remote path completion enables:
#   ssh host <command> /pa<TAB> → /path/... (paths from remote host)
#   ssh host <command> ~/use<TAB> → /home/user/... (via ~ expansion on remote)
#   ssh host <command> ./rel<TAB> → ./relative/path/...
#   ssh host <command> -p myproj<TAB> → completes remote myproj*
#   ssh host <command> -p <TAB> → lists remote files
#
# Requires key-based SSH login (password prompts will block completion).
#
# Built-in SSH completions are sourced first (flag completions, host
# completions, remote command name via __fish_complete_subcommand).
# Remote path completion fires for any non-flag argument after the command.
# You may see both local AND remote results — type more to narrow down.

# 1. Load all built-in SSH completions (flags, hosts, subcommand)
source /usr/share/fish/completions/ssh.fish

# 2. Add remote path completion for arguments after the host+command
function __fish_ssh_remote_should_complete -d 'Check if remote path completion should activate'
    # Need at least: ssh + host + command
    test (__fish_number_of_cmd_args_wo_opts) -ge 3; or return 1

    set -l token (commandline -ct)
    # Skip flags — let local command completions handle those
    string match -q -- '-*' $token; and return 1
    # Complete remote paths for any non-flag token (empty, path, or plain word)
    return 0
end

function __fish_ssh_remote_get_host -d 'Extract the SSH target host from command line tokens'
    set -l tokens (commandline -poc)
    for t in $tokens
        if not string match -qr '^--?|^ssh$' -- $t
            echo $t
            return 0
        end
    end
    return 1
end

function __fish_ssh_remote_complete_path -d 'Complete paths on the remote host via SSH'
    set -l host (__fish_ssh_remote_get_host); or return
    set -l token (commandline -ct)

    # ls -1dp: one-per-line, list dirs-as-entries (no recuse), append / to dirs
    # Two globs: normal files and dotfiles
    # Using 2>/dev/null to suppress errors from both local and remote side
    ssh -o Batchmode=yes -o ConnectTimeout=2 -- "$host" \
        "ls -1dp -- $token* 2>/dev/null; ls -1dp -- $token.* 2>/dev/null" 2>/dev/null \
        | string trim
end

complete -c ssh -n __fish_ssh_remote_should_complete -k -x \
    -a '(__fish_ssh_remote_complete_path)'
