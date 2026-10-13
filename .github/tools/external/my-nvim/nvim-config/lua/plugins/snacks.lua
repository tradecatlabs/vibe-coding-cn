return {
  {
    "folke/snacks.nvim",
    opts = function(_, opts)
      -- ==================== 默认显示隐藏/被忽略文件 ====================
      -- LazyVim install_version=8 默认 picker/explorer 都优先走 Snacks，这里统一打开 hidden/ignored。
      opts.picker = opts.picker or {}
      opts.picker.sources = opts.picker.sources or {}

      local sources = opts.picker.sources
      sources.files = vim.tbl_deep_extend("force", sources.files or {}, {
        hidden = true,
        ignored = true,
      })

      sources.explorer = vim.tbl_deep_extend("force", sources.explorer or {}, {
        hidden = true,
        ignored = true,
      })

      sources.grep = vim.tbl_deep_extend("force", sources.grep or {}, {
        hidden = true,
        ignored = true,
      })
    end,
  },
}

