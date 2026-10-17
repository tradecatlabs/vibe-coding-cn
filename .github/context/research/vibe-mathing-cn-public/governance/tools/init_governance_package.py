#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import shutil
from datetime import date
from pathlib import Path


GOV_ROOT = Path("governance")
TOOL_NAMES = [
    "init_governance_package.py",
    "new_governance_record.py",
    "validate_governance_package.py",
    "rebuild_governance_index.py",
    "new_module_context.py",
    "governance_health_report.py",
    "governance_context_bundle.py",
    "scan_principle_gates.py",
]


def fm(doc_id: str, doc_type: str, status: str = "current") -> str:
    today = date.today().isoformat()
    return (
        "---\n"
        f"id: {doc_id}\n"
        f"type: {doc_type}\n"
        f"status: {status}\n"
        "owner: engineering\n"
        f"created: {today}\n"
        f"last_reviewed: {today}\n"
        "review_cycle: P90D\n"
        "---\n\n"
    )


def doc(doc_id: str, doc_type: str, title: str, body: str, status: str = "current") -> str:
    return fm(doc_id, doc_type, status) + f"# {title}\n\n{body.strip()}\n"


def gate_doc(
    doc_id: str,
    title: str,
    body: str,
    severity: str = "BLOCK",
    detectability: str = "agent+manual",
    source: str = "STD-PONYTAIL-LADDER",
) -> str:
    today = date.today().isoformat()
    return (
        "---\n"
        f"id: {doc_id}\n"
        "type: gate\n"
        "status: active\n"
        "owner: engineering\n"
        f"created: {today}\n"
        f"last_reviewed: {today}\n"
        "review_cycle: P90D\n"
        f"severity: {severity}\n"
        f"detectability: {detectability}\n"
        f"source: {source}\n"
        "---\n\n"
        f"# {title}\n\n{body.strip()}\n"
    )


def index_doc(title: str, rows: list[tuple[str, str]]) -> str:
    safe_id = "IDX-" + re.sub(r"[^A-Z0-9]+", "-", title.upper()).strip("-")
    lines = [
        f"# {title}",
        "",
        "| 名称 | 说明 |",
        "|---|---|",
    ]
    for name, desc in rows:
        lines.append(f"| `{name}` | {desc} |")
    return fm(safe_id, "index") + "\n".join(lines) + "\n"


def record_index_doc(title: str) -> str:
    safe_id = "IDX-" + re.sub(r"[^A-Z0-9]+", "-", title.upper()).strip("-")
    lines = [
        f"# {title}",
        "",
        "| ID | 标题 | 状态 | 文件 |",
        "|---|---|---|---|",
    ]
    return fm(safe_id, "index") + "\n".join(lines) + "\n"


def default_gate_rules_index_doc() -> str:
    lines = [
        "# GATE Index",
        "",
        "| ID | 标题 | 状态 | 文件 |",
        "|---|---|---|---|",
        "| `GATE-0000` | 新增所有权面必须证明存在必要性 | active | `GATE-0000-PONYTAIL-OWNERSHIP-SURFACE.md` |",
        "| `GATE-0001` | 非平凡方案不得主动降级成短期补丁 | active | `GATE-0001-FUTURE-OPTIMAL-NO-DOWNGRADE.md` |",
    ]
    return fm("IDX-GATE-INDEX", "index") + "\n".join(lines) + "\n"


def gate_index_doc() -> str:
    return doc(
        "GATE-INDEX",
        "gate-index",
        "Gate Index",
        """
| Gate ID | 严重级别 | 标题 | 检测方式 | 来源 | 状态 | 文件 |
|---|---|---|---|---|---|---|
| `GATE-0000` | BLOCK | 新增所有权面必须证明存在必要性 | agent+script+manual | STD-PONYTAIL-LADDER | active | `rules/GATE-0000-PONYTAIL-OWNERSHIP-SURFACE.md` |
| `GATE-0001` | BLOCK | 非平凡方案不得主动降级成短期补丁 | agent+script+manual | STD-FUTURE-OPTIMAL | active | `rules/GATE-0001-FUTURE-OPTIMAL-NO-DOWNGRADE.md` |
        """,
    )


def project_operating_model_doc() -> str:
    return doc(
        "GOV-PROJECT-OPERATING-MODEL",
        "context",
        "Project Operating Model",
        """
本文件是项目级人类入口和代理入口的共享操作模型。它只记录项目当前应该如何被理解、修改、验证和交付；不替代代码、契约、ADR、任务包、README 或 AGENTS。

## 项目一句话定义

待补充：用一句话说明项目服务的对象、核心价值和运行边界。

## 业务模型

- 核心用户：
- 核心对象：
- 关键流程：
- 不属于本项目的范围：

## 技术模型

- 主要运行形态：
- 核心模块：
- 数据事实源：
- 外部依赖：
- 主要验证入口：

## 工具链模型

工具链边界以 `context/TOOLCHAIN_MODEL.md` 为准。这里仅记录最短摘要：

- 构建：
- 测试：
- 类型检查：
- 格式 / lint：
- 发布 / 回滚：

## 目录和真相源地图

| 事实类型 | 真相源 | 备注 |
|---|---|---|
| 项目操作模型 | `governance/context/PROJECT_OPERATING_MODEL.md` | 人类和代理的项目入口 |
| 上下文路由 | `governance/context/CONTEXT-ROUTER.md` | 任务类型到最小上下文包 |
| 工程流程 | `governance/processes/DOCUMENT_DRIVEN_DEVELOPMENT.md` | 文档先行和文档回填规则 |
| 工具链边界 | `governance/context/TOOLCHAIN_MODEL.md` | 成熟工具、项目脚本和禁用做法 |
| 机器契约 | `governance/context/project_operating_model_contract.v1.yaml` | 脚本和 agent 可读取的契约 |
| 架构决策 | `governance/decisions/adr/` | 不可逆或高影响决策 |
| 任务证据 | `governance/tasks/` | 执行计划、状态、验收、closeout |

## 变更入口

非平凡工程变更开始前必须判断：

- 是否需要先更新本操作模型。
- 是否需要更新文档驱动开发流程。
- 是否需要更新工具链模型。
- 是否需要新增或更新 ADR、Gate、module context、contracts、catalog、README 或 AGENTS。

## 验证入口

```bash
python3 governance/tools/governance_context_bundle.py --project-root . --task-type docs
python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict
```

## 最近一次 review

- 日期：待补充
- 结论：待补充
- 后续动作：待补充
        """,
    )


