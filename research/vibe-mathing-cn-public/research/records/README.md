# `failed-routes.jsonl`

失败路线登记是可选的 JSONL 账本：每行记录一条曾尝试但未闭合的研究路线。它只追加，不改写历史；失败路线不是数学反例，也不是 `Result`。

## 用途

把“这条路为什么暂时走不通”沉淀为可检索知识，避免重复投入。`blocked`、`exhausted`、`artifact` 和 `superseded` 需要与证据路径一起记录；不能用路线状态替代独立验证。

## 合成示例

```json
{"route_id":"route:synthetic-lra-enumeration-20260901","problem_id":"problem:synthetic-contract-active","route":"bounded integer enumeration","blocker":"the finite bound does not imply the quantified statement","conclusion":"blocked","evidence":["fixtures/smt-lra/case.json"],"recorded_at":"2026-09-01T00:00:00Z","recorded_by":"synthetic-test"}
```

## 字段

| 字段 | 含义 |
| --- | --- |
| `route_id` | 稳定路线标识，不能重复覆盖 |
| `problem_id` | 关联的 ProblemContract 标识 |
| `route` | 尝试过的方法或方向 |
| `blocker` | 最具体的阻塞、预算边界或伪影原因 |
| `conclusion` | `blocked`、`exhausted`、`refuted`、`artifact` 或 `superseded` |
| `evidence` | 至少一条仓库相对路径或可复核引用 |
| `recorded_at` | 带时区的 RFC3339 时间 |
| `recorded_by` | 非敏感的登记者标签 |

## 校验

```bash
python3 scripts/validate_failed_routes.py
```

新路线下发前应先读取同一 Problem 的历史账本；重复已登记的死路必须明确说明新输入或新假设。账本不能包含 prompt、reasoning、凭据、机器身份或内部路径。
