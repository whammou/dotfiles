local M = {}

local applied = false

-- bloocky updates a cached block by copying only the keys carried by the pulled
-- event. A timed event has no all_day key, so a block that used to be date-based
-- keeps a stale all_day flag and renders in the all-day strip (four rows plus a
-- "+N more" line) instead of its hour slot. Date-based blocks always carry
-- start_min = 0, so a non-zero start proves the flag is stale.
local function repair(blocks)
  local repaired = false
  for _, block in ipairs(blocks) do
    if block.all_day and (block.start_min or 0) ~= 0 then
      block.all_day = nil
      repaired = true
    end
  end
  return repaired
end

function M.apply()
  if applied then
    return
  end
  applied = true

  local state = require("bloocky.state")
  local save_blocks = state.save_blocks

  state.save_blocks = function(...)
    repair(state.blocks)
    return save_blocks(...)
  end

  state.ensure_loaded()
  if repair(state.blocks) then
    state.save_blocks()
  end
end

return M
