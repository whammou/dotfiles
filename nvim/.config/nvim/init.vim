" __     _____ __  __ ____   ____ 
" \ \   / /_ _|  \/  |  _ \ / ___|
"  \ \ / / | || |\/| | |_) | |    
"   \ V /  | || |  | |  _ <| |___ 
"    \_/  |___|_|  |_|_| \_\\____|
"_________________________________                                 


lua vim.loader.enable()
let g:python3_host_prog = '/usr/bin/python3'
let g:loaded_perl_provider = 0


" SETTINGS --------------------------------------
" Key binds

let mapleader=" "
let maplocalleader=" "

nnoremap <silent><A-j> :set paste<CR>m`o<Esc>``:set nopaste<CR>
nnoremap <silent><A-k> :set paste<CR>m`O<Esc>``:set nopaste<CR>
nnoremap <SPACE> <Nop>
nnoremap [s [sz=
nnoremap ]s ]sz=
nnoremap <M-h> Hzb
nnoremap <M-l> Lzt
nnoremap zo zMzvzz
nnoremap <CR> :noh<CR>
nnoremap <leader>u :let @+ = expand('<cfile>')<CR>
nnoremap <silent> <leader>b :Buffers<CR>
nnoremap <silent> <leader>M :MarksToggleSigns<CR>
nnoremap <silent> <leader>m :Marks<CR>
nnoremap <silent> <leader>l :Lines<CR>
nnoremap <silent> <leader>L :BLines<CR>
nnoremap <silent> <leader>f :Files<CR>
nnoremap <silent> <leader>R :RG<CR>

inoremap <C-b> <space><esc>ce
map <Leader>r :set wrap!<CR>
map <Leader>p :set spell!<CR>
map <Leader>G :GripStart<CR>

" Git related keybinds
nnoremap <silent> <leader>gu :GetCurrentBranchLink<CR>
nnoremap <silent> <leader>gl :GFiles<CR>
nnoremap <silent> <leader>gs :Git<CR>
nnoremap <silent> <leader>gf :G fetch<CR>
nnoremap <silent> <leader>gm :G merge<CR>
nnoremap <silent> <leader>gp :G pull<CR>
nnoremap <silent> <leader>gc :G commit %<CR>
nnoremap <silent> <leader>gdx :Gvdiffsplit!<CR>
nnoremap <silent> <leader>gdy :Gdiffsplit!<CR>

" Default colorscheme
":set termguicolors
:filetype on
:filetype plugin on
:filetype indent on

:syntax on
":set foldmethod=syntax
set shell=/bin/bash
:set number relativenumber
:set cursorline

:set shiftwidth=4
:set tabstop=4
:set expandtab
:set nobackup
:set scrolloff=0
:set nowrap
:set incsearch
:set ignorecase
:set smartcase
:set showcmd
:set showmatch
:set hlsearch
:set noshowmode
:set history=1000
:set cmdheight=0
:set showtabline=1
:set nomore


" PLUGINS-------------------------------------------

call plug#begin('~/.config/nvim/vim-plug')
Plug 'tpope/vim-fugitive'
Plug 'navarasu/onedark.nvim'
Plug 'chrisbra/Colorizer'
Plug 'christoomey/vim-tmux-navigator'
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'

" nvim completion
Plug 'ervandew/supertab'
Plug 'Valloric/YouCompleteMe'

" nvim snippet
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'

" nvim-tts
" Plug 'wolandark/vim-piper'

Plug 'kuangliu/vim-easymotion'
Plug 'jiangmiao/auto-pairs'
Plug 'chentoast/marks.nvim'
Plug 'knsh14/vim-github-link', {'for': ['markdown', 'org']}
Plug 'echasnovski/mini.nvim'
Plug 'nvim-treesitter/nvim-treesitter'
Plug 'duane9/nvim-rg'
Plug '3rd/image.nvim', {'for': ['markdown', 'org']}

" vim-markdown
Plug 'willchao612/vim-diagon', {'for': 'markdown'}
Plug 'PratikBhusal/vim-grip', {'for': 'markdown'}
Plug 'MeanderingProgrammer/render-markdown.nvim'

" Vim-tex
Plug 'lervag/vimtex', {'for': 'tex'}
Plug 'matze/vim-tex-fold', {'for': 'tex'}

