---
id: ADR-0002
type: record
status: active
owner: engineering
created: 2026-08-15
last_reviewed: 2026-08-15
source: docs/HARNESS_MODEL.md
related_gates: [GATE-0000, GATE-0001]
---

# ADR-0002 项目重命名为 Vibe Harness CN

## 背景

项目原标识为 `harness-harness`（产品名 "Harness Harness"），仓库目录已迁移为
`vibe-harness-cn`。为使机器标识、契约域名与人类可读产品名保持一致，需要把项目内全部
`harness-harness` 引用迁移到 `vibe-harness-cn`，并同步迁移 auto-assets 全局资产中的
项目 pack 与注册索引。

## 决策或结论

- 机器标识统一为 `vibe-harness-cn`：Schema `$id`、manifest `api_version`、全局
  `state://projects/...` 路径、exemplar `project` 字段。
- 契约域名从 `harness-harness.dev/v1alpha1` 迁移到 `vibe-harness-cn.dev/v1alpha1`。
  这是破坏性契约变更，但项目处于 `v1alpha1` 且无外部消费者，因此直接切换、不双轨兼容。
- 人类可读产品名统一为 "Vibe Harness CN"；"元 Harness"、"Meta Harness" 等概念名保留。
- 历史任务目录 slug（如 `0001-bootstrap-meta-harness`）与上游 Harness 名称不改，
  避免破坏任务索引与 revision lock 的既有事实。

## 证据

- Proof point：改名后 `uv run --locked --script scripts/validate_harness.py --self-test`
  正反例全通过；仓库内不再存在 `harness-harness` 残留引用。
- Falsifier：任何遗漏的旧域名或旧产品名引用会使 `rg` 扫描或 conformance 测试失败。
- 当前证据：契约、README/AGENTS、PROJECT_OPERATING_MODEL、0001 资产交接文件与全局
  auto-assets pack/索引均已迁移；governance strict/health 与任务文档校验 PASS。

## 影响范围

- `contracts/harness-manifest.schema.json`、`contracts/examples/`、`tests/fixtures/`：
  `api_version` 与 `$id` 同步迁移。
- 文档与治理资产：README、AGENTS、PROJECT_OPERATING_MODEL、0001 REUSE_ASSET_HANDOFF /
  exemplar。历史任务 DEBUG.md 保留创建时的旧产品名作为当时环境事实，不属于本次迁移范围。
- 全局资产（仓库外）：`skills/auto-assets/state/projects/vibe-harness-cn/` pack、
  `completion-exemplar-index.json` 与搜索索引重建。
- 回滚路径：恢复改名前的 commit，并把全局 pack 与索引反向迁移；契约 `v1alpha1`
  阶段无数据迁移或在线服务副作用。

## 后续动作

- [ ] 接入第一个真实 runtime adapter 时确认 manifest 消费方只接受新域名。
- [ ] 全局资产迁移后运行一次 auto-assets 检索抽查，确认 exemplar 可被搜索命中。
