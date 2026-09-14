# 研究技能供应链

`vendor/sources.lock.json` 是公开供应链的固定来源清单。它只记录经审查的 URL、固定 commit/reference、许可证摘要、导入路径和用途；reference-only 对象不等于已安装、激活或验证器准入。

当前公开锁定来源包括：

- 可移植研究与数学 discovery/proof 方法来源；
- `teorth/erdosproblems` 与 `google-deepmind/formal-conjectures` 的固定 reference，用于候选/形式化生态调研；
- 只在许可证和 owner mapping 闭合后才会进入 `.codex/skills/` 的上游材料。

公开仓不携带工作树、运行日志、研究报告、私密供应链清单、原始网页或模型资产。移动分支、未固定 Git archive、未知许可证和 TLS 验证失败都保持 discovery-only 或进入失败账本。

运行：

```bash
python3 scripts/sync_supply_chain.py --check
# 只有在明确需要重建本地固定缓存时：
python3 scripts/sync_supply_chain.py
```

同步命令必须有 timeout、无绕过 TLS 的网络验证、固定 commit 和根许可证摘要。失败时非零退出；不得用旧缓存或空目录伪造同步成功。
