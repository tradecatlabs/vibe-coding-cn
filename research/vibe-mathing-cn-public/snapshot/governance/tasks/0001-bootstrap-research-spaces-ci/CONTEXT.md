# Repo Evidence

- 任务开始时项目不是 Git 仓库；目标 GitHub 仓库为空、公开、当前 `tradecatlabs` 身份具有 ADMIN 权限。
- 已有 6012 条本地来源记录、1 本本地电子书目录、6 个 active math skills。
- `vendor/upstream/` 约 231 MiB、电子书约 1 GiB、问题库 raw 约 22 MiB，均不适合普通公开 Git/CI。
- Lean/elan/lake 尚未安装，形式化验证保持 fail-closed。

# Constraints Matrix

- 必须：三个核心对象、可派生解库、负例门禁、公开仓库卫生、CI、本地完整验证、非破坏性 Git。
- 禁止：问题直接映射答案、有限证据冒充证明、自评冒充独立验证、上传 PDF/凭据/未授权内容、强推覆盖远端。
- 允许：空真相源、JSON Schema、Python 跨引用校验、GitHub Actions 只读权限。

# Change Boundary

- 新增 `research/`、`result-library/`、`governance/`、`.github/workflows/`、Makefile、requirements 和验证脚本。
- 同步根及受影响目录 README/AGENTS/CHANGELOG/.gitignore。
- 不修改现有 6012 条本地来源事实、电子书内容或 active skill 行为。

# Risk Matrix

| 风险 | 控制 |
|---|---|
| 有限证据进入解库 | 非 closing kind + 派生索引 + 负例测试 |
| 自评或形式化失真 | independent + statement_faithfulness Gate |
| CI 依赖 ignored 数据 | portable/full 两级命令，在模拟公开克隆中复验 |
| 公开仓库泄漏内容/路径/秘密 | .gitignore、staged 文件审计、secret/path/large-file scan |
| CI action 供应链漂移 | 官方 action 固定不可变 commit，最小权限和超时 |
| 治理模板冒充真相 | 清除占位符，strict/health 必须 PASS |

# Assumptions and Falsification

- 假设 JSON/JSONL 足以承载第一阶段规模；若真实跨记录查询/并发写成为瓶颈，再评估 SQLite。
- 假设完整解只需 proof/counterexample 两种顶层 kind；若垂直样例证明语义不足，再通过 ADR 变更。
- Falsifier：有限数值、自我审查或不忠实形式化能够进入 `solutions.json`，或干净公开克隆无法运行 `make check`。

# Critical Ambiguities

无阻塞歧义。远端为空且用户明确要求直接推送；采用 `main` 作为首个默认分支。

# Debug Evidence Contract

本任务出现统一门禁 RED：治理文档固定章节/状态枚举不兼容。根因、最小修复和同源 GREEN 已记录在根 `DEBUG.md`；产品逻辑没有用降级测试绕过。

# Task Package Context Map

- TP-01：ADR-0000、三个 Schema、GATE-0002。
- TP-02：局部 README/AGENTS、PROJECT_OPERATING_MODEL、module contexts。
- TP-03：Makefile、scripts/check.sh、portable validators、CI workflow。
- TP-04：.gitignore、公开文件清单、Git/GitHub/Actions 证据。

# Target End State

公开仓库可从零克隆并运行 `make check`；本地完整材料运行 `make check-full`；解库始终由 Result 机械派生。

# Ceiling and Upgrade Path

第一阶段保持文件系统和线性校验。只有记录达到 10x/100x、需要复杂关系查询或多写者并发时，才以 benchmark/query 证据评估 SQLite；不直接跳到分布式数据库或知识图谱。