" " telescope
" Plug 'nvim-lua/plenary.nvim'
" Plug 'nvim-telescope/telescope.nvim'
" 
" " telescope-plugin
" Plug 'nvim-lua/popup.nvim'
" Plug 'nvim-telescope/telescope-media-files.nvim'

" Vim-papis
Plug 'junegunn/fzf'
Plug 'junegunn/fzf.vim'
"Plug 'papis/papis-vim'

" Vim-citation
"Plug 'rafaqz/citation.vim'
"Plug 'Shougo/unite.vim'

" vim-orgmode
Plug 'nvim-orgmode/orgmode'
Plug 'lukas-reineke/headlines.nvim', {'for': 'org'}
Plug 'nvim-orgmode/org-bullets.nvim', {'for': 'org'}
call plug#end()
lua require('init')


" vim-onedark CONFIGS ------------------------------

let g:onedark_config = {'style': 'darkest'}
:colorscheme onedark

" vim-marks SETTINGS -------------------------------

hi MarkSignHL gui=bold guifg=#00FF00

" vim-airline SETTINGS -----------------------------
let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#formatter = 'unique_tail'
let g:airline#extensions#tabline#buffer_nr_show = 0
let g:airline_theme = 'onedark'
let g:airline_powerline_fonts = 1
let g:airline_skip_empty_sections = 1
let g:airline_section_y = ''
let g:airline_section_x = ''
let g:airline_section_warning = ''

" YouCompleteMe SETTINGS ---------------------------
let g:ycm_filetype_blacklist = {}

let g:ycm_key_list_select_completion = ['<C-n>', '<Down>']
let g:ycm_key_list_previous_completion = ['<C-p>', '<Up>']

" UltilSnip SETTINGS -------------------------------
let g:UltiSnipsSnippetDirectories=[$HOME.'/.vim/bundle/vim-snippets/UltiSnips', 'mycoolsnippets']
let g:UltiSnipsExpandTrigger = "<tab>"
let g:UltiSnipsJumpForwardTrigger = "<tab>"
let g:UltiSnipsJumpBackwardTrigger = "<s-tab>"
let g:UltiSnipsEditSplit="horizontal"

" Supertab SETTINGS -------------------------------
let g:SuperTabDefaultCompletionType = '<C-n>'

" EASYMOTION SETTINGS ------------------------------
let g:EasyMotion_verbose = 0
let g:EasyMotion_prompt = ""

" BUFFERLINE SETTINGS ------------------------------
let g:bufferline_echo = 1
let g:bufferline_inactive_highlight = 'StatusLineNC'
let g:bufferline_active_highlight = 'StatusLine'

" Citation-vim SETTINGS ----------------------------
let g:citation_vim_mode="zotero"
let g:citation_vim_zotero_path="~/Zotero"
let g:citation_vim_zotero_version=5
let g:citation_vim_cache_path='~/.cache/nvim_sessions'
let g:citation_vim_outer_prefix="["
let g:citation_vim_inner_prefix="@"
let g:citation_vim_suffix="]"

" vim-pandoc SETTINGS ------------------------------
let g:pandoc#filetypes#handled = ["pandoc", "markdown"]
let g:pandoc#filetypes#pandoc_markdown = 0

" MARKDOWN SETTINGS --------------------------------
let g:markdown_folding = 1
let g:markdown_recommended_style = 0
let g:mardown_fenced_languages  = ['html', 'python', 'lua', 'vim', 'typescript', 'javascript']
let g:vim_markdown_math = 1

" LATEX SETTINGS -----------------------------------
let g:vimtex_view_method = 'zathura'
let g:vimtex_compiler_method = 'latexmk'

" VIM-FZF SETTINGS ---------------------------------
let g:fzf_vim ={}

" VIM-FZF SETTINGS ---------------------------------
:hi @org.headline.level1 gui=bold guifg=#ff005c
:hi @org.headline.level2 gui=bold guifg=#ae00ff
:hi @org.headline.level3 gui=bold guifg=#ff6700
:hi @org.headline.level4 gui=bold guifg=#ff005c
:hi @org.headline.level5 gui=bold guifg=#ae00ff
:hi @org.agenda.scheduled_past guifg=#ff005c
:hi @org.keyword.todo gui=reverse guifg=#ffff33

lua require'nvim-treesitter.configs'.setup{ ensure_installed = { "latex", "html", "org"},highlight={enable=true} }
