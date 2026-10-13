#!/usr/bin/env lua
-- 主题预览器 - 简化版
-- 用法: nvim -u theme-previewer.lua

-- 临时配置目录
local tmp_dir = "/tmp/nvim-theme-preview"
os.execute("mkdir -p " .. tmp_dir)

-- 写入基础配置
local init_lua = tmp_dir .. "/init.lua"
local file = io.open(init_lua, "w")
if not file then
  print("无法创建临时配置")
  os.exit(1)
end

file:write([[
-- 最小化主题预览配置
vim.opt.termguicolors = true
vim.opt.background = "dark"

-- 主题列表
local themes = {
  dracula = function()
    package.path = package.path .. ";" .. vim.fn.stdpath("config") .. "/lua/?.lua"
    require('plugins.dracula')
  end,
  onedark = function()
    vim.cmd [[colorscheme onedark]]
  end,
  tokyonight = function()
    require('tokyonight').setup({style = 'night'})
    vim.cmd.colorscheme('tokyonight')
  end,
  catppuccin = function()
    require('catppuccin').setup({flavour = 'mocha'})
    vim.cmd.colorscheme('catppuccin')
  end,
  gruvbox = function()
    require('gruvbox').setup({contrast = 'hard'})
    vim.cmd.colorscheme('gruvbox')
  end,
}

-- 获取主题参数
local theme = arg[1] or 'dracula'

-- 应用主题
if themes[theme] then
  themes[theme]()
else
  print("未知主题: " .. theme)
  print("可用主题: " .. table.concat(vim.tbl_keys(themes), ", "))
end

-- 预览内容
vim.api.nvim_buf_set_lines(0, 0, -1, false, {
  "🎨 " .. theme .. " 主题预览",
  "",
  "-- Lua 代码示例",
  "local function hello_world()",
  "  print('Hello, World!')  -- 注释",
  "  local dracula = '🧛'",
  "  return dracula",
  "end",
  "",
  "-- JavaScript 代码示例",
  "function hello() {",
  "  console.log('Hello, World!');",
  "  const theme = '" .. theme .. "';",
  "  return theme;",
  "}",
  "",
  "快捷键: q 退出预览",
})

-- 设置快捷键
vim.keymap.set('n', 'q', ':qa!<CR>', {noremap = true, silent = true})
vim.keymap.set('n', '<Esc>', ':qa!<CR>', {noremap = true, silent = true})

print("🎨 预览 " .. theme .. " 主题")
print("按 q 退出预览")
]])

file:close()

-- 启动 nvim
local cmd = string.format("nvim -u %s", init_lua)
os.execute(cmd)

-- 清理
os.execute("rm -rf " .. tmp_dir)