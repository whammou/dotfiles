"%% SiSU Vim color file
" Slate Maintainer: Ralph Amissah <ralph@amissah.com>
" (originally looked at desert Hans Fugal <hans@fugal.net> http://hans.fugal.net/vim/colors/desert.vim (2003/05/06)
:set background=dark
:highlight clear
if version > 580
 hi clear
 if exists("syntax_on")
 syntax reset
 endif
endif
let colors_name = "slate"
:hi link _Comment Comment
" colors
:hi _memberFunc guifg=magenta
:hi _Operator guifg=cyan
:hi Operator_ guifg=magenta
":hi Title cterm=bold ctermfg=cyan
:hi Normal guifg=white guibg=black
:hi Pmenu guifg=#00FF00 guibg=#0A0A0A
:hi PmenuSel guifg=cyan guibg=#002628
:hi CursorLine guibg=#002628 gui=NONE
:hi CursorLineNR guibg=#002628 guifg=white gui=NONE
:hi VertSplit gui=reverse
:hi Folded guifg=#AE00FF guibg=#0D0014
:hi FoldColumn guifg=4 guibg=7
:hi IncSearch gui=none guifg=black guibg=#FFDB00
:hi ModeMsg gui=none guifg=cyan guibg=#002628
:hi MoreMsg guifg=#00FF00
:hi NonText gui=bold guifg=#AE00FF
:hi Question guifg=#00FF00
:hi Search gui=none guifg=black guibg=#AE00FF
:hi SpecialKey guifg=#00FF00
:hi StatusLine gui=NONE guibg=#140007 guifg=#FF005C
:hi StatusLineNC gui=NONE guibg=#0A0A0A guifg=#464646
:hi Title gui=bold guifg=cyan
:hi Statement guifg=magenta
:hi Visual gui=reverse
:hi WarningMsg guifg=#FFDB00
:hi String guifg=cyan
:hi Comment guifg=#464646
:hi Constant gui=bold guifg=cyan
:hi Special guifg=#FFDB00
:hi Identifier guifg=#FF005C
:hi Include guifg=#00FF00
:hi Number guifg=white
:hi PreProc guifg=#00FF00
:hi Operator guifg=#FF005C
:hi Define guifg=#FFDB00
:hi Type guifg=#FF005C
:hi Function guifg=#FFDB00
:hi Structure guifg=#FF005C
:hi LineNr gui=bold guifg=#464646
:hi Ignore gui=bold guifg=7
:hi Todo gui=bold guifg=back guibg=#FFDB00
:hi Directory guifg=cyan
:hi ErrorMsg gui=NONE guifg=#FF005C
:hi WildMenu guifg=0 guibg=3
:hi DiffAdd guibg=4
:hi DiffChange guibg=5
:hi DiffDelete gui=bold guifg=4 guibg=6
:hi DiffText gui=bold guibg=1
:hi Underlgrayed gui=underline guifg=5
:hi Error gui=bold guifg=#FF005C guibg=black
:hi MatchParen gui=NONE guifg=black guibg=#FF005C
:hi Underlined gui=underline guifg=#FF005C
":hi SpellErrors fg=White bg=#FF005C gui=bold guifg=7 guibg=1"
:hi Spellbad guifg=#FF00FF
:hi NvimInternalError guibg=#FF005C guifg=#464646
:hi ErrorMsg guifg=#FF005C guibg=black

" SNIPPETS -----------------------------------------
:hi snipTabStop guifg=#00FF00
:hi snipEscape guifg=#AE00FF

" MARKDOWN------------------------------------------
:hi markdownUrl guifg=cyan
:hi markdownAutomaticLink guifg=cyan
:hi markdownListMarker guifg=magenta
:hi markdownOrderedListMarker guifg=magenta
:hi markdownBlockquote gui=bold guifg=#FF005C
:hi markdownUrlDelimiter guifg=#28003B
:hi markdownUrlTitleDelimiter guifg=#00FF00
:hi markdownCodeDelimiter guifg=#00FF00
:hi markdownHeadingDelimiter guifg=#00FF00
:hi markdownH1 gui=bold guifg=cyan
:hi markdownH1Delimiter guifg=cyan
:hi markdownH2 gui=bold guifg=#FF005C
:hi markdownH2Delimiter guifg=#FF005C
:hi markdownH3 gui=bold guifg=#FF00FF
:hi markdownH3Delimiter guifg=#FF00FF
:hi markdownH4 gui=bold guifg=#00FF00
:hi markdownH4Delimiter guifg=#00FF00
:hi markdownH5 gui=bold guifg=#AE00FF
:hi markdownH5Delimiter guifg=#AE00FF
:hi markdownH6Delimiter guifg=#00FF00
:hi markdownBold gui=bold
:hi markdownBoldDelimiter gui=bold
:hi markdownItalic gui=italic
:hi markdownItalicDelimiter gui=italic
:hi markdownBoldItalic gui=bold,italic
:hi markdownBoldItalicDelimiter gui=bold,italic
:hi markdownIdDeclaration guifg=magenta
:hi markdownLink gui=bold
:hi markdownLinkDelimiter gui=bold
:hi markdownLinkTextDelimiter gui=bold
:hi markdownFootnoteDefinition guifg=#AE00FF
:hi markdownFootnote guifg=#AE00FF
:hi htmlTagName gui=NONE guifg=#464646
:hi htmlTag guifg=#28003B
:hi htmlEndTag guifg=#3B0015
:hi yamlBlockMappingKey guifg=#FF00FF
:hi yamlKeyValueDelimiter guifg=#00FFFF

" LaTeX --------------------------------------------
:hi TexRefZone guifg=#00FFFF
:hi texMathZoneES guifg=cyan
:hi texMathMatcher guifg=cyan
:hi texMathZoneX guifg=cyan
:hi texInputFile gui=bold guifg=cyan
:hi texSection gui=bold guifg=#FF005C
:hi texSpecialChar guifg=#00FF00
:hi texString guifg=#00FF00
:hi texDelimiter guifg=#FF00FF
:hi texBoldStyle gui=bold
:hi texItalStyle gui=italic
:hi texCmdBody guifg=cyan

" ORGMODE ------------------------------------------
:hi org_todo_keyword_TODO guifg=black guibg=#FFDB00
:hi org_list_checkbox guifg=#AE00FF
:hi org_heading3 gui=bold guifg=#FF005C
:hi org_shade_stars guifg=#464646
:hi hyperlink gui=underline guifg=normal

" EasyMotion ---------------------------------------
:hi EasyMotionTargetDefault guifg=#FF005C
:hi EasyMotionTarget2FirstDefault guifg=#005C5C
:hi EasyMotionTarget2SecondDefault guifg=#00FFFF

" Python -------------------------------------------
:hi pythonInclude guifg=#00FF00 gui=bold
:hi pythonFunction guifg=#FF005C  gui=bold
:hi pythonOperator guifg=#FF005C gui=bold
:hi pythonString guifg=#AE00FF
:hi pythonNumber guifg=#00FF00
:hi pythonQuotes guifg=#AE00FF
function MyCustoHighLights()
    hi semshiSelected guifg=black
    hi semshiGlobal gui=bold guifg=normal
    hi semshiBuiltin guifg=#FF00FF
    hi semshiImported guifg=cyan
    hi semshiAttribute guifg=#AE00FF
    hi semshiParameter guifg=cyan
endfunction
autocmd FileType python call MyCustoHighLights()
