# 提示词文件组维护指南

## 用途

提示词库入口文件平铺在`.github/`根；README和AGENTS指南因重名分别命名为`prompts-README.md`与`prompts-AGENTS.md`，实际提示词内容以云端表格为准。

## 在线资源

**主表格**：[提示词云端表格](https://docs.google.com/spreadsheets/d/1Ifk_dLF25ULSxcfGem1hXzJsi7_RBUNAki8SBCuvkJA/edit?gid=1254297203#gid=1254297203)

**原版表格**：[原版本（非直观易读）](https://docs.google.com/spreadsheets/d/1ngoQOhJqdguwNAilCl1joNwTje7FWWN9WiI2bo5VhpU/edit?gid=1890901677#gid=1890901677)

## 表格结构

- **工作表**：每个 Sheet 代表一类提示词
- **横轴**：提示词迭代版本（1a → 1b → 1c）
- **纵轴**：不同提示词（提示词1、提示词2、...）

## 操作规范

### 允许
- 更新`.github/prompts-README.md`中的链接和说明
- 同步云端表格的结构变化到文档

### 禁止
- 在本地创建提示词文件（应添加到云端表格）
- 删除`.github/prompts-README.md`
- 不在本组文件中写入敏感信息（密钥/Token/个人路径等）

## 工具状态

提示词格式转换程序已从当前仓库退役。本组文件仍只提供云端表格入口；历史实现不构成当前执行入口。
