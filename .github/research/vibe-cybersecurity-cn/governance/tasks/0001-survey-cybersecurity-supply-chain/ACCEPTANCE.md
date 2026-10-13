# Task-Level Acceptance

- [x] 八类供应链均有代表候选，且满足明确停止条件。
- [x] 每个候选包含官方来源、许可初筛、机器接口、输出、副作用、隔离、证据上限、阻塞和状态。
- [x] 候选机器真相源可校验，并能确定性重建 Markdown 表。
- [x] 首个本地纵向样例、第二阶段组合、淘汰项和供应链门禁明确。
- [x] 完成声明严格限定为“首轮调研与候选表完成”。

# Validation Plan

- `python3 validate_candidates.py`：校验 schema、来源、评分、主动风险与状态，并重建候选表。
- `python3 -m py_compile validate_candidates.py`：校验 Python 语法。
- `python3 governance/tools/rebuild_governance_index.py --project-root .`：重建治理索引。
- `python3 governance/tools/validate_governance_package.py --project-root . --strict`：治理结构和链接门禁。
- `python3 governance/tools/governance_health_report.py --project-root . --strict`：占位、过期与治理健康。
- `validate_task_docs.py --phase closeout`：任务状态与证据一致性。

# Review Gate

- BLOCK：`active-high` 进入 MVP；缺官方来源；许可证或事故被隐藏；候选表与 JSON 漂移。
- BLOCK：声称工具已测试、系统已可扫描或生产就绪。
- WARN：候选尚未固定版本本地复跑；混合项目许可证未做 artifact 级法律复核。
- PASS：机器资产与文档一致，所有限制和未验证项可见。

# Runtime Verification Gate

- 本轮只验证目录结构、来源可追溯和选型逻辑。
- 不验证任何候选实际发现率、误报率、性能、安全默认值或生产兼容性。
- 任何运行时能力必须在下一任务用隔离 ground truth 正负例重新证明。

# Ship Readiness

首轮调研可交付；运行时交付继续 BLOCK。回滚只涉及本地 Markdown/JSON/Python 文件，无外部资源或数据迁移。

# Task Package Acceptance

- TP-01：范围、证据层级、评分、风险分级、停止和刷新条件完整。
- TP-02：强结论回指官方仓库、官方文档、官方 advisory 或原始论文。
- TP-03：机器目录、自动表和综合架构一致；新增候选无无价值堆叠。
- TP-04：结构/治理校验通过，自审明确剩余 WARN 和未知项。

# Anti-Goals

- 不下载、安装、运行或部署候选工具。
- 不扫描目标，不测试凭据，不生成利用 payload。
- 不把 GitHub 星标、README 营销和模型自评当作能力验证。
- 不建立新扫描框架、数据库、Kubernetes 平台或多 Agent runtime。

