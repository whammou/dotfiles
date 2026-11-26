-- capture_patch.lua -- capture-time fixes kept separate from FILETAGS inference.
--
-- 1. OrgFile:_get_directive() only reads direct directive children of `body`.
--    Without a blank line after #+TITLE, tree-sitter nests directives in a
--    `paragraph`, so org-roam cannot resolve %[slug] from the injected title.
--    Fall back to directives inside top-level body paragraphs only when the
--    direct lookup finds nothing.
-- 2. org-roam injects a blank line after the title to make it parse correctly.
--    That blank must exist while the target is resolved, but is removed from
--    the final capture lines. Preserve Template:compile()'s target restoration
--    while doing that.

local M = {}

local function patch_get_directive()
  local ok_orgfile, OrgFile = pcall(require, "orgmode.files.file")
  local ok_ts, ts_utils = pcall(require, "orgmode.utils.treesitter")
  if not ok_orgfile or not ok_ts then
    return false
  end
  if OrgFile._capture_nested_directive_patched then
    return true
  end

  local orig_get_directive = OrgFile._get_directive
  OrgFile._get_directive = function(self, directive_name, all_matches)
    local direct = orig_get_directive(self, directive_name, all_matches)
    if direct then
      return direct
    end

    self:parse(true)
    local body = self.root and self.root:field("body")[1]
    if not body then
      return nil
    end

    local values = {}
    for _, paragraph in ipairs(ts_utils.get_named_children(body) or {}) do
      if paragraph:type() == "paragraph" then
        for _, directive in ipairs(ts_utils.get_named_children(paragraph) or {}) do
          if directive:type() == "directive" then
            local name = directive:field("name")[1]
            local value = directive:field("value")[1]
            if name and value then
              local name_text = self:get_node_text(name)
              if name_text:lower() == directive_name:lower() then
                table.insert(values, self:get_node_text(value))
              end
            end
          end
        end
      end
    end

    if all_matches then
      return #values > 0 and values or nil
    end
    return values[1]
  end

  OrgFile._capture_nested_directive_patched = true
  return true
end

local function patch_compile()
  local ok, Template = pcall(require, "orgmode.capture.template")
  if not ok then
    return false
  end
  if Template._capture_blank_line_patched then
    return true
  end

  local orig_compile = Template.compile
  Template.compile = function(self)
    if self._saved_target then
      self.target = self._saved_target
    end
    local pending = self.target
    return orig_compile(self):next(function(lines)
      self._saved_target = pending
      if lines then
        for i = 1, #lines - 1 do
          if lines[i] == ":END:" or (lines[i] and lines[i]:match("^#%+TITLE: ")) then
            if lines[i + 1] == "" then
              table.remove(lines, i + 1)
              break
            end
          end
        end
      end
      return lines
    end)
  end

  Template._capture_blank_line_patched = true
  return true
end

do
  local patched = false
  local function try_patch()
    if patched then
      return
    end
    local ok_directive = patch_get_directive()
    local ok_compile = patch_compile()
    patched = ok_directive and ok_compile
  end
  try_patch()
  if not patched then
    vim.schedule(try_patch)
  end
end

return M
