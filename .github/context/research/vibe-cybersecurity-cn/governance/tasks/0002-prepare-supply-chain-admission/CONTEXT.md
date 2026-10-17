# Repo Evidence

- 0001 保存 46 项研究候选，其中 18 项状态为 `mvp`。
- 0001 的 `mvp` 只表示值得本地验证，并非供应链批准。
- 当前仓库没有业务运行时、安装清单、lockfile 或扫描入口。
- 项目原则要求成熟工具优先，但工具、规则和数据均是不可信供应链输入。

# Constraints Matrix

| 约束 | 强制决策 |
|---|---|
| 不复制研究事实 | 名称、上游、许可和网络副作用从 0001 读取 |
| 默认无副作用 | 候选字段保持 `default_enabled=false`；具体运行权不进入供应链状态机 |
| 不能虚构版本 | `pin` 保持 pending，直到真实 artifact 被验证 |
| 安全工具也是攻击面 | engine、规则、插件、DB 分别固定和失效 |
| 候选不等于事实 | 扫描输出仍只能创建候选漏洞 |
| 本轮不执行 | 不下载、不安装、不联网、不扫描 |

# Change Boundary

本轮只修改任务 0002、根/治理目录自述和项目操作模型相关文档；不创建运行时代码，不修改 0001 研究真相源。

# Risk Matrix

| 风险 | 影响 | 控制 |
|---|---|---|
| 研究状态被误读为批准 | 未验证工具进入执行面 | 独立准入状态机，运行权仍归 ScopeGrant/策略 |
| 版本字段被猜测 | 无法复现、供应链污染 | pin 为空且 pending |
| 工具与规则混为一个制品 | 规则漂移绕过审查 | Nuclei engine/template 分开建账 |
| 主动工具提前启用 | 越权或副作用 | W2/W3 后置、隔离配置和 ScopeGrant |
| 同类工具全部纳入 | 所有权和成本膨胀 | 波次按 proof point，而非数量推进 |

# Assumptions and Falsification

- 假设：0001 的 18 个 MVP 都应进入“候选队列”；若后续许可证或安全事件阻断，可转 `suspended/retired`，不影响其他候选。
- 假设：先做 W0/W1 能降低 W2 主动验证风险；若本地实验表明关键 Web 证据无法由这些能力支持，则重新调整波次。
- 推翻条件：研究目录 snapshot 漂移、候选不再为 MVP、出现 active-high 候选或准入字段无法完整验证时，校验器必须 BLOCK。

# Critical Ambiguities

- 具体版本、OCI digest、数据快照和 trusted issuer 尚未选择；本轮明确保持 pending。
- 未来商业分发形态尚未确定；许可证审查不能提前完成。
- 运行时沙箱尚未实现；隔离政策目前是准入契约，不是运行证据。

# Debug Evidence Contract

- 调试模式: `Optional`

任务本身不是 bugfix；实施中发现的血缘解析缺陷已按 `DEBUG.md` 留下 RED/GREEN。其他失败证据由校验器非零退出、具体候选 ID 和门禁字段产生。

# Task Package Context Map

- TP-01：`ADMISSION_POLICY.md`
- TP-02：`admission-candidates.json`
- TP-03：`validate_admission_candidates.py`、`ADMISSION_CANDIDATE_TABLE.md`
- TP-04：项目操作模型、工具链、拓扑、README/AGENTS 和治理校验结果
