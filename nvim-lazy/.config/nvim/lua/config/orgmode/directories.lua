local base_dir = vim.fn.expand("~/Journal/")
local zettel_dir = base_dir .. "/topics/vault/"
local relative_dir = vim.fn.getcwd():gsub(base_dir, "")

local dir = {
  base_dir = base_dir,
  zettel_dir = zettel_dir,
  relative_dir = relative_dir,
}

return dir
