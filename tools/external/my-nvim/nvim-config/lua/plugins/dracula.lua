-- Dracula 主题插件配置

return {
  {
    'Mofiqul/dracula.nvim',
    name = 'dracula',
    lazy = false,
    priority = 1000,
    config = function()
      -- 获取主题配置
      local dracula_config = require('themes.dracula')

      -- 从环境变量或默认值获取样式
      local style = vim.env.NVIM_THEME_STYLE or 'dracula'

      -- 设置主题
      require('dracula').setup(dracula_config.config(style))

      -- 应用主题
      vim.cmd.colorscheme('dracula')
    end,
  },

  -- Lualine 主题集成
  {
    'nvim-lualine/lualine.nvim',
    dependencies = { 'dracula' },
    opts = {
      options = {
        theme = 'dracula-nvim'
      }
    }
  }
}