# 研究空间

`research/` 保存从规范化问题出发的一次次研究尝试。它记录做过什么、使用了什么方法、产生了哪些声明和产物；不负责宣布问题已经解决。顶层编排语言是 `Project → Workflow → Task → Step → Job`，其中 `Job` 是 `Step` 的一次有界执行；它与本目录的 `Attempt` 和数学结果状态正交。

## 目录结构

```text
research/
├── AGENTS.md
├── README.md
├── verifiers.json
├── artifacts/
│   └── README.md
├── runs/                    # 本地可恢复 checkpoint，Git 忽略
├── schema/
│   ├── attempt.schema.json
│   ├── evidence-receipt.schema.json
│   ├── research-bundle.schema.json # 只读派生响应契约
│   ├── failed-route.schema.json
│   ├── run-state.schema.json
│   └── verifier-registry.schema.json
└── records/
    ├── attempts.jsonl
    └── failed-routes.jsonl       # 可选、append-only 失败路线账本
```

## 边界

- 每个 `Attempt` 必须引用 `problem-library/records/canonical-problems.jsonl` 中的一个问题，并记录候选生成者 `generator`。
- discovery、derivation、computation、proof、formalization 是研究方法，不是完成等级。
- `lifecycle` 只描述尝试的运行状态，不表达数学结论；失败、阻塞和未闭合证明义务可以保存。Job 成功、Attempt completed 或 Workflow 完成都不能单独关闭数学问题。
- 研究产物要进入成果空间，必须另建 `Result` 并通过验证门。
- Result 的证据项只是一张回执索引；真实性由 `artifacts/` 内回执、底层输出的现场 SHA-256 和 `verifiers.json` 共同派生。每张回执还必须记录正 timeout、memory/threads/output 资源预算、停止条件和 termination 状态；accept 只能来自 completed 且 exit code 为 0 的路径。
- 运行时采用单机 `flock + WAL + fsync + os.replace` 唯一 writer；中断后重启先完成日志恢复，再接受新写入，跨表断链在锁内拒绝。
- `ResearchBundle` 从同一锁内的一致快照派生，不是第四张可写真相表；`export-bundle` 遇到 proof/counterexample 双闭合冲突必须非零失败。
- 失败路线账本只追加，不能覆盖历史；它记录方法阻塞，不等于数学反例或 Result。

## 验证

```bash
python3 scripts/validate_research_spaces.py
python3 scripts/test_trusted_evidence.py
python3 scripts/test_evidence_attacks.py
python3 scripts/test_research_store.py
python3 scripts/test_research_bundle.py
python3 scripts/validate_failed_routes.py
```
