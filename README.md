<!--
-------------------------------------------------------------------------------
  项目头部区域 (HEADER)
-------------------------------------------------------------------------------
-->
<div align="center">

<a id="vibe-coding-指南"></a>

# vibe-coding-cn：非严肃开发的 Vibe Coding 工具箱

**以 Pi Agent 与 OpenAI GPT 为实现基座，整合并编排可见层中既有的 Context、Skills 与 Extensions 组件，构建高可用系统。**

<!--
  徽章区域 (BADGES)
-->
<!-- 单一徽章行：紧凑标签，原链接与完整说明保留在href/alt。 -->
<p>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/tukuaiai/vibe-coding-cn?label=%E8%AE%B8%E5%8F%AF%E8%AF%81&style=flat" alt="许可证"></a>
  <a href="https://t.me/glue_coding"><img src="https://img.shields.io/badge/交流-Telegram-blue?style=flat&logo=telegram" alt="交流群"></a>
  <a href=".github/context/gongfa/README.md#原文文集"><img src="https://img.shields.io/badge/功法-体系-slateblue?style=flat" alt="功法体系：思想、准则、方法与流程"></a>
  <a href=".github/context/research/README.md"><img src="https://img.shields.io/badge/研究-证据-teal?style=flat" alt="研究事实与证据"></a>
  <a href=".github/context/getting-started/learning-map.md"><img src="https://img.shields.io/badge/入门-教程-red?style=flat" alt="Pi CLI 安装配置提示词：供网页版 AI 单步引导"></a>
  <a href=".github/skills/README.md#当前保留"><img src="https://img.shields.io/badge/Skills-技能-forestgreen?style=flat" alt="skills技能大全"></a>
  <a href=".github/context/prompts/README.md#在线提示词库"><img src="https://img.shields.io/badge/提示词-表格-blue?style=flat" alt="提示词在线表格"></a>
  <a href=".github/context/assets/README.md#外部资源本地注册表"><img src="https://img.shields.io/badge/资源-索引-teal?style=flat" alt="外部资源本地注册表"></a>
  <a href="https://github.com/tukuaiai/vibe-coding-cn/wiki"><img src="https://img.shields.io/badge/Wiki-导航-slateblue?style=flat" alt="Wiki 导航入口"></a>
  <a href=".github/context/gongfa/README.md#全部记录"><img src="https://img.shields.io/badge/功法-总表-purple?style=flat" alt="功法总表"></a>
  <a href=".github/context/gongfa/data.json"><img src="https://img.shields.io/badge/JSON-原始资料-forestgreen?style=flat" alt="功法JSON原始资料；历史Excel保留为载荷，不是活动视图"></a>
  <a href="https://zread.ai/tukuaiai/vibe-coding-cn/1-overview"><img src="https://img.shields.io/badge/Zread-AI解读-blue?style=flat" alt="zread.ai/tukuaiai/vibe-coding-cn"></a>
</p>

</div>

<a id="ai-six-propositions"></a>
<a id="ai-five-propositions"></a>
<a id="ai-three-propositions"></a>
<a id="六条核心命题"></a>

<a id="root-tldr"></a>

<details>
<summary><strong>📌 字多不看</strong></summary>

## 📌 字多不看

`vibe-coding-cn` 是以 Pi Agent 与已授权 OpenAI GPT 为基础的中文 Vibe Coding 工具箱；[Context](.github/context/README.md)、[Skills](.github/skills/README.md) 和 [Extensions](.github/extensions/README.md) 按任务取用。

<a id="getting-started"></a>

### 🚀 从零开始

1. **安装并验证 Pi：** 将[Pi CLI 上手提示词](.github/context/getting-started/learning-map.md)全文复制给网页版 Chat AI，按步骤完成本机安装、模型配置和 Agent 能力验证。
2. **第一次项目练习（可选）：** 跟着[第一个项目教程](.github/context/getting-started/first-project.md)，完成一个本地待办清单。