def document_driven_development_doc() -> str:
    return doc(
        "PROC-DOCUMENT-DRIVEN-DEVELOPMENT",
        "process",
        "Document Driven Development",
        """
文档驱动开发不是多写文档，而是让项目的关键事实先有稳定真相源，再让代码、任务、审查和交付围绕这些真相源闭环。

## 适用范围

默认适用于：

- 新增功能、接口、数据模型、配置、依赖、任务流程或运行模式。
- 修改既有业务逻辑、模块边界、公共契约、工具链或发布方式。
- 产生长期影响的 bug 修复、复盘、审查反馈或架构决策。

## 执行顺序

1. 读取 `context/PROJECT_OPERATING_MODEL.md`。
2. 使用 `context/CONTEXT-ROUTER.md` 选择最小上下文。
3. 判断本次变更影响哪些真相源。
4. 若变更会改变项目理解、模块边界、流程、契约或工具链，先更新对应文档或在任务包中记录明确豁免理由。
5. 实现代码、运行验证、记录证据。
6. closeout 前执行文档同步检查，确认所有受影响真相源已更新或明确无需更新。

## 文档影响分类

| 影响类型 | 默认落点 | 说明 |
|---|---|---|
| 项目整体理解变化 | `context/PROJECT_OPERATING_MODEL.md` | 项目定位、边界、核心流程、事实源变化 |
| 执行流程变化 | `processes/DOCUMENT_DRIVEN_DEVELOPMENT.md` | 开发、验证、交付、回填流程变化 |
| 工具链变化 | `context/TOOLCHAIN_MODEL.md` | 构建、测试、发布、脚本、成熟工具边界变化 |
| 架构决策 | `decisions/adr/` | 有 trade-off、难反转、未来会惊讶的决策 |
| 质量护栏 | `architecture-gates/rules/` | 可复发、可检测、必须阻止的问题 |
| 任务执行证据 | `tasks/` | 计划、状态、验收、验证、closeout |
| 模块事实 | `context/module-contexts/` 或项目局部 README/AGENTS | 模块职责、边界、上下游、验证入口 |

## Closeout 必填判断

每个非平凡任务 closeout 必须回答：

- 本次是否改变项目操作模型。
- 本次是否改变工具链模型。
- 本次是否改变文档驱动开发流程。
- 本次是否改变模块上下文、ADR、Gate、contract、catalog、README 或 AGENTS。
- 若没有更新文档，原因是什么。

## 不接受的做法

- 代码已经改变系统事实，但文档仍描述旧事实。
- 只在聊天记录里说明变更，不落到项目可迁移资产。
- 把任务包临时结论当成长期真相源。
- 用泛泛的“无需更新文档”绕过 closeout 证据。
        """,
    )


def toolchain_model_doc() -> str:
    return doc(
        "GOV-TOOLCHAIN-MODEL",
        "context",
        "Toolchain Model",
        """
本文件记录项目工具链的当前真相，帮助人类和代理优先复用成熟能力、项目既有脚本和稳定验证入口。

## 成熟工具优先

- 优先使用语言标准工具、官方 CLI、包管理器、测试框架、lint/typecheck、数据库迁移工具和云平台能力。
- 自研脚本只用于连接、编排、适配和表达项目特有流程。
- 新增工具前必须证明：已有工具无法满足、引入后总拥有成本更低、验证和回滚路径明确。

## 项目命令

| 场景 | 命令 | 备注 |
|---|---|---|
| 安装依赖 | 待补充 |  |
| 测试 | 待补充 |  |
| 类型检查 | 待补充 |  |
| lint / format | 待补充 |  |
| 构建 | 待补充 |  |
| 本地运行 | 待补充 |  |
| 发布 | 待补充 |  |
| 回滚 | 待补充 |  |

## 禁止或谨慎使用

- 禁止绕过项目已有脚本直接调用内部实现细节，除非在调试任务中明确说明。
- 禁止新增无 owner、无验证、无回滚说明的脚本。
- 禁止把一次性命令伪装成长期工具链。

## 工具链变更流程

1. 先检查现有命令、脚本、CI 和文档。
2. 记录新增或替换工具的存在性理由。
3. 更新本文件和相关流程文档。
4. 运行最小验证。
5. 在任务 closeout 中记录验证证据和回滚方式。
        """,
    )


