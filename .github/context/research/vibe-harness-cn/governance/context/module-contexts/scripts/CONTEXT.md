---
id: CTX-SCRIPTS
type: module-context
status: current
owner: engineering
created: 2026-09-03
last_reviewed: 2026-09-03
code_path: scripts
---

# 验证脚本 Context

## 代码路径

`scripts`

## 模块职责

- 提供 Harness manifest、Operator Pack/Runtime Core、Reference Library Profile 和项目 Gate 的薄验证入口。
- 组合 Python 标准库、`jsonschema`、Git 与治理 capability registry，输出确定性 PASS/BLOCK。
- 提供官方 Harness 上游同步和 revision lock 的可重跑入口。

## 非职责

- 不拥有 Harness 或 Operator 的领域语义、字段规范和内容目录。
- 不执行 Operator、上游 Harness、模型、tool binding 或业务 workflow。
- 不把调用者自报摘要当成验证事实。

## 单一真相源

- Harness 字段：`contracts/harness-manifest.schema.json`。
- Operator Core 字段：`contracts/problem-solving-operator-pack.schema.json`。
- Operator Runtime 字段：`contracts/operator-runtime.schema.json`。
- Reference Profile：`operators/catalog.json`、inventory 与 pack。
- 项目 Gate：`governance/control-plane/verification-capabilities.v1.yaml`。
- 工具链边界：`governance/context/TOOLCHAIN_MODEL.md`。

## 常用验证

- `uv run --locked --script scripts/validate_harness.py --self-test`
- `uv run --locked --script scripts/validate_harness.py --operator-pack contracts/examples/minimal-operator-pack.json`
- `uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json`
- `uv run --locked --script scripts/validate_harness.py --operator-runtime contracts/examples/minimal-operator-binding.json contracts/examples/minimal-operator-run-request.json contracts/examples/minimal-operator-run-record.json`
- `python3 scripts/verify_project.py --gate test`

## Agent Rules

- 自研脚本只连接成熟工具与项目规则；能在 JSON Schema 表达的字段格式不重复写 Python 分支。
- 跨文件 exact-set、引用和安全路径属于 Profile/策略检查，不得提升为 Core 内容约束。
- 新命令必须同步 `scripts/AGENTS.md`、`TOOLCHAIN_MODEL.md`、正反例和 capability registry（如适用）。
- 失败必须非零退出并给出可定位路径；输出不得泄露凭据、prompt 或工具内容。
