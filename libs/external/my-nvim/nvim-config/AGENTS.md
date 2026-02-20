# Neovim 配置（LazyVim）说明

本目录是一套可直接复制到 `~/.config/nvim/` 的 Neovim 配置，基于 LazyVim + lazy.nvim。

## 目录结构

```text
nvim-config/
├── init.lua                 # 入口：加载 config.lazy
├── lazy-lock.json           # 插件锁定版本
├── lazyvim.json             # LazyVim 元数据（extras/install_version）
└── lua/
    ├── config/              # options/keymaps/autocmds/lazy 基础配置
    └── plugins/             # 以“文件为单位”的插件/覆盖配置
        ├── ui.lua           # UI（neo-tree/bufferline 等）覆盖
        └── snacks.lua       # Snacks 默认策略（显示隐藏/被忽略文件）
```

## 关键约定

- 对人可见文本（注释/日志/文档）用中文；代码符号（变量/函数/模块名）用英文。
- 插件覆盖优先放在 `lua/plugins/*.lua`，避免在 `config/*` 里堆逻辑。
- “默认显示隐藏文件”的入口在 `lua/plugins/snacks.lua`：
  - `picker.sources.files/explorer/grep`: `hidden=true`、`ignored=true`

## 变更记录

- 2026-02-20：新增 `lua/plugins/snacks.lua`，让 Snacks Explorer/Picker 默认显示隐藏与被忽略文件。

