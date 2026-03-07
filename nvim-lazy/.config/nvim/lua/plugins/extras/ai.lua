---@diagnostic disable: undefined-global

return {
  {
    "NickvanDyke/opencode.nvim",
    lazy = true,
    event = "VeryLazy",
    config = function()
      local opencode_cmd = "opencode --port"
      local snacks_terminal_opts = {
        win = {
          position = "bottom",
          height = 0.5,
          enter = false,
          on_win = function(win)
            -- Set up keymaps and cleanup for an arbitrary terminal
            require("opencode.terminal").setup(win.win)
          end,
        },
      }
      vim.g.opencode_opts = {
        server = {
          start = function()
            require("snacks.terminal").open(opencode_cmd, snacks_terminal_opts)
          end,
          stop = function()
            local term = require("snacks.terminal").get(opencode_cmd, snacks_terminal_opts)
            if term and term.buf then
              local job_id = vim.b[term.buf].terminal_job_id
              if job_id then
                local pid = vim.fn.jobpid(job_id)
                if pid > 0 then
                  vim.fn.system("kill -TERM -" .. pid)
                end
                vim.fn.jobstop(job_id)
              end
              term:close()
            end
          end,
          toggle = function()
            require("snacks.terminal").toggle(opencode_cmd, snacks_terminal_opts)
          end,
        },
      }
      vim.keymap.set({ "n", "x" }, "<leader>aA", function()
        require("opencode").ask("", { submit = false })
      end, { desc = "Ask opencode" })
      vim.keymap.set({ "n", "x" }, "<leader>aat", function()
        require("opencode").ask("@this: ", { submit = false })
      end, { desc = "Ask opencode this" })
      vim.keymap.set({ "n", "x" }, "<leader>aab", function()
        require("opencode").ask("@buffer: ", { submit = false })
      end, { desc = "Ask opencode buffer" })
      vim.keymap.set({ "n", "x" }, "<leader>aaB", function()
        require("opencode").ask("@buffer: ", { submit = false })
      end, { desc = "Ask opencode buffers" })
      vim.keymap.set({ "n", "x" }, "<leader>aav", function()
        require("opencode").ask("@visible: ", { submit = false })
      end, { desc = "Ask opencode visible" })
      vim.keymap.set({ "n", "x" }, "<leader>aad", function()
        require("opencode").ask("@diagnostic: ", { submit = false })
      end, { desc = "Ask opencode diagnostic" })
      vim.keymap.set({ "n", "x" }, "<leader>aaf", function()
        require("opencode").ask("@quickfix: ", { submit = false })
      end, { desc = "Ask opencode quickfix" })
      vim.keymap.set({ "n", "x" }, "<leader>aai", function()
        require("opencode").ask("@diff: ", { submit = false })
      end, { desc = "Ask opencode diff" })
      vim.keymap.set({ "n", "x" }, "<leader>aam", function()
        require("opencode").ask("@marks: ", { submit = false })
      end, { desc = "Ask opencode marks" })
      vim.keymap.set({ "n", "x" }, "<leader>a<CR>", function()
        require("opencode").command("propmpt.enter")
      end, { desc = "Submit opencode prompt" })
      vim.keymap.set({ "n", "x" }, "<leader>ax", function()
        require("opencode").select()
      end, { desc = "Execute opencode action…" })
      vim.keymap.set({ "n", "x" }, "<leader>a<tab>", function()
        require("opencode").command("agent.cycle")
      end, { desc = "Cycle opencode agent" })
      vim.keymap.set({ "n", "x" }, "<leader>ak", function()
        require("opencode").command("session.interrupt")
      end, { desc = "Interrupt opencodesession" })
      vim.keymap.set({ "n", "x" }, "<leader>ag", function()
        require("opencode").prompt("@this")
      end, { desc = "Add to opencode" })
      vim.keymap.set({ "n", "t" }, "<leader>at", function()
        require("opencode").toggle()
      end, { desc = "Toggle opencode" })
      vim.keymap.set({ "n", "t" }, "<leader>ae", function()
        require("opencode").command("prompt.editor")
      end, { desc = "Opencode editor" })
      vim.keymap.set({ "n", "t" }, "<leader>aq", function()
        vim.g.opencode_opts.server.stop()
      end, { desc = "Exit Opencode session" })
    end,
  },
}
