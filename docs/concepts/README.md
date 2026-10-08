# 核心概念

## 字多不看

- 本目录解释 Vibe Coding 的核心概念，不承载工具安装细节。
- 先用问题求解定义任务，再用拼好码约束实现路径。
- 系统构建、开发范式、语言层要素和关键词系统用于提升工程判断。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| <a id="concept-problem-solving"></a>[问题求解](problem-solving.md) | 目标、现状、差距、标准、约束、对象与路径。 |
| <a id="concept-vibe-coding-state-transition"></a>[Vibe Coding 状态转移闭环](vibe-coding-state-transition.md) | 用固定目标、可变策略和分层反馈统一理解 Vibe Coding。 |
| <a id="concept-vibe-coding-cultivation-model"></a>[修仙解释图层](vibe-coding-cultivation-model.md) | 单树本体的通俗解释与任务战力评价。 |
| <a id="concept-cultivation-ontology-taxonomy"></a>[修仙领域统一本体与分类设计（V4 BFO 草案）](cultivation-ontology-taxonomy.md) | 固定 BFO 主干、领域稳定 ID、实体/品质与方法细分类、制备/再生证据链、功法JSON登记及四阶十二级。 |
| <a id="concept-glue-coding"></a>[拼好码](glue-coding.md) | 复用成熟能力，用胶水代码连接、编排、适配业务流程。 |
| <a id="concept-system-building"></a>[系统构建方法](system-building.md) | 自顶向下、自底向上与分而治之的组合使用。 |
| <a id="concept-development-paradigms"></a>[开发范式演进](development-paradigms.md) | 软件工程组织方式的演进。 |
| <a id="concept-language-layers"></a>[语言层要素](language-layers.md) | 看懂代码所需的语言层要素。 |
| <a id="concept-keyword-system"></a>[关键词系统](keyword-system.md) | Vibe Coding 与工程协作中的高频关键词。 |
| <a id="concept-recursive-self-optimizing-system"></a>[递归自优化系统](recursive-self-optimizing-system.md) | 递归自优化生成系统的形式化模型。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [问题求解](problem-solving.md) - 目标、现状、差距、标准、约束、对象与路径。
- [Vibe Coding 状态转移闭环](vibe-coding-state-transition.md) - 用固定目标、可变策略和分层反馈统一理解 Vibe Coding。
- [修仙解释图层](vibe-coding-cultivation-model.md) - 用同一分类理解模型、会话、方法、资源与任务评价。
- [修仙领域统一本体与分类设计（V4 BFO 草案）](cultivation-ontology-taxonomy.md) - BFO 原生继承、领域定义与稳定标识、实体/成员及物料关系、性质与读数、制备与施用、发育与再生、会话类外延与能力承载边界，以及功法收录/内容版本、JSON核心与四阶十二级词表。
- [拼好码](glue-coding.md) - 复用成熟能力，用胶水代码连接、编排、适配业务流程。
- [系统构建方法](system-building.md) - 自顶向下、自底向上与分而治之的组合使用。
- [开发范式演进](development-paradigms.md) - 软件工程组织方式的演进。
- [语言层要素](language-layers.md) - 看懂代码所需的语言层要素。
- [关键词系统](keyword-system.md) - Vibe Coding 与工程协作中的高频关键词。
- [递归自优化系统](recursive-self-optimizing-system.md) - 递归自优化生成系统的形式化模型。

</details>

## 使用方式

- 遇到模糊需求，先读问题求解，再读 [Vibe Coding 状态转移闭环](vibe-coding-state-transition.md) 建立目标基线、反馈和回退模型。
- 想了解修仙比喻与任务战力，可读 [修仙解释图层](vibe-coding-cultivation-model.md)。
- 想查看 BFO 下层展开和原著证据，可读 [统一本体设计草案](cultivation-ontology-taxonomy.md)；按词归类时查[领域定义与稳定标识](cultivation-ontology-taxonomy.md#领域类定义与稳定标识)。
- 登记功法或查品级，读[功法本体与品级](cultivation-ontology-taxonomy.md#功法本体与品级)；先分内容类型，再独立记录等级；当前收录与人工初评见JSON核心，暂定品级不当成实测效果。
- 细分修炼、身法、铭刻、授权或考核，查[下层判定边界](cultivation-ontology-taxonomy.md#下层展开的判定边界)和[传法到考核的证据链](cultivation-ontology-taxonomy.md#从传法到考核的证据链)。
- 原料、丹方、炼制、产物和服用如何区分，查[制备判据](cultivation-ontology-taxonomy.md#制备与施用的判定边界)及[实际证据链](cultivation-ontology-taxonomy.md#从原料到制备与施用)。
- 形状、尺寸、颜色、结构状态为何不等于读数/品阶，查[性质判据](cultivation-ontology-taxonomy.md#性质与观测的判定边界)及[观测证据链](cultivation-ontology-taxonomy.md#从性质到读数与评价)。
- 器灵或变化前后如何归类，查[器灵、化形与材料转化](cultivation-ontology-taxonomy.md#器灵化形与材料转化)，先区分意向、实际结果与身份。
- 已有结构成长、部件新生与整体身份，查[发育/再生判据](cultivation-ontology-taxonomy.md#发育再生与身份的判定边界)及[分层证据链](cultivation-ontology-taxonomy.md#从旧结构到新结构)。
- 准备技术实现，先读拼好码，确认是否已有成熟方案可复用。
- 需要统一提示词和工程词汇，读关键词系统。
- 需要提升长期工程判断，再读系统构建、开发范式和语言层要素。

## 正文

正文已拆分到上方独立文档；本 README 只保留索引、旧锚点兼容入口和阅读顺序。
