# 0001-bootstrap-meta-harness

- Exemplar ID: `EX-0001-bootstrap-meta-harness`
- Source Task: `0001-bootstrap-meta-harness`
- Evidence Digest: `sha256:0734d03a6f4e51515e5aeb44a72c213e230d68690445e6c29d4abbc299c7b7e6`

## 来源任务

- `0001-bootstrap-meta-harness`

## 目标与范围

- 0001-bootstrap-meta-harness

## 实际解决路径

- 先定义 Agent/Harness/Meta Harness 的 owner 与控制面/数据面边界，再导出供应商中立 manifest。
- 复用 Draft 2020-12 JSON Schema、jsonschema 与 uv script lock，薄 Python 只表达跨字段策略。
- 把 high-risk Task Intent 编译为项目 Verification Plan，用 owner-derived Git tree digest 和 fresh gate reexecution 收口。

## 关键决策与拒绝方案

- 选择契约优先控制面；拒绝首版统一 runtime、数据库、UI、队列与插件系统。
- 首版审批仅支持 never/always；没有真实 resolver 时不暴露 conditional policy URI。

## 失败、根因与修复

- 悬空工具/审批 URI 会形成准入假绿，已改为可解析内联契约和明确审批。
- gate runner 猜错 owner 输出类型导致误 BLOCK，已用 RED/GREEN/反事实回归修复。

## 验证证据

- manifest 正例通过且多类结构/策略负例被拒绝。
- 六个 required capability 由 owner strict validator 重新执行并验证 input/policy/artifact digest。

## 回滚与恢复

- 本轮仅本地文件与本地 revision；契约回滚到上一受支持 api_version/revision，不影响外部系统。

## 可复用候选与边界

### 候选
- exemplar

### 边界
- 本范例只描述控制面 bootstrap 方法，不证明真实 Harness runtime、eval、trace 或生产晋升。
- 单次成功只生成 Completion Exemplar，不晋升 active SOP。