def project_operating_model_contract_doc() -> str:
    today = date.today().isoformat()
    return f"""version: 1
id: project_operating_model_contract.v1
status: current
owner: engineering
created: {today}
last_reviewed: {today}
required_documents:
  - path: governance/context/PROJECT_OPERATING_MODEL.md
    owner: auto-governance
    purpose: human_and_agent_project_entry
  - path: governance/processes/DOCUMENT_DRIVEN_DEVELOPMENT.md
    owner: auto-governance
    purpose: docs_first_change_workflow
  - path: governance/context/TOOLCHAIN_MODEL.md
    owner: auto-governance
    purpose: tool_boundary_and_validation_entry
  - path: governance/context/CONTEXT-ROUTER.md
    owner: auto-governance
    purpose: task_type_to_minimal_context
closeout_required_fields:
  - operating_model_update
  - toolchain_model_update
  - process_update
  - source_of_truth_updates
  - documentation_exemption_reason
validation:
  governance_validate: python3 governance/tools/validate_governance_package.py --project-root . --strict
  context_bundle_docs: python3 governance/tools/governance_context_bundle.py --project-root . --task-type docs
"""


def minimal_files() -> dict[str, str]:
    return {
        "README.md": doc(
            "GOV-README",
            "index",
            "工程治理包",
            """
本目录是项目级工程治理包，固定落点为 `governance/`。

它只新增独立治理资产，不改写、不覆盖、不迁移项目原有 `README.md`、`AGENTS.md`、`CLAUDE.md`、模块文档、CI 配置或脚本。

使用入口：

1. 先读 `INDEX.md`。
2. 再读 `context/AGENT-ENTRY.md`。
3. 按 `context/CONTEXT-ROUTER.md` 选择最小上下文。
4. 需要模块事实时，通过 `context/CONTEXT-MAP.md` 找到对应 module context。
            """,
        ),
        "INDEX.md": doc(
            "GOV-INDEX",
            "index",
            "治理包索引",
            """
## 启动入口

- `context/AGENT-ENTRY.md`：代理启动协议。
- `context/PROJECT_OPERATING_MODEL.md`：项目操作模型，作为人类和代理的默认项目入口。
- `context/CONTEXT-MAP.md`：项目上下文地图。
- `context/CONTEXT-ROUTER.md`：任务类型到上下文包的路由。
- `context/PROJECT-TOPOLOGY.md`：项目结构和边界说明。
- `context/TOOLCHAIN_MODEL.md`：工具链边界和验证入口。
- `context/project_operating_model_contract.v1.yaml`：机器可读操作模型契约。

## 当前标准

- `standards/工程质量标准.md`
- `standards/未来最优解原则.md`
- `standards/Ponytail工程阶梯标准.md`
- `standards/劣质代码定义.md`
- `standards/非功能性需求标准.md`

## 流程

- `processes/DOCUMENT_DRIVEN_DEVELOPMENT.md`
- `processes/代理协作协议.md`
- `processes/RPI研究计划实施流程.md`
- `processes/QA计划标准.md`
- `processes/本地工具与验证入口.md`

## 门禁

- `architecture-gates/门禁与护栏.md`
- `architecture-gates/GATE-INDEX.md`
            """,
        ),
        "CHANGELOG.md": doc(
            "GOV-CHANGELOG",
            "changelog",
            "治理包变更记录",
            "- 初始化治理包。\n",
        ),
        "context/AGENT-ENTRY.md": doc(
            "GOV-AGENT-ENTRY",
            "process",
            "Agent Entry",
            """
## 项目工作协议

1. 不要在没有验证证据的情况下声明“已完成”或“已测试”。
2. 开始任务前先读取 `governance/INDEX.md`。
3. 根据 `governance/context/CONTEXT-ROUTER.md` 选择最小上下文。
4. 涉及架构边界时必须读取相关 ADR。
5. 涉及用户功能时必须产出 QA 计划或验证证据。
6. 高风险变更必须说明回滚路径。
7. 如果发现重复错误或标准缺失，记录到 `agent-governance/agent-feedback/`。
            """,
        ),
        "context/CONTEXT-MAP.md": doc(
            "GOV-CONTEXT-MAP",
            "index",
            "Context Map",
            """
## 领域上下文

| 领域 | 代码目录 | 上下文文件 | 相关 ADR | 常用验证 |
|---|---|---|---|---|
| 项目根 | `.` | `context/PROJECT-TOPOLOGY.md` | `decisions/adr/INDEX.md` | governance strict validate |
| 治理包 | `governance/` | `context/AGENT-ENTRY.md` | `decisions/adr/INDEX.md` | governance health report |
| 任务容器 | `governance/tasks/` | `tasks/INDEX.md` | `decisions/adr/INDEX.md` | task tree validation |

## 维护规则

- 不把模块上下文散落到代码目录。
- 模块上下文统一放在 `context/module-contexts/`。
- 原有模块 README 只被引用，不被治理包覆盖。
- 新增稳定模块后，再创建 `context/module-contexts/<module>/CONTEXT.md` 并更新本表。
            """,
        ),
        "context/CONTEXT-ROUTER.md": doc(
            "GOV-CONTEXT-ROUTER",
            "process",
            "Context Router",
            """
## 默认入口

所有任务先读：

1. `governance/INDEX.md`
2. `governance/context/PROJECT_OPERATING_MODEL.md`
3. `governance/context/PROJECT-TOPOLOGY.md`
4. `governance/context/CONTEXT-MAP.md`

## 任务类型路由

| 任务类型 | 必读文档 | 可选文档 | 必须产出 |
|---|---|---|---|
| 新功能 | 工程质量标准、未来最优解原则、Ponytail工程阶梯标准、非功能性需求标准、QA计划标准、代理协作协议 | 相关 ADR、术语表 | QA 计划或验证证据 |
| Bug 修复 | 劣质代码定义、本地工具与验证入口 | postmortems、lessons | 复现步骤、回归测试 |
| 性能优化 | 性能效率优化标准、门禁与护栏 | 历史性能复盘 | benchmark/profile 证据 |
| 架构变更 | 架构设计原则、ADR 索引、非功能性需求标准 | tech-debt | ADR 或 ADR 更新 |
| Review | auto-review module context、门禁与护栏 | lessons、agent-feedback | PASS/WARN/BLOCK finding |
| 复盘 | 文档治理规则、门禁与护栏 | postmortems/INDEX.md | 防复发动作 |
| 文档治理 | PROJECT_OPERATING_MODEL、DOCUMENT_DRIVEN_DEVELOPMENT、TOOLCHAIN_MODEL、CONTEXT-ROUTER | ADR、module context、任务 closeout | 文档同步证据或豁免理由 |
            """,
        ),
        "context/PROJECT_OPERATING_MODEL.md": project_operating_model_doc(),
        "context/TOOLCHAIN_MODEL.md": toolchain_model_doc(),
        "context/project_operating_model_contract.v1.yaml": project_operating_model_contract_doc(),
        "context/PROJECT-TOPOLOGY.md": doc(
            "GOV-PROJECT-TOPOLOGY",
            "index",
            "Project Topology",
            """
## 项目结构

| 路径 | 职责 | 禁止事项 | 主要验证 |
|---|---|---|---|
| `governance/` | 项目工程治理包、上下文路由、标准、门禁和证据记录 | 不覆盖项目原有 README、AGENTS、CI 或模块文档 | `validate_governance_package.py --strict` |
| `governance/tasks/` | 任务树、任务包和执行状态 | 不把任务临时状态直接当成长期标准 | `validate_tasks_tree.py` |
| 源代码目录 | 项目业务实现与测试 | 不绕过既有模块边界和公共接口 | 使用项目实际 test/lint/typecheck 命令 |

## 依赖方向

治理包只提供项目记忆和执行护栏；源代码目录保持业务实现职责；任务容器记录执行过程，长期有效经验再晋升到 standards、processes、architecture-gates 或 evidence。
            """,
        ),
        "standards/工程质量标准.md": doc(
            "STD-ENGINEERING-QUALITY",
            "standard",
            "工程质量标准",
            """
## 基本要求

- 正确性优先。
- 未来最优解优先：先按长期正确终态思考，再切成本轮可验证路径。
- 存在性优先：先证明对象应该存在，再实现。
- 行为可验证。
- 边界清晰。
- 依赖合理。
- 错误处理完整。
- 性能和成本可解释。

## 不合格信号

- 没有验证证据。
- 改动范围失控。
- 重复实现既有能力。
- 引入无法解释的复杂度。
- 因实现成本、迁移恐惧或旧结构惯性主动降级成短期补丁。
- 新增对象没有当前需求、验证路径、风险控制或维护收益证明。
            """,
        ),
        "standards/未来最优解原则.md": doc(
            "STD-FUTURE-OPTIMAL",
            "standard",
            "未来最优解原则",
            """
## 原则

非平凡方案、架构、重构、任务拆分和治理沉淀，必须先按最终状态最优、长期可维护、可扩展、可验证的目标结构思考，再评估迁移成本和本轮切片。

不得因为实现时间、代码量、迁移工作量、内部调用方成本或旧结构惯性，主动把方案降级成临时补丁、兼容壳、双轨流程或错误概念上的小修小补。

## 必填字段

- Target end state
- Real constraints
- Inertia constraints
- Kill list
- Proof point
- Falsifier
- Migration slice
- Rejected short-term patches

## 真实约束

只有公共 API、持久化数据、外部集成、用户承诺、合规、部署窗口、回滚窗口或用户明确要求，才允许降低目标终态。

## 惯性约束

旧命名、旧目录、内部调用方、局部实现形状、迁移恐惧和“改起来麻烦”不能作为目标降级理由，只能影响迁移顺序。
            """,
        ),
        "standards/Ponytail工程阶梯标准.md": doc(
            "STD-PONYTAIL-LADDER",
            "standard",
            "Ponytail 工程阶梯标准",
            """
## 原则

任何新增功能、抽象、文件、目录、依赖、配置、框架、接口、任务、文档、测试、脚本、skill、治理规则或自动化流程，必须先证明当前应该存在。

## 决策阶梯

1. 是否可以不做、删除、合并、内联或延后。
2. 是否已有标准库、系统工具、数据库能力、平台原生能力或框架原生能力。
3. 是否已有项目内模式、helper、脚本、skill、模板、治理资产或验证命令可复用。
4. 是否已有成熟依赖能在当前需求下真实降低总拥有成本。
5. 是否可以用一小段直接代码完成。
6. 只有前面都不成立，才允许新增长期所有权面。

## 不得简化掉

- 信任边界校验。
- 数据丢失防护。
- 错误处理。
- 安全、隐私、权限、审计和可访问性边界。
- 用户明确要求的可见行为。
- 非平凡逻辑的最小可运行检查。

## 输出要求

中高风险变更必须记录：存在性判断、命中的阶梯层级、跳过范围、天花板、升级路径和最小验证方式。
            """,
        ),
        "standards/劣质代码定义.md": doc(
            "STD-CODE-BAD",
            "standard",
            "劣质代码定义",
            """
不可接受模式：

- 临时补丁替代根因修复。
- 吞异常或假成功。
- 无测试的高风险改动。
- N+1、无界循环、无界并发、全量加载大数据。
- 无 timeout、无限重试、无背压。
- 硬编码业务规则。
- 绕过架构边界。
- 双真相源。
            """,
        ),
        "standards/非功能性需求标准.md": doc(
            "STD-NFR",
            "standard",
            "非功能性需求标准",
            """
默认检查：

- 性能
- 可靠性
- 安全
- 可观测性
- 可扩展性
- 兼容性
- 成本
- 可维护性
- 可测试性
            """,
        ),
        "processes/代理协作协议.md": doc(
            "PROC-AGENT-COLLAB",
            "process",
            "代理协作协议",
            """
代理执行任务时必须：

1. 读取治理包入口。
2. 按上下文路由加载最小文档。
3. 保留关键证据。
4. 不伪造验证结果。
5. 发现重复错误时写入 agent feedback。
6. 高风险变更说明回滚路径。
            """,
        ),
        "processes/DOCUMENT_DRIVEN_DEVELOPMENT.md": document_driven_development_doc(),
        "processes/RPI研究计划实施流程.md": doc(
            "PROC-RPI",
            "process",
            "RPI 研究-计划-实施流程",
            """
## Research

- 相关文件
- 当前事实
- 数据流/调用流
- 风险点
- 未确认问题

## Plan

- 修改文件列表
- 每个文件修改意图
- 测试策略
- 回滚策略
- 需要更新的治理资产

## Implement

- 严格执行计划。
- 不扩大范围。
- 偏离计划必须记录原因。
- 完成后输出验证证据。
            """,
        ),
        "processes/QA计划标准.md": doc(
            "PROC-QA-STANDARD",
            "process",
            "QA 计划标准",
            """
关键用户功能应包含：

- 功能清单
- 关键用户旅程
- 成功路径
- 失败路径
- 边界输入
- 验收证据
- PR 应附材料
            """,
        ),
        "processes/本地工具与验证入口.md": doc(
            "PROC-LOCAL-VERIFY",
            "process",
            "本地工具与验证入口",
            """
## 治理包校验

```bash
python3 governance/tools/validate_governance_package.py --project-root . --strict
python3 governance/tools/governance_health_report.py --project-root . --strict
```

## 任务树校验

```bash
python3 skills/auto-tasks/scripts/validate_tasks_tree.py --tasks-dir governance/tasks --phase auto --format markdown
```

## 项目自身验证

使用项目已有的 package manager、test、lint、typecheck、benchmark 或 CI 命令；治理包不发明项目不存在的验证入口。
            """,
        ),
        "architecture-gates/门禁与护栏.md": doc(
            "GATE-GUARDRAILS",
            "gate-index",
            "门禁与护栏",
            """
初版门禁：

- 不接受无验证证据的高风险代码。
- 不接受明显性能放大问题。
- 不接受吞异常、假成功、无 timeout、无限重试。
- 不接受因实现成本、兼容焦虑或旧结构惯性主动降级成不通向终态的短期补丁。
- 不接受绕过架构边界、双真相源、重复实现已有工具。
- 不接受新增无存在性理由的依赖、抽象、配置、文件、流程、skill 或治理规则。
- 不接受未说明回滚方式的高风险迁移。
- 不接受复发的历史错误未更新护栏。
            """,
        ),
        "architecture-gates/GATE-INDEX.md": gate_index_doc(),
        "architecture-gates/rules/INDEX.md": default_gate_rules_index_doc(),
        "architecture-gates/rules/GATE-0000-PONYTAIL-OWNERSHIP-SURFACE.md": gate_doc(
            "GATE-0000",
            "新增所有权面必须证明存在必要性",
            """
## 阻止条件

新增或扩展依赖、抽象、配置、文件、目录、流程、脚本、skill 或治理规则，但没有说明当前需求、最低工程阶梯、跳过范围、天花板、升级路径和最小验证方式。

## 原因

无证明的所有权面会增加维护、review、测试、迁移和长期理解成本，并让代理在后续任务中继续围绕错误结构扩张。

## 检查方式

- Script：`python3 governance/tools/scan_principle_gates.py --repo . --git-mode working --strict`。
- Agent review：使用 `auto-review` 的 `ponytail-complexity` profile。
- 人工审查：检查新增对象是否有当前消费者、owner、验证方式和删除/升级触发。

## 可操作错误提示

你新增了一个所有权对象，但没有证明它现在应该存在。请先尝试删除、合并、内联、使用标准/平台/项目原生能力，或补充存在性理由、最低阶梯选择、跳过范围、天花板和最小验证。

## 最小修复

- 删除或合并不必要对象；或
- 替换为标准库、平台原生、项目既有能力；或
- 补充当前存在性理由、owner、验证方式、天花板和升级触发条件。
            """,
            detectability="agent+script+manual",
        ),
        "architecture-gates/rules/GATE-0001-FUTURE-OPTIMAL-NO-DOWNGRADE.md": gate_doc(
            "GATE-0001",
            "非平凡方案不得主动降级成短期补丁",
            """
## 阻止条件

非平凡方案、架构、重构、任务拆分或治理规则没有说明 target end state、real constraints、inertia constraints、kill list、proof point、falsifier 和 migration slice，或者因实现成本、迁移恐惧、内部调用方成本、旧命名/旧目录惯性而主动降级成不通向终态的短期补丁。

## 原因

代码编写成本不是默认约束。真正昂贵的是错误概念、错误边界、缺失测试、缺失门禁、缺失迁移路径和长期质量债。

## 检查方式

- Script：`python3 governance/tools/scan_principle_gates.py --repo . --git-mode working --strict`。
- Agent review：使用 `auto-review` 的 `future-optimal-drift` profile。
- 人工审查：检查真实约束与惯性约束是否混写，短期切片是否通向目标终态。
- 治理审查：涉及架构或治理决策时，ADR 必须包含 target end state、rejected short-term patches 和 migration path。

## 可操作错误提示

你给出了能跑的短期方案，但没有证明它通向长期正确结构。请先写清目标终态、真实约束、惯性约束、kill list、proof point、falsifier 和本轮迁移切片；如果保留兼容层，请说明真实 contract、移除条件和后续任务。

## 最小修复

- 把短期补丁改成本轮可验证迁移切片；或
- 证明兼容层有真实外部 contract 并记录移除条件；或
- 明确 blocker，停止声明该目标已完成。
            """,
            source="STD-FUTURE-OPTIMAL",
            detectability="agent+script+manual",
        ),
        "decisions/adr/INDEX.md": record_index_doc("ADR Index"),
        "evidence/postmortems/INDEX.md": record_index_doc("Postmortem Index"),
        "evidence/lessons/INDEX.md": record_index_doc("Lesson Index"),
        "evidence/qa-plans/INDEX.md": record_index_doc("QA Plan Index"),
        "agent-governance/agent-feedback/INDEX.md": record_index_doc("Agent Feedback Index"),
        "templates/ADR.template.md": template("ADR"),
        "templates/GATE.template.md": template("GATE"),
        "templates/QA.template.md": template("QA"),
        "templates/AGENT-FEEDBACK.template.md": template("AF"),
        "tools/README.md": doc(
            "TOOLS-GOVERNANCE",
            "tooling",
            "Governance Tools",
            """
这里放治理包自身维护脚本或接入说明。默认不修改项目外部 CI、lint 或 hook。

默认内置工具：

- `init_governance_package.py`：初始化或补齐治理包。
- `new_governance_record.py`：新增 ADR/Gate/QA/Postmortem/Lesson/Agent Feedback 等编号记录。
- `new_module_context.py`：新增治理包内模块上下文，并更新 `CONTEXT-MAP.md`。
- `rebuild_governance_index.py`：重建根索引、记录索引、`architecture-gates/rules/INDEX.md` 和 `GATE-INDEX.md`。
- `validate_governance_package.py`：校验治理包结构、frontmatter 和 gate 必填项。
- `governance_health_report.py`：输出治理包健康度、占位内容、过期文档、open feedback 和下一步动作。
- `governance_context_bundle.py`：按任务类型输出 agent 本次应读取的治理文档、模块上下文和必须产出。

这些脚本只写入 `governance/` 内部；外部 CI、lint、hook 接入必须单独 opt-in。
            """,
        ),
        "tasks/README.md": doc(
            "TASKS-GOVERNANCE",
            "tasks",
            "Governance Tasks",
            "这里放项目任务包、任务树、执行波次、closeout 和任务级候选 lessons。长期有效规则应拆分后晋升到 `evidence/`、`architecture-gates/`、`processes/` 或 `standards/`。",
        ),
        "tasks/lessons.md": "# Task Lessons Candidate Pool\n\n本文件是任务级候选教训整理池，只记录尚未拆分、晋升或拒绝的原始经验材料。\n\n## 使用规则\n\n- 任务执行中发现的纠偏、失败复盘、可复用验收标准或防复发经验，可以先追加到这里。\n- 写入后必须拆成原子事实：事实、来源、影响、通用规则、建议目标位置。\n- 通用规则最终应晋升到 `governance/evidence/lessons/`、`governance/architecture-gates/rules/`、`governance/standards/`、`governance/processes/`、`governance/decisions/adr/` 或 `governance/context/module-contexts/`。\n- 已晋升或拒绝晋升的条目，应保留简短处理记录，避免同一教训长期堆积在候选池。\n\n## Candidate Lessons\n\n暂无候选教训。\n",
        "runtime/README.md": doc(
            "RUNTIME-GOVERNANCE",
            "runtime",
            "Runtime Records",
            "这里放代理运行记录和临时材料。任务包统一放在 `governance/tasks/`，长期价值内容应沉淀到 `evidence/`。",
        ),
        "archive/README.md": doc(
            "ARCHIVE-GOVERNANCE",
            "archive",
            "Archive",
            "这里归档失效、被替代或过期的治理资产。",
        ),
    }


