local M = {}

local state = nil ---@type {url:string, src:string, win:snacks.win, img:snacks.image.Placement}?

function M.close()
  if state then
    pcall(state.win.close, state.win)
    pcall(state.img.close, state.img)
    state = nil
  end
end

function M.is_open()
  return state ~= nil
end

local function open_win(url, dst)
  if not (pcall(require, "snacks")) then
    return
  end
  local win = Snacks.win(Snacks.win.resolve(Snacks.image.config.doc, "snacks_image", {
    show = false,
    enter = false,
    wo = { winblend = Snacks.image.terminal.env().placeholders and 0 or nil },
  }))
  win:open_buf()
  local img, updated = nil, false
  local o = Snacks.config.merge({}, Snacks.image.config.doc, {
    on_update_pre = function()
      if not updated then
        updated = true
        local loc = img:state().loc
        win.opts.width = loc.width
        win.opts.height = loc.height
        win:show()
      end
    end,
    inline = false,
  })
  img = Snacks.image.placement.new(win.buf, dst, o)
  state = { url = url, src = dst, win = win, img = img }
  vim.api.nvim_create_autocmd({ "CursorMoved", "ModeChanged", "BufLeave" }, {
    group = vim.api.nvim_create_augroup("snacks.image.url_preview", { clear = true }),
    callback = function()
      M.close()
    end,
  })
end

function M.preview_url(url)
  local ok = pcall(require, "snacks")
  if not ok then
    return
  end

  if state then
    if state.url == url then
      M.close()
      return
    end
    M.close()
  end

  local ok_doc, doc = pcall(require, "snacks.image.doc")
  if ok_doc then
    doc.hover_close()
  end

  local cache = Snacks.image.config.cache
    or (vim.fn.stdpath("cache") .. "/snacks/image")
  vim.fn.mkdir(cache, "p")

  local hash = vim.fn.sha256(url):sub(1, 12)
  local dst = cache .. "/url_" .. hash .. ".png"
  if vim.fn.filereadable(dst) == 1 then
    open_win(url, dst)
    return
  end

  vim.notify("Capturing " .. url .. " …", vim.log.levels.INFO)
  vim.fn.jobstart({ "url2png", url, dst }, {
    on_exit = function(_, exit_code)
      vim.schedule(function()
        if exit_code ~= 0 then
          vim.notify("url2png failed for: " .. url, vim.log.levels.WARN)
          return
        end
        if vim.fn.expand("<cfile>") ~= url then
          vim.notify("Captured " .. url .. " (cursor moved)", vim.log.levels.INFO)
          return
        end
        vim.notify("Captured " .. url, vim.log.levels.INFO)
        open_win(url, dst)
      end)
    end,
  })
end

return M
