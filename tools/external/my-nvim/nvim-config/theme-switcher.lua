#!/usr/bin/env lua
-- Neovim 主题切换脚本
-- 用法: nvim -l theme-switcher.lua <主题名> [样式]

local themes = {
  dracula = {
    plugin = 'Mofiqul/dracula.nvim',
    setup = function(style)
      local opts = {
        theme = style or 'dracula',  -- dracula, dracula-soft, day
        transparent_bg = false,
        italic_comment = true,
        show_end_of_buffer = true,
      }
      require('dracula').setup(opts)
    end
  },
  catppuccin = {
    plugin = 'catppuccin/nvim',
    setup = function(style)
      local flavours = { 'mocha', 'macchiato', 'frappe', 'latte' }
      local flavour = style and flavours[tonumber(style)] or 'mocha'
      require('catppuccin').setup({ flavour = flavour })
    end
  },
  tokyonight = {
    plugin = 'folke/tokyonight.nvim',
    setup = function(style)
      local opts = {
        style = style or 'night',  -- night, storm, day, moon
        transparent = false,
        terminal_colors = true,
      }
      require('tokyonight').setup(opts)
    end
  },
  gruvbox = {
    plugin = 'ellisonleao/gruvbox.nvim',
    setup = function(style)
      local opts = {
        contrast = style or 'hard',  -- soft, medium, hard
        transparent_mode = false,
      }
      require('gruvbox').setup(opts)
    end
  },
  onedark = {
    plugin = 'navarasu/onedark.nvim',
    setup = function(style)
      local opts = {
        style = style or 'dark',  -- dark, darker, cool, deep, warm, warmer
        transparent = false,
      }
      require('onedark').setup(opts)
    end
  }
}

-- 解析命令行参数
local theme_name = arg[1]
local style = arg[2]

if not theme_name then
  print("\n🎨 Neovim 主题切换器")
  print("用法: nvim -l theme-switcher.lua <主题> [样式]")
  print("\n可用主题:")
  for name, info in pairs(themes) do
    print(string.format("  %-12s %s", name, info.plugin))
  end
  print("\n示例:")
  print("  nvim -l theme-switcher.lua dracula dracula-soft")
  print("  nvim -l theme-switcher.lua catppuccin 1  (1=mocha,2=macchiato,3=frappe,4=latte)")
  print("  nvim -l theme-switcher.lua tokyonight storm")
  os.exit(0)
end

-- 检查主题是否存在
if not themes[theme_name] then
  print("❌ 未知主题: " .. theme_name)
  print("可用主题: " .. table.concat(vim.tbl_keys(themes), ", "))
  os.exit(1)
end

-- 生成临时配置文件
local config_content = string.format([[
-- 临时主题配置 - %s
vim.cmd [[set runtimepath+=~/.config/nvim]]

-- 安装主题插件
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  { "%s", priority = 1000 },
})

-- 设置主题
%s
vim.cmd.colorscheme("%s")

-- 打开一个新文件查看效果
vim.cmd [[enew]]
vim.api.nvim_buf_set_lines(0, 0, -1, false, {
  "🎨 主题预览: %s",
  "",
  "function hello() {",
  "  console.log('Hello, World!');",
  "  // This is a comment",
  "  const dracula = '🧛';",
  "  return dracula;",
  "}",
  "",
  "local themes = {",
  "  dracula = 'dark',",
  "  catppuccin = 'soft',",
  "}",
})

-- 设置快捷键
vim.keymap.set('n', 'q', ':qa!<CR>', { noremap = true, silent = true })
vim.keymap.set('n', '<Esc>', ':qa!<CR>', { noremap = true, silent = true })

print("\n🎨 主题预览: %s (%s)")
print("按 q 或 Esc 退出预览")
]],
  theme_name,
  themes[theme_name].plugin,
  themes[theme_name].setup(style),
  theme_name,
  theme_name,
  theme_name,
  style or "default"
)

-- 写入临时配置
local tmp_config = "/tmp/nvim-theme-preview.lua"
local file = io.open(tmp_config, "w")
if file then
  file:write(config_content)
  file:close()

  -- 启动 neovim 预览
  local cmd = string.format("nvim -u %s", tmp_config)
  print(string.format("\n🎨 启动 %s 主题预览 (%s)...", theme_name, style or "default"))
  os.execute(cmd)

  -- 清理临时文件
  os.remove(tmp_config)
else
  print("❌ 无法创建临时配置文件")
  os.exit(1)
end