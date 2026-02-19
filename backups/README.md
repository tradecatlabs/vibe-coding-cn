# 快速备份工具

基于 `.gitignore` 规则的项目备份工具，自动排除不需要的文件。

## 功能特性

- 自动读取 `.gitignore` 规则
- 支持取反规则（`!` 语法）
- 目录级剪枝优化
- 生成 `.tar.gz` 压缩包
- 零依赖（仅使用 Python 内置模块）

## 文件结构

```
backups/
├── 快速备份.py    # 核心备份引擎
├── 一键备份.sh    # Shell 启动脚本
└── README.md      # 本文档
```

## 使用方法

```bash
# 方式一：Shell 脚本（推荐）
bash backups/一键备份.sh

# 方式二：直接运行 Python
python3 backups/快速备份.py

# 指定输出文件
python3 backups/快速备份.py -o my_backup.tar.gz

# 指定项目目录
python3 backups/快速备份.py -p /path/to/project
```

## 输出位置

默认输出到 `backups/gz/备份_YYYYMMDD_HHMMSS.tar.gz`

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-p, --project` | 项目根目录 | 当前目录 |
| `-o, --output` | 输出文件路径 | `backups/gz/备份_时间戳.tar.gz` |
| `-g, --gitignore` | gitignore 文件路径 | `.gitignore` |

## 依赖

- Python 3.x（无需额外包）
- Bash（用于 Shell 脚本）
