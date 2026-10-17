# Task Overview
- Task ID: `0008`
- Slug: `build-complete-problem-solving-operator-library`
- Objective: `把用户给出的全部跨领域思维模型和方法论制作成可机检的问题求解算子库`
- Status: `Blocked`

## In Scope
- 建立 `operators/` 模块、机器目录、来源清单和七个领域 pack。
- 把用户明确列出的 75 项逐项建模，并增加 7 个不参与原始覆盖计数的领域组合 Method。
- 定义并验证 MentalModelSpec、OperatorSpec、MethodSpec 结构。
- 实现离线校验、正反例测试，并接入项目验证入口。
- 同步目录说明、PRD、领域模型、ADR、项目操作模型、拓扑、工具链和治理上下文。

## Out of Scope
- 不实现 selector、planner、在线 registry、数据库、UI 或 marketplace。
- 不实现具体 Harness Binding，不执行模型或上游 Harness 代码。
- 不声称完整兼容外部规划、工作流、验证或 provenance 标准。
- 不以 7 个派生 Method 掩盖任何原始条目缺失。

## Task Package Tree
```text
TP-01 冻结原始清单和机器契约
  -> TP-02 制作七个领域 pack
      -> TP-03 实现校验器和关键负例
          -> TP-04 同步项目文档与治理真相源
              -> TP-05 自审、验证与本地交付
```

## Requirement Alignment
- 原始清单精确计数：科研 3、计算机科学 10、数学 12、软件工程 12、编程 12、机器学习 12、深度学习 14，共 75 项。
- Library 另外包含每个领域一个组合 Method，共 7 项；最终总条目为 82，但原始覆盖仍单独验收为 75/75。
- 外部标准保留为 reference framework/provenance，不冒充 Operator 或已实现兼容。
- 算子库属于 Harness；本仓库只交付共享内容与 conformance，不拥有业务运行状态。

## Task Package Overview
| ID | 目标 | 输出 | Depends On |
|---|---|---|---|
| TP-01 | 固定完整性基线和结构契约 | source inventory、catalog、Schema | - |
| TP-02 | 制作全部内容 | 七个 pack、75 个原始条目、7 个派生 Method | TP-01 |
| TP-03 | 让完整性可以机械证明 | validator、fixtures、tests、project gates | TP-02 |
| TP-04 | 同步长期项目真相 | README/AGENTS、docs、ADR、governance context | TP-03 |
| TP-05 | 深度自审并交付 | REVIEW、采样、closeout、Git/verification evidence | TP-04 |

## Reading Order
1. README.md
2. CONTEXT.md
3. PLAN.md
4. ACCEPTANCE.md
5. ACCEPTANCE_CHECKLIST.md
6. TODO.md
7. STATUS.md

## Closeout Blocker
- 产品实现、文档、自审和本地门禁已完成。
- `auto-retro` 全局 registry 中既有 Tradecat 记录的来源摘要已与当前 artifact 漂移，导致 owner preflight 在写入本任务复盘前失败；未生成或伪造 `RETROSPECTIVE_HANDOFF.json`。
