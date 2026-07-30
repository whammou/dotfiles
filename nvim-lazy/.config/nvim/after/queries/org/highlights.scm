; inherits: org

(section (headline (tag_list) @_tags (#match? @_tags ":ARCHIVE:") (#set! priority "150"))) @comment
(("\\") (#set! priority "150")) @comment

; Enable spell checking inside #+begin_quote blocks
(block name: (expr) @_name (contents) @spell (#eq? @_name "quote"))

