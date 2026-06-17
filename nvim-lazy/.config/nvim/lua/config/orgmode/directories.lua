local base_dir = vim.fn.expand("~/.local/share/orgmode/")
local zettel_dir = "/vault/"
local relative_dir = vim.fn.getcwd():gsub(base_dir, "")

local dir = {
  base_dir = base_dir,
  zettel_dir = zettel_dir,
  relative_dir = relative_dir,
}

return dir
