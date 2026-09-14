# Changelog

## 0.3.0

- 候选来源状态和 candidate formal file 不得触发研究证明或 Result 晋升。
- 研究库任务必须先绑定明确请求或 active ProblemContract。

## 0.2.0 - 2026-08-26

- 增加 proof-obligation DAG 的唯一节点、依赖存在、无环和开放义务 fail-closed 契约。
- 分离 route status 与原 Claim status，阻止“辅助引理失败即原命题被反驳”的错误升级。
- 接入固定 commit 的 ProofFlow 与 Lean 官方 Skills 证据谱系，并以源码缺陷生成反例压力测试。

## 0.1.0 - 2026-08-13

- 建立定理陈述、证明义务、依赖图、反例攻击和状态分层契约。
