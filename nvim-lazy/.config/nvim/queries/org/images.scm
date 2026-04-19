; Custom orgmode queries for snacks.image preview
; Includes ALL original nvim-orgmode patterns + new mermaid/dot

;; ===== Image file links =====
(link url: (expr) @image.src
  (#gsub! @image.src "^file:" "")
  (#match? @image.src "(png|jpg|jpeg|gif|bmp|webp|tiff|heic|avif|mp4|mov|avi|mkv|webm|pdf|svg)$"))

;; ===== LaTeX Math (from nvim-orgmode) =====
(block
  name: (expr) @name
  parameter: (expr) @lang
  contents: (contents) @image.content
  (#match? @name "(src|SRC)")
  (#match? @lang "(math|latex)")
  (#set! injection.language "latex")
  (#set! image.ext "math.tex"))

(block
  name: (expr) @name
  contents: (contents) @image.content
  (#match? @name "(equation|EQUATION)")
  (#set! injection.language "latex")
  (#set! image.ext "math.tex"))

(latex_env
  (#set! injection.language "latex")
  (#set! image.ext "math.tex")) @image.content @image

(inline_math_block
  (#set! injection.language "latex")
  (#set! image.ext "math.tex")) @image.content @image

(display_math_block
  (#set! injection.language "latex")
  (#set! image.ext "math.tex")) @image.content @image

;; ===== NEW: Mermaid Diagrams =====
(block
  name: (expr) @name
  parameter: (expr) @lang
  contents: (contents) @image.content
  (#match? @name "(src|SRC)")
  (#match? @lang "(mermaid)")
  (#set! injection.language "mermaid")
  (#set! image.ext "mmd")) @image

;; ===== NEW: Graphviz / DOT =====
(block
  name: (expr) @name
  parameter: (expr) @lang
  contents: (contents) @image.content
  (#match? @name "(src|SRC)")
  (#match? @lang "(dot|graphviz)")
  (#set! injection.language "dot")
  (#set! image.ext "dot")) @image

;; ===== NEW: PlantUML =====
(block
  name: (expr) @name
  parameter: (expr) @lang
  contents: (contents) @image.content
  (#match? @name "(src|SRC)")
  (#match? @lang "(plantuml|uml)")
  (#set! injection.language "plantuml")
  (#set! image.ext "puml")) @image