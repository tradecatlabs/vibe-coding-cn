# Review

- Date: `2026-08-13`
- Target: 开源网络安全 Agent 供应链首轮调研
- Provenance: 主 Agent 自审，不具备外部独立 reviewer provenance
- Verdict: `WARN`

## Findings

### WARN-01 — 候选尚未固定版本本地复跑

- Evidence: `SOURCE_LEDGER.md` 明确记录本轮只核验官方仓库、文档、许可和公开安全事实。
- Impact: `mvp/pilot` 表示研究优先级，不是生产可用声明。
- Minimal fix: 下一任务固定 Juice Shop/httpx/Nuclei/Cosign 版本与镜像 digest，执行本地隔离负例和正例。

### WARN-02 — 混合项目许可证仍需 artifact 级审查

- Evidence: Greenbone、PentAGI、Nettacker、WebGoat、Prowler、in-toto 等候选标有固定版本复核门禁；Nmap 使用 NPSL，Semgrep 规则许可独立于引擎。
- Impact: 不能根据 GitHub 页面单一 license badge 决定商业嵌入或再分发。
- Minimal fix: 采用时生成组件清单，逐 LICENSE/NOTICE/镜像层复核并记录结论。

### WARN-03 — 实证漏洞准入尚未用 ground truth 证明

- Evidence: `SYNTHESIS.md` 只定义 proof point 与 falsifier，尚无真实 ValidationRun artifact。
- Impact: 当前完成的是候选选型，不是“自动找漏洞系统就绪”。
- Minimal fix: 用本地 Juice Shop 正负例证明同生成器自证、越权目标、证据篡改和失效记录无法晋升。

### WARN-04 — 全局复盘 handoff 被 owner state 陈旧证据阻塞

- Evidence: `auto-retro` 已派生 `RETROSPECTIVE_REQUIREMENT.json`（risk=`medium`），本地 draft 通过 strict validation；canonical ingest 在预检无关的 `RETRO-TRADECAT-0361-V2-FIVE-MODEL-PRODUCTION` 时发现其 `STATUS.md` 与 Kubernetes manifest 摘要漂移并 fail-closed。
- Impact: 本轮研究资产和项目校验不受影响，但不能声称全局 canonical retrospective closeout 完成。
- Minimal fix: 由 TradeCat/auto-retro owner 修复或归档陈旧记录并重建全局 registry；随后重新 seal、ingest 并签发本任务 `RETROSPECTIVE_HANDOFF.json`。本任务不越权修改外部项目。

## Passed Checks

- 候选事实字段和项目判断字段分离。
- 46 个候选全部有官方/原始来源、许可初筛、机器接口、网络副作用、隔离要求、证据上限和阻塞项。
- `active-high` 没有进入 `mvp`。
- 候选表由机器目录生成，不维护第二套手工状态。
- Trivy 2026 官方供应链事件已进入采用门，而不是只看当前 release 页面。
- Nmap NPSL、Semgrep 规则许可、Nuclei 模板签名和 EPSS 非开源运营管线等非显然边界已显式记录。
- 没有下载、安装或执行任何攻击/扫描工具，没有访问任何目标。
- `no-code` / `reuse` / `ponytail` 审查通过：本轮没有提前实现控制面、插件框架、多 Agent 或扫描引擎；唯一自研脚本只负责项目特有 schema 门禁和确定性渲染，并复用 Python 标准库。
- `future-optimal` 审查通过：首个切片直接验证授权、独立验证和证据晋升，不围绕“万能渗透 Agent”增加包装层。
- 性能审查通过：候选校验和排序为 `O(n log n)` 时间、`O(n)` 空间，当前 `n=46`，不是系统 hot path；真正的规模风险已在 `SYNTHESIS.md` 约束为有界网络 I/O、模板展开和验证预算。
- 主要任务复用采样已严格生成：项目特有时点目录不重复晋升为全局 SOP，通用流程继续由既有 owner skills 持有。

## Unknowns

- 不同工具在本地 ground truth 上的误报、漏报与证据完整率。
- Agent runtime 的 prompt injection、越权与停止条件负例表现。
- 大规模运行的 p95/p99、CPU/内存、网络和 token/API 成本。
- 许可证对未来具体发布/商业形态的适用结论。
- 全局 auto-retro owner registry 的陈旧外部记录何时完成修复。

## Gate

候选研究和首轮架构分析可以交付；任何“已验证、可扫描、生产可用”或“全局复盘 closeout 已完成”的声明继续 BLOCK，直到对应 pilot 或 owner handoff 证据存在。