</details>

<a id="gongfa"></a>
<!-- 其他方法历史定位收口到功法；六命题旧锚点仅作兼容，正文入口在功法体系。 -->
<a id="dao-fa-shu-qi"></a>
<a id="tools"></a>
<a id="经验"></a>
<a id="实验性方法"></a>
<a id="道法术器"></a>
<a id="修仙解释图层"></a>

<details>
<summary><strong>📚 功法体系</strong></summary>

## 功法体系

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | 功法体系。本区块说明的是一组可复用内容，不对应单一功法。 |
| 2 | 是什么 | 统一导航思想、准则、思维模型、方法与工程流程；经验、道法术器、实验性方法和哲学作为同一集合中的原始文集保留。 |
| 3 | 为什么 | 让读者按当前问题选用适用内容，避免从首页分散的旧栏目或独立分库中查找。 |
| 4 | 怎么做 | 先明确当前任务的问题，再从[功法体系目录](.github/context/gongfa/README.md)选择文集或条目；具体用法以条目说明和来源为准。 |
| 5 | 扩展 | 需要继续阅读时进入相应原始文集；文集归并本身不创建新的功法身份或登记条目。 |
| 6 | 关联信息 | [工具解释模板 v0](.github/context/assets/templates/tool-explanation-template-v0.md)规定说明结构；具体类型和边界见[功法体系目录](.github/context/gongfa/README.md)。 |
| 7 | 出处 | [功法原始资料](.github/context/gongfa/data.json)记录逐条身份、内容版本、冻结来源与已有意见；[生成总表](.github/context/gongfa/README.md#全部记录)用于浏览。 |
| 8 | 相关图书 | 本区块未列集合级书目；具体书目须按对应条目的来源核实，未核实前不补列。 |
| 9 | 它要解决什么问题？ | 帮助读者从统一入口按任务找到可参考的思想和方法；集合本身不是单一问题求解器，具体问题由各条目说明。 |
| 10 | 为什么这样设计？ | 把既有内容保留在同一集合中，既维持原文可追溯，也不恢复经验、道法术器、实验性方法和哲学的首页独立栏目或分库入口。 |
| 11 | 内部如何实现？ | 以`data.json`为唯一维护数据，由生成器输出轻量README导航页和天、地、玄、黄四阶正文；逐条身份、内容版本和来源绑定仍按原登记记录维护。 |
| 12 | 付出了什么代价？ | 现有总览没有集合级成本测量；不能据此认定维护或应用成本为零，具体限制以各条目来源为准。 |
| 13 | 比较不同技术与方法。 | 应在同一问题和适用条件下比较具体条目；不同任务中的效果或品级不能直接互比。 |
| 14 | 提炼共同规律。 | 当前可归纳的共同做法是先看问题，再选择方法；不把目录归类或已有初评当作统一效果证明。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 选择依赖具体任务和条目的适用条件、限制；文集归并不等于全部内容已经逐条登记，已有初评也不等于正式效果验证。 |
| 16 | 结论 | 当前登记411项逐对象说明；每项结论仅在相应对象身份和第15项条件内成立，不合并为全集合的统一效果或正式评级主张。 |
| 17 | 连接规则 | 说明载荷按对象身份把第15项边界、第16项结论和第18项依据绑定在同一记录中；因此集合层只能汇总记录范围，不能跨条目拼接局部推理推出普遍效果。 |
| 18 | 依据 | 逐项事实依据与边界由唯一[功法数据源](.github/context/gongfa/data.json)第18项维护，浏览见[生成总表](.github/context/gongfa/README.md#全部记录)；本集合摘要不复写或替代对象级依据。 |

</details>

<a id="faqi"></a>
<details>
<summary><strong>🧰 法器体系</strong></summary>

## 法器体系

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | 法器体系。本区块说明工具、入口和依赖的集合，不对应单一产品。 |
| 2 | 是什么 | 整理 Vibe Coding 流程中使用或依赖的工具、可调用入口和依赖类别；固定来源实现、当前运行实例、候选对象与抽象类别分别记录。 |
| 3 | 为什么 | 帮助读者理解各对象在 Vibe Coding 工作流中的位置；重要性分级不代表实现质量、运行状态或任务效果。 |
| 4 | 怎么做 | 先明确任务，再核实具体对象的来源、版本、可用性和权限；选用流程见[法器体系说明](.github/context/faqi/README.md#doc-faqi-system)。 |
| 5 | 扩展 | 新增或延伸说明须先明确对象身份和来源；抽象依赖类别不自动代表具体产品、部署或已启用能力。 |
| 6 | 关联信息 | [工具解释模板 v0](.github/context/assets/templates/tool-explanation-template-v0.md)、[法器体系说明](.github/context/faqi/README.md#doc-faqi-system)（分类、重要性、选用方式与固定 MCP 源码副作用边界）及[法器类型与正式效能规约](.github/context/gongfa/README.md#doc-cultivation-ontology-taxonomy-法器品级规约)。 |
| 7 | 出处 | [法器登记源](.github/context/faqi/data.json)是唯一可编辑数据源；[法器重要性总表](.github/context/faqi/README.md#法器总表)是生成视图。固定来源和选区按登记记录核对，不据此推断当前运行。 |
| 8 | 相关图书 | 本区块未列集合级书目；具体书目须按对应对象的来源核实，未核实前不补列。 |
| 9 | 它要解决什么问题？ | 帮助读者识别 Vibe Coding 工作流中的工具角色、可调用入口和依赖类别；它不是某个工具，也不保证对象当前可用。 |
| 10 | 为什么这样设计？ | 将固定来源实现、运行实例、候选对象和抽象类别分开记录，避免把来源、依赖关系或名称相似误当成同一对象。 |
| 11 | 内部如何实现？ | 登记数据生成浏览总表；具体实现机制须根据各对象对应的固定来源、版本和选区说明，不能从集合摘要推断。 |
| 12 | 付出了什么代价？ | 本区块没有集合级成本或效能测量；具体资源代价和副作用须按对象来源核实。文件级许可线索仅作支持证据，不等于许可批准或再分发授权。 |
| 13 | 比较不同技术与方法。 | 30 项分级比较的是 Vibe Coding 重要性，不是质量或效能；方案比较须限定同一任务、对象层级和适用条件。 |
| 14 | 提炼共同规律。 | 应分别核对对象身份、重要性、当前运行状态、许可和效果证据；其中一项不能替代其他项。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 当前 30 项按重要性暂分天阶 4 项、地阶 12 项、玄阶 9 项、黄阶 5 项；重要性不代表实现质量、运行可用性或效能验证。正式效能量表仍为草案，评级尚未完成。 |
| 16 | 结论 | 当前登记30项对象说明；每项结论只覆盖其固定来源和第15项条件，不把重要性分级解释为当前可用、有效或获许可。 |
| 17 | 连接规则 | 重要性分级只记录对象在项目中的相对角色，静态来源选区只记录固定版本范围；两者都不是目标环境的安装、运行、效果或许可证据，故不能推出这些状态。 |
| 18 | 依据 | 每项的来源、版本、选区与边界由唯一[法器数据源](.github/context/faqi/data.json)第18项维护，浏览见[法器总表](.github/context/faqi/README.md#法器总表)；本集合摘要不代替对象级依据。 |

</details>



<div align="center">

---

## Star History

<a href="https://www.star-history.com/#tukuaiai/vibe-coding-cn&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=tukuaiai/vibe-coding-cn&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=tukuaiai/vibe-coding-cn&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=tukuaiai/vibe-coding-cn&type=date&legend=top-left" />
 </picture>
</a>

[⬆ 返回顶部](#vibe-coding-指南)

**如果这个项目对您有帮助，请考虑为其点亮一颗 Star ⭐！**
</div>
