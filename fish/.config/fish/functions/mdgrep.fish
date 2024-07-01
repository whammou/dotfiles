function mdgrep --wraps='grep -rin --color=always --include="*.md*"' --description 'alias mdgrep=grep -rin --color=always --include="*.md*"'
  grep -rin --color=always --include="*.md*" $argv
        
end
