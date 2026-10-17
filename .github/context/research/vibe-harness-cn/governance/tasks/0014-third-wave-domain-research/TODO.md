# Execution Checklist
[x] TP-01.01 | P0 | 形式逻辑与自动推理研究 | Verify: 核对验收项: 形成可追溯的规格、子目标、反模型和内核证据程序 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.02 | P0 | 哲学与科学认识论研究 | Verify: 核对验收项: 保留观察、推断、辅助假设和未决分支的边界 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.03 | P0 | 地球科学与地学研究 | Verify: 核对验收项: 结论绑定观测、尺度、校准、质量平衡和验证条件 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.04 | P0 | 天文学与天体物理研究 | Verify: 核对验收项: 保留仪器、背景、模型、尺度和独立确认的不确定性 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.05 | P0 | 材料科学研究 | Verify: 核对验收项: 形成从加工变量到结构、性能和校准证据的受限链条 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.06 | P0 | 信息与知识科学研究 | Verify: 核对验收项: 区分检索相关性、来源权威、完整性、公平性和事实正确性 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-02 | P0 | 既有库缺口与重复审计 | Verify: 核对验收项: 每个候选有 add/crosswalk/gap 决策；不因追求数量重复登记同义条目 | Gate: 前置步骤已完成: research-evidence | Parallelizable: No
[x] TP-03 | P0 | 提炼新增算子与组合 Method | Verify: 核对验收项: 新增 source 有来源和功能主类；治理字段保持 harness_policy、verifier、reference_only；derived Method 只引用已登记条目 | Gate: 前置步骤已完成: gap-audit | Parallelizable: No
[x] TP-04 | P0 | 入库并同步目录文档 | Verify: 核对验收项: source inventory、pack 和 catalog 精确一致；所有受影响 source-of-truth 已更新或记录具体豁免 | Gate: 前置步骤已完成: define-operators | Parallelizable: No
[ ] TP-05 | P0 | 验证、审查与交付收口 | Verify: 核对验收项: required gates 全部 PASS；任务级 verification 绑定当前输入、策略和真实 artifact；未验证项与后续路径已记录 | Gate: 前置步骤已完成: materialize-library | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
