# docs 目录

`docs/` 保存领域研究和目标架构，只解释稳定概念与决策依据，不复制机器契约。

```text
docs/
├── AGENTS.md                                      # 本目录边界
├── HARNESS_MODEL.md                               # Harness 定义、控制面边界与路线图
├── OPERATOR_SPEC.md                               # 宽松 Core Contract、Profile 与扩展规则
└── PROBLEM_SOLVING_OPERATOR_ARCHITECTURE_PRD.md   # Harness 内算子库的需求、语义边界与验收基线
```

上游是用户目标和一手资料；下游是 `contracts/`、ADR 和实现任务。字段级约束必须落到
Schema，长期项目决策必须落到 `governance/`。

`HARNESS_MODEL.md` 是元 Harness 总体领域模型；PSOA PRD 是 Harness 内问题求解算子库的需求真相源。
两者只描述已经确认的语义或显式标注的目标需求，不把规划中的能力写成已实现事实。

## 近期变更

- 2026-09-03：将 Operator Library 明确归入 Harness，并区分共享规范、本地库存、Binding 与治理目录。
- 2026-09-03：记录 196 个跨学科原始条目、20 个派生 Method、Operator Pack Schema 与离线 conformance
  已实现；selector、Binding、运行态证据和互操作 proof 仍未实现。
- 2026-09-03：新增 Operator Spec；公共契约只约束稳定结构，完整内容与 196+20 基线由显式 Profile 加严，
  并以 taxonomy 双轴区分母领域与八类功能。
- 2026-09-03：继续加入十二个母领域，当前参考库为 256 个原始条目、32 个派生 Method；第二轮新增法律、伦理、教育、语言、历史和社会科学，证据矩阵和迁移边界
  见 `research/DOMAIN_EVIDENCE_MATRIX.md`，运行时能力仍未实现。
- 2026-09-03：第三轮新增形式逻辑与自动推理、哲学与科学认识论、地球科学、天文学与天体物理、材料科学、信息与知识科学六个母领域；当前参考库为 286 个原始条目、38 个派生 Method，运行时能力仍未实现。
- 2026-09-03：第四轮新增控制论、数值分析与科学计算、离散组合数学、热力学与统计物理、有机化学反应设计、分析化学与计量学六个母领域；当前参考库为 316 个原始条目、44 个派生 Method，运行时能力仍未实现。
- 2026-09-03：第五轮新增随机过程、微分方程与动力系统、经典力学与变分方法、流体与连续介质、物理化学与化学动力学、电化学与传质六个母领域；当前参考库为 346 个原始条目、50 个派生 Method，运行时能力仍未实现。
- 2026-09-04：第六轮新增线性代数谱方法、拓扑几何、电磁场方法、量子算子方法、溶液热力学相平衡和光谱结构解析；该轮参考库达到 376 个原始条目、56 个派生 Method，运行时能力仍未实现。
- 2026-09-04：数学专项将 55 个问题求解方法逐项 crosswalk，复用 20 项并新增 35 个 source 与 1 个 derived；当前参考库为 411 个原始条目、57 个派生 Method，公共 Core 与运行时边界不变。
- 2026-09-04：新增宽松 Operator Runtime Core 与无副作用参考 Harness，证明 Selector、Binding、
  三类 Spec 物化、独立摘要验证和最小披露 Trace；真实执行、第二 Binding 和生产 eval 仍未实现。