def full_extra_files() -> dict[str, str]:
    return {
        "standards/优质代码定义.md": doc(
            "STD-CODE-GOOD",
            "standard",
            "优质代码定义",
            "优质代码必须正确、清晰、边界明确、可测试、可维护、性能可解释，并优先复用成熟能力。",
        ),
        "standards/性能效率优化标准.md": doc(
            "STD-PERFORMANCE",
            "standard",
            "性能效率优化标准",
            "默认检查复杂度、hot path、数据库/API/I/O、缓存、内存、并发、成本、benchmark/profile 和 p95/p99。",
        ),
        "standards/可靠性标准.md": doc(
            "STD-RELIABILITY",
            "standard",
            "可靠性标准",
            "默认检查 timeout、retry budget、熔断、降级、幂等、背压、资源池、队列容量、恢复路径和可观测性。",
        ),
        "standards/架构设计原则.md": doc(
            "STD-ARCHITECTURE",
            "standard",
            "架构设计原则",
            "默认检查模块边界、依赖方向、单一真相源、信息隐藏、深模块、禁止旁路和数据所有权。",
        ),
        "standards/工程变更安全标准.md": doc(
            "STD-CHANGE-SAFETY",
            "standard",
            "工程变更安全标准",
            "新增功能、API、数据、缓存、异步、第三方、权限、权益和副作用变更前，必须按风险等级检查影响面、数据流、控制流、状态变化、副作用、幂等并发、失败恢复、兼容性、观测、发布回滚和必要测试。",
        ),
        "standards/术语表.md": doc(
            "STD-GLOSSARY",
            "standard",
            "术语表",
            "记录项目领域词、模块名、缩写、状态名和关键概念。",
        ),
        "processes/代码评审标准.md": doc(
            "PROC-REVIEW",
            "process",
            "代码评审标准",
            "评审输出必须包含 PASS/WARN/BLOCK、证据、影响、最小修复和验证方式。",
        ),
        "processes/工程变更安全审查流程.md": doc(
            "PROC-CHANGE-SAFETY",
            "process",
            "工程变更安全审查流程",
            "中高风险工程变更按 `auto-thinking` 预检、`auto-tasks` 任务字段、`auto-review` feature-change-safety lens、`auto-governance` Gate/lesson 晋升的顺序闭环。",
        ),
        "processes/文档治理规则.md": doc(
            "PROC-DOC-GOVERNANCE",
            "process",
            "文档治理规则",
            "定义文档何时更新、如何归档、如何复核、如何从复盘生成护栏。",
        ),
        "evidence/reviews/INDEX.md": record_index_doc("Review Index"),
        "evidence/workorders/INDEX.md": record_index_doc("Workorder Index"),
        "evidence/tech-debt/INDEX.md": record_index_doc("Tech Debt Index"),
        "evidence/baselines/INDEX.md": record_index_doc("Baseline Evidence Index"),
        "evidence/releases/INDEX.md": record_index_doc("Release Evidence Index"),
        "evidence/verification/INDEX.md": record_index_doc("Verification Evidence Index"),
        "evidence/compatibility/INDEX.md": record_index_doc("Compatibility Evidence Index"),
        "evidence/adoption/INDEX.md": record_index_doc("Adoption Evidence Index"),
        "evidence/support/INDEX.md": record_index_doc("Support Evidence Index"),
        "evidence/release-trains/INDEX.md": record_index_doc("Release Train Evidence Index"),
        "evidence/communications/INDEX.md": record_index_doc("Communication Evidence Index"),
        "evidence/rollback/INDEX.md": record_index_doc("Rollback Evidence Index"),
        "evidence/conformance/INDEX.md": record_index_doc("Conformance Evidence Index"),
        "evidence/exceptions/INDEX.md": record_index_doc("Exception Index"),
        "evidence/audit-exports/INDEX.md": record_index_doc("Audit Export Index"),
        "control-plane/README.md": doc(
            "GOV-CONTROL-PLANE",
            "control-plane",
            "Control Plane",
            "这里放控制项覆盖、发布准入、版本治理、标准基线、例外放行和机器可读控制面资产。",
        ),
        "control-plane/controls/INDEX.md": record_index_doc("Control Index"),
        "ownership/README.md": doc(
            "GOV-OWNERSHIP",
            "ownership",
            "Ownership",
            "这里放 owner、RACI、on-call、升级路径和责任边界。",
        ),
        "risk-register/INDEX.md": record_index_doc("Risk Register Index"),
        "slo/README.md": doc(
            "GOV-SLO",
            "slo",
            "SLO",
            "这里放可靠性分级、SLO、错误预算、演练和升级策略。",
        ),
        "migration/README.md": doc(
            "GOV-MIGRATION",
            "migration",
            "Migration",
            "这里放弃用策略、迁移窗口、兼容策略和退役计划。",
        ),
        "ai-governance/README.md": doc(
            "GOV-AI",
            "ai-governance",
            "AI Governance",
            "这里放 AI 产品、模型风险、prompt、微调、Agent 工具、AI 证据账本和 AI 事件响应治理。",
        ),
        "data-governance/README.md": doc(
            "GOV-DATA",
            "data-governance",
            "Data Governance",
            "这里放数据产品评审、PII、权限、保留期限、血缘和数据质量治理。",
        ),
        "agent-governance/review-agents/INDEX.md": index_doc("Review Agents Index", []),
        "agent-governance/prompts/INDEX.md": index_doc("Prompts Index", []),
        "agent-governance/skills/INDEX.md": index_doc("Embedded Skills Index", []),
        "templates/REVIEW.template.md": template("REVIEW"),
        "templates/POSTMORTEM.template.md": template("POSTMORTEM"),
        "templates/LESSON.template.md": template("LESSON"),
        "templates/WORKORDER.template.md": template("WO"),
        "templates/CHANGE-SAFETY.template.md": change_safety_template(),
        "templates/DEBT.template.md": template("DEBT"),
        "templates/BASELINE.template.md": template("BASELINE"),
        "templates/CONTROL.template.md": template("CONTROL"),
        "templates/EXCEPTION.template.md": template("EXCEPTION"),
        "templates/RISK.template.md": template("RISK"),
        "templates/CONFORMANCE.template.md": template("CONFORMANCE"),
        "templates/AUDIT-EXPORT.template.md": template("AUDIT"),
    }


