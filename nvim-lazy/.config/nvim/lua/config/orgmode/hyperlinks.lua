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
  local url = link:sub(6)
  Snacks.terminal.open({ "ping", url }, { win = { position = "right", width = 0.5 } })
  return true
end

---This method is optional.
---@param context OrgCompletionContext
---@return string[]
function LinkPingType:autocomplete(context)
  local base = type(context) == "string" and context or context.base or ""
  local items = {
    "ping:google.com",
    "ping:github.com",
  }
  return vim.tbl_filter(function(item)
    return vim.startswith(item, base)
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
  local command = link:sub(7)
  Snacks.terminal.open(command, { win = { position = "bottom", height = 0.5 } })
  return true
end

local SendMail = {}

---@return string
function SendMail:get_name()
  return "mailto"
end

---@param link string - The current value of the link, for example: "mailto: user@domain.com <user@domain.com>"
---@return boolean - When true, link was handled, when false, continue to the next source
function SendMail:follow(link)
  if not vim.startswith(link, "mailto:") then
    return false
  end
  local mail = link:sub(8)
  mail = vim.trim(mail)
  Snacks.terminal.open({ "neomutt", "--", mail }, { win = { position = "bottom", height = 0.5 } })
  return true
end

require("orgmode").setup({
  hyperlinks = {
    sources = {
      LinkPingType,
      RunShellCommand,
      SendMail,
      --      {
      --        get_name = function()
      --          return "mailto"
      --        end,
      --        follow = function(self, link)
      --          local mail = link:sub(8)
      --          vim.cmd("split | term neomutt -- " .. mail)
      --          return true
      --        end,
      --        autocomplete = function(self, link)
      --          return { "my_custom_type:my_custom_link" }
      --        end,
      --      },
    },
  },
})
