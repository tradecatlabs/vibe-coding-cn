---
id: GOV-TOOLCHAIN-MODEL
type: context
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-09-04
review_cycle: P90D
---

# Toolchain Model

本文件记录项目工具链的当前真相，帮助人类和代理优先复用成熟能力、项目既有脚本和稳定验证入口。

## 成熟工具优先

- 优先使用语言标准工具、官方 CLI、包管理器、测试框架、lint/typecheck、数据库迁移工具和云平台能力。
- 自研脚本只用于连接、编排、适配和表达项目特有流程。
- 新增工具前必须证明：已有工具无法满足、引入后总拥有成本更低、验证和回滚路径明确。

## 项目命令

| 场景 | 命令 | 备注 |
|---|---|---|
| 安装依赖 | 无持久安装步骤 | `uv` 按 PEP 723 声明创建隔离环境并锁定 `jsonschema` |
| 测试 | `uv run --locked --script scripts/validate_harness.py --self-test` | Harness、Operator Library 与 Runtime Core 正例必须 PASS，关键负例必须 BLOCK |
| 类型检查 | `python3 -m py_compile scripts/validate_harness.py scripts/validate_operator_library.py examples/reference_harness/reference_harness.py` | 当前规模的最小语法门禁 |
| lint / format | `python3 -m json.tool <file>` | JSON 语法；Markdown/链接由 governance strict validator 检查 |
| 构建 | N/A | 当前无服务或发布产物 |
| 本地运行 | `uv run --locked --script scripts/validate_harness.py <manifest...>` | 可批量校验 manifest |
| Operator Pack Core 校验 | `uv run --locked --script scripts/validate_harness.py --operator-pack <pack.json>` | 只检查公共字段结构、类型判别与安全 owner |
| 参考算子库校验 | `uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json` | 检查 Profile、411/411 覆盖、57/57 派生 Method 与引用 |
| Runtime Core 校验 | `uv run --locked --script scripts/validate_harness.py --operator-runtime <json...>` | 校验 Binding、RunRequest 与 RunRecord 稳定信封 |
| 参考 Harness | `python3 examples/reference_harness/reference_harness.py` | 输出无副作用 instruction packet 和摘要记录 |
| 参考 Harness 回归 | `python3 -m unittest tests.test_reference_operator_harness` | 覆盖选择、三种 Spec、预算、策略、引用与篡改拒绝 |
| 上游同步 | `bash scripts/sync_upstreams.sh` | 浅克隆/fast-forward 官方仓库并刷新 revision lock；不执行上游代码 |
| 项目门禁 | `python3 scripts/verify_project.py --gate <capability>` | 命令与 artifact 由 control-plane registry 固定 |
| 发布 | 未接入 | 出现真实发布目标后新增可重跑入口 |
| 回滚 | 普通反向提交恢复上一 Schema/manifest revision | 破坏性变化必须升级 `api_version`；当前无持久业务状态 |

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

## Verification Control Plane

- Policy：`governance/control-plane/verification-policy.v1.yaml`。
- Capability Registry：`governance/control-plane/verification-capabilities.v1.yaml`。
- 项目级 capability artifact：被忽略的 `governance/runtime/verification-artifacts/`；任务只引用新鲜结果，不拥有 runner 输出路径。
- `enforce` 只表示本地确定性 closeout fail-closed；未建立真实 Harness corpus、holdout、
  生产 trace 和外部 reviewer 前，生产 Verification Control Plane 仍处于校准前阶段。
