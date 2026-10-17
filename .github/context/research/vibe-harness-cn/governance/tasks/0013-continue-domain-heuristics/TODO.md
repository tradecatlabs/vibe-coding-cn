# Execution Checklist
[x] TP-01.01 | P0 | 法律推理研究 | Verify: 核对验收项: 形成可追溯的争点、规则、事实、反方和证明标准程序 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.02 | P0 | 伦理与公共政策研究 | Verify: 核对验收项: 形成可审计的影响、权利、比例、监督和责任检查 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.03 | P0 | 教育与学习科学研究 | Verify: 核对验收项: 区分学习过程证据、迁移证据和熟悉感，保留支架与反馈边界 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.04 | P0 | 语言学研究 | Verify: 核对验收项: 结论绑定语言变体、语域、标注、上下文和可反驳对比 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.05 | P0 | 历史推理研究 | Verify: 核对验收项: 区分来源证据、解释推断和反事实假设，不把叙事写成事实数据库 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.06 | P0 | 社会科学方法研究 | Verify: 核对验收项: 形成问题—构念—样本—方法—解释的可追溯链 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-02 | P0 | 既有库缺口与重复审计 | Verify: 核对验收项: 每个候选有 add/crosswalk/gap 决策；不因追求数量重复登记同义条目 | Gate: 前置步骤已完成: research-evidence | Parallelizable: No
[x] TP-03 | P0 | 提炼新增算子与组合 Method | Verify: 核对验收项: 所有新增 source 有来源和功能主类；治理字段保持 harness_policy、verifier、reference_only；derived Method 只引用已登记条目 | Gate: 前置步骤已完成: gap-audit | Parallelizable: No
[x] TP-04 | P0 | 入库并同步目录文档 | Verify: 核对验收项: source inventory、pack 和 catalog 精确一致；所有受影响 source-of-truth 已更新或记录具体豁免 | Gate: 前置步骤已完成: define-operators | Parallelizable: No
[ ] TP-05 | P0 | 验证、审查与交付收口 | Verify: 核对验收项: required gates 全部 PASS；任务级 verification 绑定 clean HEAD、当前输入、策略和 artifact；未验证项与后续路径已记录 | Gate: 前置步骤已完成: materialize-library | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
