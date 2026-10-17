# Review: 宽松 Operator Core 与 Reference Profile

## Scope

- `target`: merge_gate
- `review_depth`: deep
- `base`: `fac646954a5d5efbf9ab49602207e06f7b79c757`
- `subject`: base 到当前完整 working-tree diff
- `review mode`: 主 Codex 自审；只证明本地确定性检查，不冒充外部独立 reviewer provenance

## Verdict

- `decision`: PASS
- `summary`: Core 只保留可交换字段、类型判别、显式扩展和安全 owner；本仓库 75+7 完整度由
  显式 `vibe-harness-cn/reference-library-v1` Profile 加严。未发现剩余产品级 BLOCK/WARN。

## Findings

- 已修复：PSOA PRD 仍有参数、失败恢复、预算和分类“所有 Operator 必须写满”的旧措辞；已改为
  Core 提供表达能力、执行型 Profile 或 Binding 按场景要求。
- 已补强：Reference validator 原本可在 catalog 未声明 Profile 时继续按本地规则运行；现在要求
  显式 Profile 标识，并有错误 Profile 负例。
- 未发现剩余产品级 BLOCK/WARN。

## Contract And Behavior

- Core 正例覆盖自定义领域、最小 metadata、空 `semantics`、显式扩展和空 Pack。
- Core 仍拒绝错误类型、未知稳定字段和 kind/semantics 类型混用；`source` 条目仍要求可追踪
  `source_key`。
- Reference Profile 继续要求完整内容、75/75 source、7/7 derived、计数、唯一 ID、引用类型、
  Method 无环、路径包含关系和治理 owner。
- 省略治理字段不产生授权；权限和 outcome 始终由 Harness policy 与 Verifier 裁决。

## Architecture And Simplicity

- 采用 `Core -> Profile -> Evaluation -> Runtime Policy` 单向分层；没有新增 selector、planner、
  Binding、服务、数据库、UI 或第二套 CLI。
- 复用 Draft 2020-12、`jsonschema==4.25.1`、现有 uv lock 与统一验证入口。
- 新增对象仅为规范、最小正例、Profile 标识与薄校验分支，均有直接消费方；未引入预想式扩展点。

## Performance

- Core 单 Pack 校验为 `O(E)`；Reference Profile 为 `O(F + E + R)`，空间为 `O(E + R)`。
- 该路径只读本地 JSON，不在 Agent 执行热路径。当前 7 个 Pack、82 个条目无缓存、数据库、并发
  或模型成本；在 10x/100x 数据证明 Schema 编译为瓶颈前暂不优化。

## Document Drift

- 已同步 README、根及模块 AGENTS、HARNESS_MODEL、PSOA PRD、Operator Spec、ADR-0004、QA-0003、
  项目操作模型、拓扑、上下文路由、工具链和 contracts/operators/docs/scripts module context。
- `DOCUMENT_DRIVEN_DEVELOPMENT.md` 未修改：开发流程未变，只增加了该流程管理的契约对象与命令。
- Harness manifest、75+7 条目内容、上游 registry/lock 与同步脚本未修改。

## Audit Cases

- `CASE-0003` 已消费：TODO、STATUS、验收清单将在 closeout 与真实命令证据对齐；复盘 handoff
  未完成时不得写 Done。
- `CASE-0013`、`CASE-0014` 是由文档中的 migration/domain 词汇误命中。本任务没有远端 Git 写入、
  force push、Cloudflare、DNS、Pages 或部署动作，相关审计问题不适用。
- database、reverse-engineering、layout-migration 路由同为关键词误报；本任务没有数据库、二进制样本
  或路径迁移。

## Evidence And Unknowns

- `validate_harness.py --operator-pack`: PASS。
- `validate_harness.py --operator-library`: PASS，`75/75 + 7/7 = 82`。
- `validate_harness.py --self-test`: PASS，宽松正例和格式/Profile/安全负例均符合预期。
- architecture、behavior、contract、test gates: PASS。
- governance strict/health、principle scan、`git diff --check`: PASS。
- 当前只证明结构互操作，不证明方法有效、运行安全或双 Harness Binding 兼容；这些仍是后续 eval。
- 无远端 CI、PR 或外部 reviewer provenance；高风险复盘需外部受信 reviewer，不能由实现者自签。

## Rollback

- 通过反向提交撤销本任务，不使用 reset、checkout 或 clean。
- 本轮没有部署、持久数据迁移或业务运行状态；回滚只恢复 Schema/validator/catalog 与文档分层。
