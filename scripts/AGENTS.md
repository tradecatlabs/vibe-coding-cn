# scripts/ Agent 指南

本目录维护仓库级自动化脚本，主要用于 Markdown、链接、锚点、metadata 和 AI 引用资产校验。

## 约束

- 脚本默认从仓库根目录运行，路径解析必须稳定。
- 新增检查脚本时，同步更新 `scripts/README.md`、`Makefile`、CI 和根目录 `AGENTS.md` 的命令清单。
- 检查失败输出应包含文件路径、行号或可定位的错误信息。
- 跳过目录必须明确，至少跳过 `.git`、`.history`、`node_modules` 和外部源码快照。

## 验证

```bash
make test
```
