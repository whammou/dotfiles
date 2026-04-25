-- Add this helper function after line 26 (after current_time function):

local function headline_custom_id()
  return f(function()
    local ok, api = pcall(require, 'orgmode.api')
    if not ok then
      return ''
    end

    local file = api.current()
    if not file then
      return ''
    end

    local headline = file:get_closest_headline()
    if not headline or not headline.title then
      return ''
    end

    -- Convert to GitHub markdown snake-case
    local title = headline.title
    local custom_id = title
      :gsub('%s+', '-')
      :gsub('[^a-zA-Z0-9%-]', '')
      :lower()

    return ':CUSTOM_ID: ' .. custom_id
  end, {})
end


-- Add this snippet inside ls.add_snippets("org", {...}):

s(":CUSTOM_ID", {
  headline_custom_id(),
}, { desc = "CUSTOM_ID from current headline" }),