-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

-- ==================== 文件搜索：包含隐藏/被忽略文件 ====================
-- 说明：
-- - LazyVim 默认 <leader>ff 通常不包含 .gitignore 忽略的文件
-- - 这个快捷键用于“真的找不到文件时”兜底（例如 .env）
vim.keymap.set("n", "<leader>fF", function()
  require("telescope.builtin").find_files({
    hidden = true,
    no_ignore = true,
    no_ignore_parent = true,
  })
end, { desc = "Find All Files (hidden + ignored)" })
