require("nvmm").setup({
  mappings = {
    attachment = "<leader>ma",
    config = "<leader>mc",
    preview = "<leader>mp",
    send_text = "<leader>mst",
    send_html = "<leader>msh",
  },
  options = {
    mail_client = {
      text = "neomutt", -- or "mailx"
      html = "neomutt",
    },
    auto_break_md = true, -- line breaks without two spaces for markdown
    neomutt_config = vim.fn.expand("~/.config/neomutt/account.com.gmail.account1"),
    mailx_account = nil, -- if you use different accounts in .mailrc
    save_log = true,
    log_file = vim.fn.expand("~/Mail/.nvmm.log"),
    date_format = "%Y-%m-%d",
    pandoc_metadatas = { -- syntax with [['metadata']] is important
      [['title= ']],
      [['margin-top=0']],
      [['margin-left=0']],
      [['margin-right=0']],
      [['margin-bottom=0']],
      [['mainfont: sans-serif']],
    },
  },
})
