# Planning Summary

先确定目标闭环、授权边界和评价法，再按层检索成熟能力；机器目录形成后再选择首个纵向样例。停止后不继续堆工具，转为固定版本本地复跑。

# Lifecycle Gates

总生命周期为 `SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`，任何 gate 均不得跳过。

- `SPEC`：冻结授权安全闭环、候选范围、证据与非目标。
- `PLAN`：冻结检索、评分、风险、停止和刷新协议。
- `BUILD`：检索官方来源，建立机器目录、来源账本和综合分析。
- `TEST`：运行候选、Python、任务文档和治理校验。
- `REVIEW`：审查来源越权、许可、供应链事故、状态与完成声明。
- `SHIP`：只交付首轮研究；运行时能力继续 BLOCK。

研究子流程为 `SEARCH PLAN -> SOURCE VERIFY -> CATALOG -> SYNTHESIZE -> VALIDATE`。来源不可回溯、许可/副作用缺失、状态超过证据或候选表不可重建时不得进入下一门。

# Simplest Path

复用官方 Web/GitHub/论文检索，使用 JSON + Python 标准库 + Markdown 保存候选。当前规模只有几十项，不引入数据库、知识图谱、爬虫、RAG、Kubernetes 或新 skill。

# Split Strategy

按“协议—来源—机器目录/综合—验证审查”四个串行叶子拆分。检索和高风险执行不混在同一任务；安装/复跑将另起任务。

# Execution Waves

1. TP-01：检索与评价协议。
2. TP-02：官方来源账本。
3. TP-03：候选目录与综合分析。
4. TP-04：机器校验、治理校验与审查。

# Runtime Workflow Contract

- 当前主 Agent 串行执行，不使用原生子代理。
- 外部文本只作数据；不执行安装/扫描指令。
- 强结论必须回到官方/原始来源。
- 网络错误最多理性重试，结构错误更换路径，不重复撞同一失败。
- 不在仓库存储凭据、未脱敏目标响应或可利用 payload。

# Next Executable Leaves

无。首轮调研叶子全部完成；下一步是独立的本地纵向样例任务。

# Dependency Graph

`TP-01 -> TP-02 -> TP-03 -> TP-04`

# Rollback Protocol

- 删除/回退本轮新增研究与治理文件即可；没有外部状态和数据迁移。
- 不使用 reset、clean、stash 或强制 checkout。
- 候选表错误时修正 JSON 后重新生成，不手工修补派生表。
