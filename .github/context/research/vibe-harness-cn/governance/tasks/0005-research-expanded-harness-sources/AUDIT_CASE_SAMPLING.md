# Audit Case Sampling Decision

- Source: governance/tasks/0005-research-expanded-harness-sources
- Fixed Problem: 自审未发现需要修复的产品或文档缺陷；审查观察集中于两处证据分级纪律
  （sandbox 能力存在性不得推断、相邻仓库能力不得计入当前 checkout），已在研究报告
  与领域文档中以显式规则处理。
- Decision: no-case
- Case ID: -
- Case Path: -
- Root Cause Class: research-evidence-grading-discipline
- Trigger Signals: sandbox capability, 默认安全, agent core, 相邻仓库能力, 证据分级
- Evidence: governance/tasks/0005-research-expanded-harness-sources/REVIEW.md；
  research/HARNESS_RESEARCH.md；docs/HARNESS_MODEL.md。
- No-Case Reason: 本轮是文档与静态研究任务，两个观察点均由现有审查 lens（agent-harness-runtime、
  knowledge-assets-zone）与研究报告内的证据契约显式覆盖，属于一次性的项目内研究纪律执行，
  尚无第二个独立实例证明需要新增全局审计案例；若后续研究批次再次出现把“未验证”写为
  “不支持”或把相邻仓库能力计入 checkout 的情况，再按复发信号晋升案例。

## Decision Values

- `case-created`
- `case-updated`
- `project-overlay`
- `promoted-to-gate`
- `no-case`

## Rule

每次问题修复后都必须填写采样判定。`no-case` 不是跳过；它必须给出明确理由。
