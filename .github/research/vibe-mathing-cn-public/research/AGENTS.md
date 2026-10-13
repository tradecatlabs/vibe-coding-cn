# Research Space Agent Guide

本目录是数学研究尝试的真相源。`records/attempts.jsonl` 记录研究活动；`schema/attempt.schema.json` 定义机器契约。ProblemContract 的输入契约位于 `problem-library/schema/canonical-problem.schema.json`。

## 目录结构

```text
research/
├── AGENTS.md
├── README.md
├── verifiers.json             # generator/verifier 信任域与能力注册表
├── artifacts/                 # 真实 verifier 输出与可重算回执
├── runs/                      # 可恢复运行 checkpoint（本地忽略）
├── schema/
│   ├── attempt.schema.json
│   ├── evidence-receipt.schema.json
│   ├── research-bundle.schema.json # 只读派生响应
│   ├── failed-route.schema.json
│   ├── run-state.schema.json
│   └── verifier-registry.schema.json
└── records/
    ├── attempts.jsonl
    └── failed-routes.jsonl       # 可选、append-only 失败路线账本
```

## 职责与依赖

- 上游：规范化 `Problem`、文献目录和项目数学 skills；在顶层编排中，`research/` 消费 Project/Workflow 下的 Attempt 活动，不拥有五级生命周期的第二套状态源。
- 下游：`result-library/records/results.jsonl` 中引用当前 Attempt 的候选成果。
- 不把尝试完成等同于问题解决；`lifecycle=completed` 只表示本次活动停止。
- `generator` 记录候选生成主体；解库所依赖的独立证据不得由同一主体签发。
- 独立性从 `verifiers.json` 的 trust domain 派生；Result 自报布尔值没有通过权。
- `artifacts/` 是证据可信根；locator 逃逸、symlink、文件缺失或现场摘要不符一律拒绝。每张 evidence receipt 必须记录 timeout、memory/threads/output 预算、停止条件和终止状态；无 timeout 的成功路径不得晋升。
- `.store.lock`、事务日志与 `runs/` 属于可恢复 runtime，不是数学事实源；Job 的执行状态不能替代 Attempt lifecycle 或 Result outcome。
- 只有 `lifecycle=active` 的 ProblemContract 允许新 Attempt；契约 lifecycle 单向转换，不能用状态字段伪造开放问题已解决。
- `ResearchBundle` 只从同一锁内的一致快照派生，不新增可写 collection；proof 与 counterexample 同时闭合时必须 fail-closed。
- 失败路线账本只追加；路线耗尽、数值伪影或阻塞不是 Result。
- 输入、声明和产物使用稳定 ID 或仓库相对路径；不得写入凭据、私有材料或伪造日志。
- 新增、删除或移动文件时同步维护本文件与 README。

## 验证

```bash
python3 scripts/validate_research_spaces.py
python3 scripts/validate_failed_routes.py
```
