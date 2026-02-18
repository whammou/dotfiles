---@diagnostic disable: undefined-global

return {
  {
    "NickvanDyke/opencode.nvim",
    config = function()
      vim.g.opencode_opts = {
        provider = {
          enabled = "snacks",
          snacks = {
            win = {
              position = "bottom",
              height = 0.5,
            },
          },
        },
      }
      vim.keymap.set({ "n", "x" }, "<leader>aa", function()
        require("opencode").ask("@this: ", { submit = true })
      end, { desc = "Ask opencode" })
      vim.keymap.set({ "n", "x" }, "<leader>ax", function()
        require("opencode").select()
      end, { desc = "Execute opencode action…" })
      vim.keymap.set({ "n", "x" }, "<leader>ag", function()
        require("opencode").prompt("@this")
      end, { desc = "Add to opencode" })
      vim.keymap.set({ "n", "t" }, "<leader>at", function()
        require("opencode").toggle()
      end, { desc = "Toggle opencode" })
      vim.keymap.set({ "n", "t" }, "<leader>ae", function()
        require("opencode").command("prompt.editor")
      end, { desc = "Opencode editor" })
    end,
  },
}
