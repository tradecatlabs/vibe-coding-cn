# Execution Checklist
[x] TP-01.01 | P0 | Representation 表征研究 | Verify: 核对验收项: 记录表征改变如何缩小或重构问题空间 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.02 | P0 | Decomposition 分解研究 | Verify: 核对验收项: 记录子问题边界、依赖和合并证据 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.03 | P0 | Transformation 变换研究 | Verify: 核对验收项: 记录变换保持什么、损失什么和如何回译 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.04 | P0 | Search 搜索研究 | Verify: 核对验收项: 记录搜索预算、剪枝条件和回退路径 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.05 | P0 | Construction 构造研究 | Verify: 核对验收项: 记录候选产物、可运行见证和失败处理 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.06 | P0 | Verification/Falsification 验证证伪研究 | Verify: 核对验收项: 区分证明、证伪、验证、确认和 inconclusive | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.07 | P0 | Diagnosis/Revision 诊断修正研究 | Verify: 核对验收项: 记录最小失败案例、首个失效点和回归证据 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-01.08 | P0 | Control/Metacognition 控制元认知研究 | Verify: 核对验收项: 记录何时继续、停止、换路和升级人工 | Gate: 父步骤范围已确认: research-evidence | Parallelizable: No
[x] TP-02 | P0 | 提炼母领域算子与双轴分类 | Verify: 检查新增条目的 kind、语义、来源、主类/辅助类、治理 owner、失败和恢复 | Gate: 新增方法不把母领域事实写成权限，不引入重复或无法验证的空壳条目 | Parallelizable: No
[x] TP-03 | P0 | 入库并同步交叉索引与文档 | Verify: 运行 JSON/引用/计数检查并核对文档规模、双轴边界和未验证项 | Gate: catalog、inventory、packs、taxonomy 与文档没有漂移或悬空引用 | Parallelizable: No
[x] TP-04 | P0 | 验证、审查与交付收口 | Verify: 运行 operator self-test、项目 gates、治理 strict/health/principle 和 task closeout validators | Gate: required gate 绑定当前输入、策略和真实产物；失败必须 fail-closed | Parallelizable: No

说明：
- 每一行后续必须绑定 `TP-XX(.YY...)`
- 不允许出现无归属 TODO
