local LinkPingType = {}

---@return string
function LinkPingType:get_name()
  return "ping"
end

---@param link string - The current value of the link, for example: "ping:google.com"
---@return boolean - When true, link was handled, when false, continue to the next source
function LinkPingType:follow(link)
  if not vim.startswith(link, "ping:") then
    return false
  end
  -- Get the part after the `ping:` part
  local url = link:sub(6)
  -- Open terminal in vertical split and ping the URL
  vim.cmd("vsplit | term ping " .. url)
  return true
end

---This method is optional.
---@param link string - The current value of the link, for example: "ping:go"
---@return string[]
function LinkPingType:autocomplete(link)
  local items = {
    "ping:google.com",
    "ping:github.com",
  }
  return vim.tbl_filter(function(item)
    return vim.startswith(item, link)
  end, items)
end

local RunShellCommand = {}

---@return string
function RunShellCommand:get_name()
  return "shell"
end

---@param link string - The current value of the link, for example: "ping:google.com"
---@return boolean - When true, link was handled, when false, continue to the next source
function RunShellCommand:follow(link)
  if not vim.startswith(link, "shell:") then
    return false
  end
  -- Get the part after the `ping:` part
  local command = link:sub(7)
  -- Open terminal in vertical split and ping the URL
  vim.cmd("split | term " .. command)
  return true
end

require("orgmode").setup({
  hyperlinks = {
    sources = {
      LinkPingType,
      RunShellCommand,
      {
        get_name = function()
          return "mailto"
        end,
        follow = function(self, link)
          local mail = link:sub(8)
          vim.cmd("split | term neomutt -- " .. mail)
          return true
        end,
        autocomplete = function(self, link)
          return { "my_custom_type:my_custom_link" }
        end,
      },
    },
  },
})
