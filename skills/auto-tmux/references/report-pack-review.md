# auto-tmux Report Pack Review

本文件给 reviewer 一条最短验收路径：先跑统一门禁，再看结论文件，最后只在必要时追溯附件。

## 最短验收命令

```bash
skills/auto-tmux/scripts/verify-report-pack.sh --pack /tmp/ai-swarm-report-pack
```

该命令会检查：

- `review-checklist.sh --strict`：报告包必需文件是否齐全。
- `manifest.json`：根级 manifest 类型是否正确。
- `results.jsonl`：结果记录是否具备 `type`、`id`、`status` 字段。

## 推荐阅读顺序

1. `index.md`：确认报告包创建时间、状态目录和文件清单。
2. `review-checklist.md`：按固定审计项判断能否交接。
3. `results.md`：查看 DONE/FAIL/BLOCKED 结果。
4. `blockers.md`：确认阻塞项是否需要人工处理。
5. `board.md`：查看全量任务状态。
6. `timeline.md`：追溯最近状态变化。
7. `attachments.md`：仅在需要外部证据时查看。

## 通过标准

- 必需文件齐全，`verify-report-pack.sh` 通过。
- `results.md` 能说明 worker 交付结果。
- `blockers.md` 没有阻止交接的未处理 FAIL/BLOCKED。
- `manifest.json` 与 `results.jsonl` 可被机器门禁读取。
- 附件目录没有密钥、Token、密码或无关私密输出。

## 不通过标准

- 缺失 `manifest.json`、`results.jsonl`、`review-checklist.md` 或 `export/manifest.json`。
- `results.md` 只有状态，没有可判断的 result。
- `blockers.md` 存在未解释的 FAIL/BLOCKED。
- 附件中包含未脱敏的敏感信息。
- 结论必须依赖报告包外的口头说明才能成立。
