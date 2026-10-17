---
id: GOV-CONTROL-AGENTS
type: context
status: current
owner: engineering
created: 2026-08-14
last_reviewed: 2026-08-14
review_cycle: P90D
---

# control-plane 目录

本目录保存元 Harness 自身的机器治理策略，不保存受管 Harness 的业务状态或运行数据。

```text
control-plane/
├── AGENTS.md                              # 本目录职责与依赖边界
├── controls/INDEX.md                      # 控制项索引
├── verification-policy.v1.yaml            # 风险等级到 required capability 的映射
└── verification-capabilities.v1.yaml      # 项目真实命令、owner、timeout 与 artifact
```

依赖方向：Task Intent 读取 policy，policy 只引用 capability ID，capability registry 绑定项目
真实命令；`auto-tasks` 编译任务计划，`auto-review` 执行命令并生成证据。调用者不得在运行时
降低 required 能力、替换命令或自定义证据摘要排除路径。

策略处于项目本地确定性门禁层；没有真实 Harness corpus、holdout、外部 reviewer 和生产 trace
前，不得把它描述为已校准的生产验证系统。