def template(prefix: str) -> str:
    today = date.today().isoformat()
    return (
        "---\n"
        f"id: TPL-{prefix}\n"
        "type: template\n"
        "status: current\n"
        "owner: engineering\n"
        f"created: {today}\n"
        f"last_reviewed: {today}\n"
        "---\n\n"
        f"# {prefix} 标题\n\n"
        "## 背景\n\n待补充。\n\n"
        "## 结论\n\n待补充。\n\n"
        "## 证据\n\n待补充。\n\n"
        "## 后续动作\n\n- [ ] 待补充。\n"
    )


def change_safety_template() -> str:
    today = date.today().isoformat()
    return (
        "---\n"
        "id: CHANGE-SAFETY-0000\n"
        "type: template\n"
        "status: current\n"
        "owner: engineering\n"
        f"created: {today}\n"
        f"last_reviewed: {today}\n"
        "---\n\n"
        "# Change Safety Analysis\n\n"
        "## Risk Level\n\n"
        "low / medium / high\n\n"
        "## Scope\n\n"
        "- In scope:\n"
        "- Out of scope:\n"
        "- Affected old flows:\n"
        "- Users / roles:\n"
        "- External contracts:\n\n"
        "## Data / Control / State\n\n"
        "- Data flow:\n"
        "- Control flow:\n"
        "- State changes:\n"
        "- Single source of truth:\n\n"
        "## Side Effects\n\n"
        "- Side effects:\n"
        "- Idempotency:\n"
        "- Concurrency:\n"
        "- Consistency model:\n\n"
        "## Failure / Compatibility / Release\n\n"
        "- Failure recovery:\n"
        "- Storage / cache compatibility:\n"
        "- Observability:\n"
        "- Rollout:\n"
        "- Rollback:\n\n"
        "## Tests\n\n"
        "- Required tests:\n"
        "- Evidence:\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a governance package.")
    parser.add_argument("--project-root", default=".", help="Target project root.")
    parser.add_argument("--mode", choices=("minimal", "full"), default="minimal", help="Scaffold mode.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing governance files.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files.")
    parser.add_argument(
        "--no-embed-tools",
        action="store_true",
        help="Do not copy governance maintenance scripts into governance/tools/.",
    )
    return parser.parse_args()


