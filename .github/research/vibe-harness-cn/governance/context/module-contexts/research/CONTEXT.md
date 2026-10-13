---
id: CTX-RESEARCH
type: module-context
status: current
owner: engineering
created: 2026-08-14
last_reviewed: 2026-09-04
code_path: research
---

# 上游研究 Context

## 代码路径

`research`

## 模块职责

固定 15 个官方 Harness GitHub 输入的来源、revision、许可证、公开范围和研究限制。
沉淀逐仓源码级研究结论，供领域模型与治理控制面消费。

## 非职责

- 不把第三方源码 vendoring 到项目历史，也不把它们安装为产品运行依赖。
- 不执行上游仓库中的脚本、hooks、测试或嵌入式指令。
- 不用公开接口、插件或文档推断未公开的核心实现。

## 单一真相源

- 允许同步的来源定义：`research/upstreams.sources.json`。
- 精确 revision 与机器元数据：`research/upstreams.lock.json`。
- 人类可读的范围和限制：`research/UPSTREAMS.md`。
- 逐仓源码级研究结论：`research/HARNESS_RESEARCH.md`（revision 绑定，lock 变化后旧结论失效）。
- 跨学科方法与算子证据矩阵：`research/EXPANDED_OPERATOR_RESEARCH.md`（来源事实、迁移推断和未知项）。
- 上位问题求解方法论：`research/HEURISTIC_METACOGNITIVE_RESEARCH.md`（八类功能、母领域双轴、抽取规约和未知项）。
- 前六轮新增三十六个母领域的证据缺口：`research/DOMAIN_EVIDENCE_MATRIX.md`（前五轮三十个领域，加上线性代数谱方法、拓扑几何、电磁场方法、量子算子方法、溶液热力学相平衡和光谱结构解析）。
- 数学问题求解专项：`research/MATHEMATICAL_PROBLEM_SOLVING_RESEARCH.md`（55 项逐一 crosswalk、权威来源、证据等级和未验证项）。
- 可重跑同步入口：`scripts/sync_upstreams.sh`。

## 依赖边界

`scripts/sync_upstreams.sh` 只从 source registry 登记的官方 origin 写入被忽略 checkout 和 revision lock；领域文档与后续比较只读取这些输入，不修改上游。

## 常用验证

- `bash -n scripts/sync_upstreams.sh`
- `bash scripts/sync_upstreams.sh`
- `python3 -m json.tool research/upstreams.lock.json`

## Agent Rules

- Claude Code 官方仓库当前不含 CLI 核心实现；只能按公开扩展面做证据有限的比较。
- OpenHands 当前仓库是 Agent Canvas，不含独立 agent server 的核心实现。
- DeepSeek Harness 当前是 developer preview；公开核心源码不等价于稳定或生产就绪。
- Crush 当前是 FSL-1.1-MIT；Future License 不等价于当前 MIT。
- revision、许可证或源码可见性变化后，旧研究结论自动失效并必须重新审查。
