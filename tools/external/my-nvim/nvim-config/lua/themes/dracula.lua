-- Dracula 主题配置
-- 支持多种变体: dracula, dracula-soft, day

local M = {}

M.config = function(style)
  local opts = {
    -- 主题变体: dracula, dracula-soft, day
    theme = style or 'dracula',

    -- 透明背景
    transparent_bg = false,

    -- 斜体注释
    italic_comment = true,

    -- 显示文件末尾的 ~ 符号
    show_end_of_buffer = true,

    -- Lualine 背景色
    lualine_bg_color = '#44475a',
  }

  -- 高级自定义选项（可选）
  if style == 'soft' then
    opts.colors = {
      -- 更柔和的背景色
      bg = '#21222c',
      fg = '#f8f8f2',
    }
  elseif style == 'day' then
    opts.colors = {
      -- 浅色主题配色
      bg = '#f8f8f2',
      fg = '#282a36',
    }
  end

  return opts
end

-- 主题信息
M.info = {
  name = 'dracula',
  plugin = 'Mofiqul/dracula.nvim',
  variants = {
    { name = 'dracula', desc = '经典深色主题' },
    { name = 'dracula-soft', desc = '柔和深色主题' },
    { name = 'day', desc = '浅色主题' },
  },
  features = {
    '支持透明背景',
    '斜体注释',
    '完整的 LSP 和 Treesitter 支持',
    'Lualine 主题集成',
    '多插件支持（Telescope, NvimTree 等）',
  }
}

return M