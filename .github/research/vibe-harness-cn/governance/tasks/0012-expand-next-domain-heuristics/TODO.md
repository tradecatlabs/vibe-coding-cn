# Execution Checklist
[x] TP-01.01 | P0 | 因果推断研究 | Verify: 核对验收项: 至少形成可审计的因果建模、干预或敏感性程序 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.02 | P0 | 经济与博弈研究 | Verify: 核对验收项: 明确假设、参与者、收益、约束和均衡/偏离证据 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.03 | P0 | 生态与生物研究 | Verify: 核对验收项: 区分机制假设、观察证据、模型和现实实验边界 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.04 | P0 | 认知科学研究 | Verify: 核对验收项: 把认知发现转换为问题空间动作而非人格或能力标签 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.05 | P0 | 人因可靠性研究 | Verify: 核对验收项: 明确人为复核、升级、停止和恢复边界，不自动放行高影响动作 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.06 | P0 | 医学决策研究 | Verify: 核对验收项: 所有结论标记为参考，明确不能替代专业诊疗或临床流程 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-02 | P0 | 既有库缺口与重复审计 | Verify: 核对验收项: 每个候选有 add/crosswalk/gap 决策；不因追求数量重复登记同义条目 | Gate: 前置步骤已完成: research-evidence | Parallelizable: No
[x] TP-03 | P0 | 提炼新增算子与组合 Method | Verify: 核对验收项: 所有新增 source 有来源和功能主类；治理字段保持 harness_policy、verifier、reference_only；derived Method 只引用已登记条目 | Gate: 前置步骤已完成: gap-audit | Parallelizable: No
[x] TP-04 | P0 | 入库并同步目录文档 | Verify: 核对验收项: source inventory、pack 和 catalog 精确一致；所有受影响 source-of-truth 已更新或记录具体豁免 | Gate: 前置步骤已完成: define-operators | Parallelizable: No
[x] TP-05 | P0 | 验证、审查与交付收口 | Verify: 核对验收项: required gates 全部 PASS；任务级 verification 绑定 clean HEAD、当前输入、策略和 artifact；未验证项与后续路径已记录 | Gate: 前置步骤已完成: materialize-library | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
