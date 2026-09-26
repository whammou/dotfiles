local M = {}

local agenda_submenus = {}
local capture_templates_ref

local function split_extended_commands(extended)
  local flat, submenus = {}, {}
  for key, def in pairs(extended) do
    if def.submenu then
      submenus[key] = def
    else
      flat[key] = def
    end
  end
  return flat, submenus
end

local function patch_agenda_menu()
  local ok, org = pcall(require, "orgmode")
  if not ok then
    return
  end
  local instance = org.instance()
  if not instance or not instance.agenda then
    return
  end
  local Agenda = getmetatable(instance.agenda) or instance.agenda
  if Agenda._submenu_patched then
    return
  end
  local orig_build_menu = Agenda._build_menu
  if not orig_build_menu then
    return
  end

  Agenda._build_menu = function(self)
    local menu = orig_build_menu(self)
    local Menu = require("orgmode.ui.menu")
    local AgendaTypes = require("orgmode.agenda.types")
    local utils = require("orgmode.utils")

    local function build_views_from_types(types, id_prefix)
      local views = {}
      for i, agenda_type in ipairs(types) do
        local base = {
          agenda = {
            span = agenda_type.org_agenda_span,
            start_day = agenda_type.org_agenda_start_day,
            start_on_weekday = agenda_type.org_agenda_start_on_weekday,
          },
          tags = {
            match_query = agenda_type.match,
            todo_ignore_scheduled = agenda_type.org_agenda_todo_ignore_scheduled,
            todo_ignore_deadlines = agenda_type.org_agenda_todo_ignore_deadlines,
          },
          tags_todo = {
            match_query = agenda_type.match,
            todo_ignore_scheduled = agenda_type.org_agenda_todo_ignore_scheduled,
            todo_ignore_deadlines = agenda_type.org_agenda_todo_ignore_deadlines,
          },
          agenda_entry = {
            span = agenda_type.org_agenda_span,
          },
        }
        local opts = base[agenda_type.type]
        if not opts then
          if agenda_type.type == "agenda" then
            opts = base.agenda
          else
            utils.echo_error("Invalid submenu type " .. tostring(agenda_type.type))
            break
          end
        end
        opts.sorting_strategy = agenda_type.org_agenda_sorting_strategy
        opts.agenda_filter = self.filters
        opts.files = self.files
        opts.header = agenda_type.org_agenda_overriding_header
        opts.agenda_files = agenda_type.org_agenda_files
        opts.tag_filter = agenda_type.org_agenda_tag_filter_preset
        opts.category_filter = agenda_type.org_agenda_category_filter_preset
        opts.highlighter = self.highlighter
        opts.remove_tags = agenda_type.org_agenda_remove_tags
        opts.id = string.format("%s_%s_%d", id_prefix, agenda_type.type, i)
        local view = AgendaTypes[agenda_type.type]:new(opts)
        if view then
          table.insert(views, view)
        end
      end
      return views
    end

    local function make_types_action(types, id_prefix)
      return function()
        self.views = build_views_from_types(types, id_prefix)
        return self:prepare_and_render():next(function()
          if #self.views > 1 then
            vim.fn.cursor({ 1, 0 })
          end
        end)
      end
    end

    local function insert_before_quit(item)
      local quit_idx
      for i, entry in ipairs(menu.items) do
        if entry.key == "q" and entry.label == "Quit" then
          quit_idx = i
          break
        end
      end
      if quit_idx then
        table.insert(menu.items, quit_idx, item)
      else
        menu:add_option(item)
      end
    end

    local function build_submenu_menu(def, prefix, title_prefix)
      local title = string.format("%s  (%s)", def.description or prefix, prefix)
      local prompt = string.format("Press key for %s", def.description or prefix)
      if title_prefix then
        title = title_prefix .. " → " .. title
      end
      local sub = Menu:new({ title = title, prompt = prompt })
      for subkey, child in pairs(def.submenu or {}) do
        local child_prefix = prefix .. subkey
        if child.submenu then
          local nested_title_prefix = def.description or prefix
          sub:add_option({
            label = (child.description or child_prefix) .. " ▶",
            key = subkey,
            action = function()
              return build_submenu_menu(child, child_prefix, nested_title_prefix):open()
            end,
          })
        elseif child.types then
          sub:add_option({
            label = child.description or child_prefix,
            key = subkey,
            action = make_types_action(child.types, "submenu_" .. child_prefix:gsub("[^%w]", "_")),
          })
        end
      end
      sub:add_separator()
      sub:add_option({ label = "Quit", key = "q" })
      sub:add_separator({ icon = " ", length = 1 })
      return sub
    end

    for key, def in pairs(agenda_submenus) do
      insert_before_quit({
        label = (def.description or key) .. " ▶",
        key = key,
        action = function()
          return build_submenu_menu(def, key):open()
        end,
      })
    end

    return menu
  end

  Agenda._submenu_patched = true
end

local setup_fn
local function setup_org_capture_template()
  local extended = M._extended or {}
  local flat, submenus = split_extended_commands(extended)
  agenda_submenus = submenus
  require("orgmode").setup({
    org_capture_templates = capture_templates_ref,
    org_agenda_custom_commands = flat,
  })
end

function M.setup(extended_commands, capture_templates)
  M._extended = extended_commands
  capture_templates_ref = capture_templates
  setup_fn = setup_org_capture_template
  setup_fn()
  pcall(patch_agenda_menu)
  local orig = setup_fn
  setup_fn = function(...)
    local r = orig(...)
    pcall(patch_agenda_menu)
    return r
  end
  vim.api.nvim_create_user_command("ReloadOrgConfig", setup_fn, {
    desc = "Reloads Orgmode capture templates and related configuration",
  })
  M._setup_fn = setup_fn
  M._patch = patch_agenda_menu
end

return M
