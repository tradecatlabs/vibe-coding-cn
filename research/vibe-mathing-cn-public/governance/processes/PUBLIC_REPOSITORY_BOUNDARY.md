---
id: PROC-PUBLIC-REPOSITORY-BOUNDARY
type: process
status: current
owner: engineering
created: 2026-08-29
last_reviewed: 2026-08-29
review_cycle: P90D
---

# 公开仓库发布边界

## 定位

本仓库只保存可公开、可移植、可从零验证的工程核心。私密数学探索、原始计算、运行状态、恢复快照和内部基础设施记录在独立的私密研究仓中维护，不从本仓库反向推断其状态。

## 允许内容

- Problem、Attempt、Result、ResearchBundle schema 与准入代码；
- 合成 fixture、攻击负例和可重复测试；
- 已完成许可审计的最小供应链元数据；
- 不包含私密运行事实的公开文档；
- 经公开准入门验证且明确批准发布的 Result 与证据。

## 禁止内容

- Millennium 或其他活动研究工作树的原始计算；
- `research/runs/`、研究 artifact、worker goal、验证 ledger 和恢复快照；
- `.olean`、日志、PDF、数据库、压缩归档、模型或构建缓存；
- 密钥、token、私有端点、私有 IP、用户主目录绝对路径或 WSL UNC 路径；
- 私密仓 remote、分支或提交历史的整体导入。

## 发布流程

1. 从批准的固定源提交按显式文件清单导出到新的临时 staging。
2. 不复制源工作树，不把私密仓添加为本仓可推送 remote。
3. 对 staging 执行路径、内容、凭据、许可证和大文件扫描。
4. 只把审查后的文件变化应用到公开工程分支。
5. 运行 `make check`，再以普通 merge 合入公开 `main`。
6. push 是独立动作；未经明确批准不得自动执行。

## 机械门禁

```bash
python3 scripts/test_validate_public_boundary.py
python3 scripts/validate_public_boundary.py --project-root .
```

门禁检查公开 origin、禁止路径、符号链接、敏感内容模式和不可发布文件类型。任何未知或无法读取的跟踪对象均 fail-closed。
