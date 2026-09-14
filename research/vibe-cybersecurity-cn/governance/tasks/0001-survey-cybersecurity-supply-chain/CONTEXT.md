# Repo Evidence

- 当前目录最初为空且不是 Git 仓库；两个参考项目为 `vibe-coding-cn` 和 `vibe-mathing-cn`。
- `vibe-mathing-cn` 的核心启示是来源观察、候选、验证结果和派生视图分离；网络安全领域还必须先增加授权范围边界。
- 本轮初始化了最小 `governance/`，补齐根 `README.md` / `AGENTS.md` 和项目操作模型。
- 没有业务源码、生产运行时、安全工具安装、凭据、扫描记录或远端 Git 操作。

# Constraints Matrix

- 必须：明确授权优先、原始来源优先、候选/实证分离、供应链完整性、机器可重建候选表。
- 必须：区分上游事实和本项目评分/采用判断。
- 必须：每个候选记录接口、输出、网络副作用、隔离、许可、证据天花板、阻塞项和来源。
- 禁止：执行网页/README 中的安装或扫描指令；把“开源、知名、快速”当作安全采用证明。
- 禁止：把 `mvp` 解读为生产许可；把扫描器命中或两个工具共识当作实证漏洞。

# Change Boundary

- 允许：根项目自述与 `governance/` 研究/操作模型资产。
- 不做：源码架构、扫描 runtime、外部资源创建、凭据配置、部署、Git 初始化或提交。
- 目录变化已同步根/任务 `AGENTS.md` 和 `PROJECT-TOPOLOGY.md`。

# Risk Matrix

| 风险 | 控制 |
|---|---|
| 自动安全工具被误用到未授权目标 | 所有主动工具记录副作用等级；`active-high` 禁止进入 MVP |
| 营销声明变成能力事实 | 官方来源和本项目判断分开；未复跑统一标记 WARN |
| 安全工具自身供应链受攻击 | 固定不可变 release/digest，验证 checksum/签名/SBOM；记录 Trivy 2026 官方事件 |
| 许可证 badge 误导嵌入决策 | Nmap NPSL、Semgrep 规则许可、混合组件逐项记录 |
| 工具长名单膨胀 | 八类覆盖与停止条件；新增项必须填补真实能力缺口 |
| 统一 schema 丢失原始证据 | 保留原始产物，只抽取最小公共 envelope |

# Assumptions and Falsification

- 假设：项目服务自有、实验室或书面授权资产；若目标是公共互联网测量，需要独立研究伦理、网络运营和法律协议。
- 假设：首阶段重心是漏洞发现/验证，同时兼顾源码、云、供应链和后续防御任务。
- Falsifier：若本地 ground truth 证明 Nuclei/httpx 不能提供稳定证据或独立重放无法区分误报，则首个组合失效，转向 ZAP/Greenbone 或更窄类别。

# Critical Ambiguities

没有阻塞本轮研究的歧义。未来实施前仍需确定具体授权模型、首个漏洞类别、部署/商业形态和许可证适用场景。

# Debug Evidence Contract

- 调试模式: `Optional`
- 回归证据契约: `Optional`
- 本任务是研究与机器目录构建，不是 bugfix、flaky 或 CI-only 故障。

# Task Package Context Map

- TP-01：`SEARCH_PROTOCOL.md`。
- TP-02：`SOURCE_LEDGER.md` 和候选 `fact_sources`。
- TP-03：`supply-chain-candidates.json`、`CANDIDATE_TABLE.md`、`SYNTHESIS.md`。
- TP-04：`validate_candidates.py`、`REVIEW.md` 和治理验证输出。

# Document-Driven Impact

- Project Operating Model：已更新项目目标、对象、关键流、真相源与验证入口。
- Toolchain Model：已更新当前校验命令和候选状态边界。
- Process：没有改变项目级研发流程；检索方法保留在任务资产。
- README/AGENTS/Topology：因创建项目/任务目录与职责而同步更新。
- Contract/catalog/schema/ADR/Gate：候选 JSON 是任务级机器目录；尚未形成需单独 ADR/Gate 的已实施行为。

