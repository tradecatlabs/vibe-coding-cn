-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua
--
-- Add any additional autocmds here
-- with `vim.api.nvim_create_autocmd`
--
-- Or remove existing autocmds by their group name (which is prefixed with `lazyvim_` for the defaults)
-- e.g. vim.api.nvim_del_augroup_by_name("lazyvim_wrap_spell")

-- 自动打开Neotree（使用标准LazyVim方式）
vim.api.nvim_create_autocmd("VimEnter", {
  callback = function()
    -- 延迟执行，确保插件加载完成
    vim.defer_fn(function()
      vim.cmd("Neotree show")
    end, 50)
  end,
})

-- 确保bufferline始终显示
vim.api.nvim_create_autocmd("VimEnter", {
  callback = function()
    vim.o.showtabline = 2
  end,
})