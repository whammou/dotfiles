; extends
; nvim-orgmode provides image links + LaTeX math queries
; Only custom diagram types added here

;; ===== Mermaid Diagrams =====
(block
  name: (expr) @name
  parameter: (expr) @lang
  contents: (contents) @image.content
  (#match? @name "(src|SRC)")
  (#match? @lang "(mermaid)")
  (#set! injection.language "mermaid")
  (#set! image.ext "mmd")) @image

;; ===== Graphviz / DOT =====
(block
  name: (expr) @name
  parameter: (expr) @lang
  contents: (contents) @image.content
  (#match? @name "(src|SRC)")
  (#match? @lang "(dot|graphviz)")
  (#set! injection.language "dot")
  (#set! image.ext "dot")) @image

;; ===== PlantUML =====
(block
  name: (expr) @name
  parameter: (expr) @lang
  contents: (contents) @image.content
  (#match? @name "(src|SRC)")
  (#match? @lang "(plantuml|uml)")
  (#set! injection.language "plantuml")
  (#set! image.ext "puml")) @image