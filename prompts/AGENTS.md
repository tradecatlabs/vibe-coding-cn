# Prompts 目录 Agent 指南

## 目录用途

`prompts/` 提示词库入口，实际内容已迁移至云端表格。

## 在线资源

**主表格**：[提示词云端表格](https://docs.google.com/spreadsheets/d/1Ifk_dLF25ULSxcfGem1hXzJsi7_RBUNAki8SBCuvkJA/edit?gid=1254297203#gid=1254297203)

**原版表格**：[原版本（非直观易读）](https://docs.google.com/spreadsheets/d/1ngoQOhJqdguwNAilCl1joNwTje7FWWN9WiI2bo5VhpU/edit?gid=1890901677#gid=1890901677)

## 表格结构

- **工作表**：每个 Sheet 代表一类提示词
- **横轴**：提示词迭代版本（1a → 1b → 1c）
- **纵轴**：不同提示词（提示词1、提示词2、...）

## 操作规范

### 允许
- 更新 README.md 中的链接和说明
- 同步云端表格的结构变化到文档

### 禁止
- 在本地创建提示词文件（应添加到云端表格）
- 删除 README.md
 - 在本目录写入敏感信息（密钥/Token/个人路径等）

## 相关工具

- `assets/repo/prompts-library/` - Excel ↔ Markdown 互转工具