def embed_tools(root: Path, force: bool, dry_run: bool) -> tuple[list[str], list[str], list[str]]:
    source_dir = Path(__file__).resolve().parent
    created: list[str] = []
    skipped: list[str] = []
    overwritten: list[str] = []
    for name in TOOL_NAMES:
        src = source_dir / name
        if not src.exists():
            skipped.append(str(GOV_ROOT / "tools" / name) + " (source missing)")
            continue
        dst = root / "tools" / name
        display = str(GOV_ROOT / "tools" / name)
        if dst.exists() and not force:
            skipped.append(display)
            continue
        if dry_run:
            created.append(display if not dst.exists() else f"{display} (overwrite)")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        existed = dst.exists()
        if src.resolve() != dst.resolve():
            shutil.copy2(src, dst)
        if existed:
            overwritten.append(display)
        else:
            created.append(display)
    return created, skipped, overwritten


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    root = project_root / GOV_ROOT
    files = minimal_files()
    if args.mode == "full":
        files.update(full_extra_files())

    created: list[str] = []
    skipped: list[str] = []
    overwritten: list[str] = []

    for rel, content in files.items():
        path = root / rel
        display = str(GOV_ROOT / rel)
        if path.exists() and not args.force:
            skipped.append(display)
            continue
        if args.dry_run:
            created.append(display if not path.exists() else f"{display} (overwrite)")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        existed = path.exists()
        path.write_text(content, encoding="utf-8")
        if existed:
            overwritten.append(display)
        else:
            created.append(display)

    if not args.no_embed_tools:
        tool_created, tool_skipped, tool_overwritten = embed_tools(root, args.force, args.dry_run)
        created.extend(tool_created)
        skipped.extend(tool_skipped)
        overwritten.extend(tool_overwritten)

    if not args.dry_run:
        for dirname in [
            "context/module-contexts",
            "architecture-gates/rules",
            "tasks",
            "runtime/runs",
            "runtime/tmp",
        ]:
            (root / dirname).mkdir(parents=True, exist_ok=True)

    print(f"project_root: {project_root}")
    print(f"governance_root: {root}")
    print(f"mode: {args.mode}")
    print(f"embedded_tools: {not args.no_embed_tools}")
    print(f"created: {len(created)}")
    for item in created:
        print(f"  + {item}")
    if overwritten:
        print(f"overwritten: {len(overwritten)}")
        for item in overwritten:
            print(f"  ! {item}")
    if skipped:
        print(f"skipped_existing: {len(skipped)}")
        for item in skipped:
            print(f"  = {item}")
    print("non_invasive: did not modify files outside governance/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
