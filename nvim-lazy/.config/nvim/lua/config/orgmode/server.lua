---@diagnostic disable: undefined-global

local M = {}

local started = false

function M.setup()
  -- Only start one Org server per session
  if started then
    return
  end

  local socket_dir = os.getenv("XDG_RUNTIME_DIR")
  if not socket_dir or socket_dir == "" then
    socket_dir = os.getenv("TMPDIR")
    if not socket_dir or socket_dir == "" then
      socket_dir = "/tmp/nvim." .. (os.getenv("USER") or "user")
    end
  end

  -- Ensure directory exists
  if vim.fn.isdirectory(socket_dir) == 0 then
    vim.fn.mkdir(socket_dir, "p")
  end

  local base_name = "nvim-orgmode"
  local counter = 1
  local socket_path = ""

  -- Find an available socket name
  while true do
    local path = socket_dir .. "/" .. base_name .. "-" .. counter .. ".socket"
    if vim.loop.fs_stat(path) == nil then
      socket_path = path
      break
    end
    counter = counter + 1
  end

  local ok, err = pcall(vim.fn.serverstart, socket_path)
  if ok then
    started = true
    -- vim.notify("Org server started: " .. socket_path, vim.log.levels.INFO)
  else
    vim.notify("Failed to start Org server: " .. tostring(err), vim.log.levels.ERROR)
  end
end

-- Filter noweb syntax diagnostics (<< >>) from org LSP output
local function setup_lsp_filter()
	local orig_handler = vim.lsp.handlers["textDocument/publishDiagnostics"]
	vim.lsp.handlers["textDocument/publishDiagnostics"] = function(err, result, ctx, config)
		if result and result.diagnostics then
			local client = vim.lsp.get_client_by_id(ctx.client_id)
			if client and client.name == "org" then
				result.diagnostics = vim.tbl_filter(function(d)
					return not d.message:find("<<") and not d.message:find(">>")
				end, result.diagnostics)
			end
		end
		orig_handler(err, result, ctx, config)
	end
end

-- Run immediately when required
M.setup()
setup_lsp_filter()

return M
