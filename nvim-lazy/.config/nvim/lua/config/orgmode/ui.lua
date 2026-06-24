local Menu = require("org-modern.menu")

require("orgmode").setup({
  ui = {
    agenda = {
      preview_window = {
        wrap = true,
        border = "single",
        anchor_bias = "above",
        focusable = true,
      },
    },
    menu = {
      handler = function(data)
        Menu:new({
          window = {
            margin = { 1, 0, 1, 0 },
            padding = { 0, 1, 0, 1 },
            title_pos = "center",
            border = "single",
            zindex = 1000,
          },
          icons = {
            separator = "➜",
          },
        }):open(data)
      end,
    },
  },
})

-- Monkey-patch preview_item to strip headlines.nvim fat_headline virt_lines
-- from the preview floating buffer. headlines.nvim's refresh() fires on the
-- Syntax event (when filetype = 'org' is set), adding virt_lines/virt_lines_above
-- around headlines that the window wasn't sized for, pushing notes out of view.
do
  local ok, org = pcall(require, "orgmode")
  if ok then
    local instance = org.instance()
    if instance and instance.agenda then
      local Agenda = getmetatable(instance.agenda)
      if Agenda then
        local orig_preview_item = Agenda.preview_item
        Agenda.preview_item = function(self)
          local headline = self:get_headline_at_cursor()
          if not headline then
            return
          end

          local lines = headline:get_lines()
          local offset = 4
          local width = lines[1]:len() + offset

          vim.tbl_map(function(line)
            width = math.max(width, line:len() + offset)
          end, lines)

          local win_opts = vim.tbl_deep_extend("force", {
            width = width,
          }, require("orgmode.config").ui.agenda.preview_window or {})

          local buf = vim.lsp.util.open_floating_preview(lines, "", win_opts)
          vim.api.nvim_set_option_value("filetype", "org", { buf = buf })

          pcall(vim.api.nvim_buf_clear_namespace, buf,
            vim.api.nvim_create_namespace("headlines_namespace"), 0, -1)
        end
      end
    end
  end
end
