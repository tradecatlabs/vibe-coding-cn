<!-- generated: sync-faqi-catalog.py -->
# Vibe Coding法器重要性总表：玄阶

本页包含9项玄阶对象。分级仅表示重要性暂定，不代表效能验证。
- [返回总索引](README.md)；其他阶：[天阶](tian.md)、[地阶](di.md)、[黄阶](huang.md)

## 玄阶对象

- [7.1 Git托管、CI Runner与CI/CD平台](#v0-faqi-dep-category-ci-platform-e3564493)
- [2.3 检索/索引/记忆与向量库](#v0-faqi-dep-category-retrieval-memory-da201109)
- [7.2-7.3 制品注册表、部署目标、产品运行时、数据库与外部API](#v0-faqi-dep-category-deployment-data-35c30956)
- [auto-skill模板生成脚本](#v0-faqi-faqi-auto-skill-create-ffe7ec4d)
- [auto-skill结构校验脚本](#v0-faqi-faqi-auto-skill-validate-5244b18f)
- [Skill Seekers程序](#v0-faqi-faqi-skill-seekers-cc1f7ed8)
- [官方Skill初始化脚本](#v0-faqi-faqi-claude-skill-init-3a642a5d)
- [Codex配置安装与恢复脚本](#v0-faqi-faqi-codex-config-installer-2dcddf43)
- [Skill Seekers本地运行适配脚本](#v0-faqi-faqi-skill-seekers-adapter-eb5e7e6f)

<a id="v0-faqi-dep-category-ci-platform-e3564493"></a>
### 7.1 Git托管、CI Runner与CI/CD平台

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | 7.1 Git托管、CI Runner与CI/CD平台 |
| 2 | 是什么 | 依赖图将其作为抽象依赖类别登记：7.1 Git托管、CI Runner与CI/CD平台；纳入依据：用户确认此依赖类别已核并要求纳入；托管服务、Runner执行环境与CI/CD平台分开分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。 |
| 3 | 为什么 | 待核：抽象类别的纳入依据已记录，但没有具体采用动机；不把范围理由改写成产品用途。 |
| 4 | 怎么做 | 不适用：本条是抽象依赖类别，不指定唯一可执行产品、安装步骤或操作流程；具体实现需另行识别。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖类别ID=dep-category-ci-platform；类别节点=7.1 Git托管、CI Runner与CI/CD平台；纳入状态=user&#95;confirmed&#95;in&#95;scope。这是抽象类别，不是具体产品或运行实例。<br>Vibe Coding 重要性暂定：玄阶高级（grade&#95;id=faqi-xuan-advanced；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：自动化验证、协作与持续交付；分级依据：把代码生成接入可重复测试、审查和协作交付，显著扩展可靠使用范围；本地闭环可运行但难以替代团队级持续验证。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖类别来源与登记记录：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>类别登记：{<br>  "id": "dep-category-ci-platform",<br>  "node": "7.1 Git托管、CI Runner与CI/CD平台",<br>  "disposition": "user&#95;confirmed&#95;in&#95;scope",<br>  "reason": "用户确认此依赖类别已核并要求纳入；托管服务、Runner执行环境与CI/CD平台分开分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-category-ci-platform",<br>  "grade&#95;id": "faqi-xuan-advanced",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：自动化验证、协作与持续交付",<br>  "basis": "把代码生成接入可重复测试、审查和协作交付，显著扩展可靠使用范围；本地闭环可运行但难以替代团队级持续验证。"<br>}<br>类别纳入状态仅表示范围登记，不指向已部署的具体产品。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 不适用：该条是类别节点而非具名实现，当前材料不能支持具体设计选择解释。 |
| 11 | 内部如何实现？ | 不适用：抽象类别没有单一内部实现；不得以任一供应商/实现代表整个类别。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 类别依据（原记录）：用户确认此依赖类别已核并要求纳入；托管服务、Runner执行环境与CI/CD平台分开分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。<br>纳入状态：user&#95;confirmed&#95;in&#95;scope；类别不是具体实现或部署。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-category-retrieval-memory-da201109"></a>
### 2.3 检索/索引/记忆与向量库

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | 2.3 检索/索引/记忆与向量库 |
| 2 | 是什么 | 依赖图将其作为抽象依赖类别登记：2.3 检索/索引/记忆与向量库；纳入依据：用户确认此可选依赖类别已核并要求纳入；检索过程、索引、记忆内容与向量存储分别分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。 |
| 3 | 为什么 | 待核：抽象类别的纳入依据已记录，但没有具体采用动机；不把范围理由改写成产品用途。 |
| 4 | 怎么做 | 不适用：本条是抽象依赖类别，不指定唯一可执行产品、安装步骤或操作流程；具体实现需另行识别。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖类别ID=dep-category-retrieval-memory；类别节点=2.3 检索/索引/记忆与向量库；纳入状态=user&#95;confirmed&#95;in&#95;scope。这是抽象类别，不是具体产品或运行实例。<br>Vibe Coding 重要性暂定：玄阶高级（grade&#95;id=faqi-xuan-advanced；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：长程上下文、知识检索与记忆；分级依据：支撑跨文件和长任务上下文保持、历史知识复用，提升复杂任务可处理范围；短任务仍可不依赖，且实现可替换。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖类别来源与登记记录：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>类别登记：{<br>  "id": "dep-category-retrieval-memory",<br>  "node": "2.3 检索/索引/记忆与向量库",<br>  "disposition": "user&#95;confirmed&#95;in&#95;scope",<br>  "reason": "用户确认此可选依赖类别已核并要求纳入；检索过程、索引、记忆内容与向量存储分别分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-category-retrieval-memory",<br>  "grade&#95;id": "faqi-xuan-advanced",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：长程上下文、知识检索与记忆",<br>  "basis": "支撑跨文件和长任务上下文保持、历史知识复用，提升复杂任务可处理范围；短任务仍可不依赖，且实现可替换。"<br>}<br>类别纳入状态仅表示范围登记，不指向已部署的具体产品。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 不适用：该条是类别节点而非具名实现，当前材料不能支持具体设计选择解释。 |
| 11 | 内部如何实现？ | 不适用：抽象类别没有单一内部实现；不得以任一供应商/实现代表整个类别。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 类别依据（原记录）：用户确认此可选依赖类别已核并要求纳入；检索过程、索引、记忆内容与向量存储分别分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。<br>纳入状态：user&#95;confirmed&#95;in&#95;scope；类别不是具体实现或部署。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-category-deployment-data-35c30956"></a>
### 7.2-7.3 制品注册表、部署目标、产品运行时、数据库与外部API

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | 7.2-7.3 制品注册表、部署目标、产品运行时、数据库与外部API |
| 2 | 是什么 | 依赖图将其作为抽象依赖类别登记：7.2-7.3 制品注册表、部署目标、产品运行时、数据库与外部API；纳入依据：用户确认此可选依赖类别已核并要求纳入；注册表、部署环境、运行时、数据库与外部API分别分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。 |
| 3 | 为什么 | 待核：抽象类别的纳入依据已记录，但没有具体采用动机；不把范围理由改写成产品用途。 |
| 4 | 怎么做 | 不适用：本条是抽象依赖类别，不指定唯一可执行产品、安装步骤或操作流程；具体实现需另行识别。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖类别ID=dep-category-deployment-data；类别节点=7.2-7.3 制品注册表、部署目标、产品运行时、数据库与外部API；纳入状态=user&#95;confirmed&#95;in&#95;scope。这是抽象类别，不是具体产品或运行实例。<br>Vibe Coding 重要性暂定：玄阶中级（grade&#95;id=faqi-xuan-intermediate；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：从代码到产品运行与外部集成；分级依据：支撑部署、数据库和API集成，使代码进入真实产品场景；并非每次编码必需，故属于重要交付扩展而非核心生成。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖类别来源与登记记录：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>类别登记：{<br>  "id": "dep-category-deployment-data",<br>  "node": "7.2-7.3 制品注册表、部署目标、产品运行时、数据库与外部API",<br>  "disposition": "user&#95;confirmed&#95;in&#95;scope",<br>  "reason": "用户确认此可选依赖类别已核并要求纳入；注册表、部署环境、运行时、数据库与外部API分别分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-category-deployment-data",<br>  "grade&#95;id": "faqi-xuan-intermediate",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：从代码到产品运行与外部集成",<br>  "basis": "支撑部署、数据库和API集成，使代码进入真实产品场景；并非每次编码必需，故属于重要交付扩展而非核心生成。"<br>}<br>类别纳入状态仅表示范围登记，不指向已部署的具体产品。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 不适用：该条是类别节点而非具名实现，当前材料不能支持具体设计选择解释。 |
| 11 | 内部如何实现？ | 不适用：抽象类别没有单一内部实现；不得以任一供应商/实现代表整个类别。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 类别依据（原记录）：用户确认此可选依赖类别已核并要求纳入；注册表、部署环境、运行时、数据库与外部API分别分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。<br>纳入状态：user&#95;confirmed&#95;in&#95;scope；类别不是具体实现或部署。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-faqi-auto-skill-create-ffe7ec4d"></a>
### auto-skill模板生成脚本

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | auto-skill模板生成脚本 |
| 2 | 是什么 | 现有登记将其界定为软件工件：指渲染Skill模板与建立目录的程序，不是生成出的Skill内容或整个元技能。--force可覆盖目标，未执行。<br>此处复述登记边界，不证明当前可安装、可运行或有效。 |
| 3 | 为什么 | 待核：未记录为何采用该程序/配置；重要性范围与分级依据不等于采用动机。 |
| 4 | 怎么做 | 待核：登记冻结了源码选区，但没有验证该对象当前完整的调用方式、输入输出与安全前提；选区本身不是操作手册。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 法器对象ID=faqi-auto-skill-create；本体类型=software-artifact；版本声明=未声明；本地入口=.github/skills/auto-skill；当前运行实例/部署状态未在对象记录中声明。<br>Vibe Coding 重要性暂定：玄阶中级（grade&#95;id=faqi-xuan-intermediate；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：技能资产扩展与复用；分级依据：把操作知识封装为可复用Agent技能，能扩展后续任务能力；属于增益支路，不是最小编码闭环的必需组件。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。<br>来源ID：S08, S07。 |
| 7 | 出处 | 固定实现/佐证来源记录：{<br>  "id": "S08",<br>  "purpose": "implementation",<br>  "path": ".github/skills/auto-skill/scripts/create-skill.sh",<br>  "repository": ".",<br>  "revision": "0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2",<br>  "sha256": "3eb16d2f24cc2af3e7d7a0f4175e06b0258504795d079ba0920be9dd75f2f7fc",<br>  "lines": &#91;<br>    80,<br>    182<br>  &#93;,<br>  "selection&#95;sha256": "e769660515ada48debbd022fdfb85ec934b4d3413cf3501e06ef075b6d36b1a4"<br>}；{<br>  "id": "S07",<br>  "purpose": "support",<br>  "path": ".github/skills/auto-skill/README.md",<br>  "repository": ".",<br>  "revision": "0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2",<br>  "sha256": "2fd869316c0469d9c4079cd9a19c41698b501bca6ddd2b6cc03617e3f96218f0",<br>  "lines": &#91;<br>    1,<br>    21<br>  &#93;,<br>  "selection&#95;sha256": "2fd869316c0469d9c4079cd9a19c41698b501bca6ddd2b6cc03617e3f96218f0"<br>}<br>本地入口记录：{<br>  "path": ".github/skills/auto-skill",<br>  "objects": &#91;<br>    "faqi-auto-skill-create",<br>    "faqi-auto-skill-validate",<br>    "faqi-skill-seekers-adapter"<br>  &#93;,<br>  "sources": &#91;<br>    "S07",<br>    "S08",<br>    "S09",<br>    "S10"<br>  &#93;,<br>  "boundary": "Skill说明/规约与三个独立入口脚本分离，不把整Skill包登记成一件软件。",<br>  "pending": &#91;<br>    "其他辅助模块未逐模块登记，不能将本次选区称为全包能力审查。"<br>  &#93;<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "faqi-auto-skill-create",<br>  "grade&#95;id": "faqi-xuan-intermediate",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：技能资产扩展与复用",<br>  "basis": "把操作知识封装为可复用Agent技能，能扩展后续任务能力；属于增益支路，不是最小编码闭环的必需组件。"<br>}<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：登记未记录设计者为何选择该结构/接口/依赖；不能从被登记为重要推断其设计意图。 |
| 11 | 内部如何实现？ | 待核：当前仅有固定源码选区及SHA登记；尚未沿调用者、数据流、状态与失败路径完成实现链分析。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 登记边界（原字段）：指渲染Skill模板与建立目录的程序，不是生成出的Skill内容或整个元技能。--force可覆盖目标，未执行。<br>重要性纳入范围：Vibe Coding重要性：技能资产扩展与复用<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。<br>待核：具体操作系统、依赖版本、权限、输入规模和部署配置须按实际来源及工作负载核验。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-faqi-auto-skill-validate-5244b18f"></a>
### auto-skill结构校验脚本

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | auto-skill结构校验脚本 |
| 2 | 是什么 | 现有登记将其界定为软件工件：指frontmatter和结构校验程序；成功结构检查不证明Skill语义、执行正确或效果。<br>此处复述登记边界，不证明当前可安装、可运行或有效。 |
| 3 | 为什么 | 待核：未记录为何采用该程序/配置；重要性范围与分级依据不等于采用动机。 |
| 4 | 怎么做 | 待核：登记冻结了源码选区，但没有验证该对象当前完整的调用方式、输入输出与安全前提；选区本身不是操作手册。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 法器对象ID=faqi-auto-skill-validate；本体类型=software-artifact；版本声明=未声明；本地入口=.github/skills/auto-skill；当前运行实例/部署状态未在对象记录中声明。<br>Vibe Coding 重要性暂定：玄阶中级（grade&#95;id=faqi-xuan-intermediate；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：技能资产质量与可载入性；分级依据：降低扩展技能结构错误造成的接入阻断；不判断语义正确性，属于能力扩展的质量辅助。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。<br>来源ID：S09, S07。 |
| 7 | 出处 | 固定实现/佐证来源记录：{<br>  "id": "S09",<br>  "purpose": "implementation",<br>  "path": ".github/skills/auto-skill/scripts/validate-skill.sh",<br>  "repository": ".",<br>  "revision": "0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2",<br>  "sha256": "deb5cf2529a93c87c8b7323b55ffc6d7798e6b59652351ba795340ac8c0061c9",<br>  "lines": &#91;<br>    67,<br>    160<br>  &#93;,<br>  "selection&#95;sha256": "dbd460af6a32307709a11281c7b90925b9fd9820128eb04881c80c020a99f0dc"<br>}；{<br>  "id": "S07",<br>  "purpose": "support",<br>  "path": ".github/skills/auto-skill/README.md",<br>  "repository": ".",<br>  "revision": "0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2",<br>  "sha256": "2fd869316c0469d9c4079cd9a19c41698b501bca6ddd2b6cc03617e3f96218f0",<br>  "lines": &#91;<br>    1,<br>    21<br>  &#93;,<br>  "selection&#95;sha256": "2fd869316c0469d9c4079cd9a19c41698b501bca6ddd2b6cc03617e3f96218f0"<br>}<br>本地入口记录：{<br>  "path": ".github/skills/auto-skill",<br>  "objects": &#91;<br>    "faqi-auto-skill-create",<br>    "faqi-auto-skill-validate",<br>    "faqi-skill-seekers-adapter"<br>  &#93;,<br>  "sources": &#91;<br>    "S07",<br>    "S08",<br>    "S09",<br>    "S10"<br>  &#93;,<br>  "boundary": "Skill说明/规约与三个独立入口脚本分离，不把整Skill包登记成一件软件。",<br>  "pending": &#91;<br>    "其他辅助模块未逐模块登记，不能将本次选区称为全包能力审查。"<br>  &#93;<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "faqi-auto-skill-validate",<br>  "grade&#95;id": "faqi-xuan-intermediate",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：技能资产质量与可载入性",<br>  "basis": "降低扩展技能结构错误造成的接入阻断；不判断语义正确性，属于能力扩展的质量辅助。"<br>}<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：登记未记录设计者为何选择该结构/接口/依赖；不能从被登记为重要推断其设计意图。 |
| 11 | 内部如何实现？ | 待核：当前仅有固定源码选区及SHA登记；尚未沿调用者、数据流、状态与失败路径完成实现链分析。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 登记边界（原字段）：指frontmatter和结构校验程序；成功结构检查不证明Skill语义、执行正确或效果。<br>重要性纳入范围：Vibe Coding重要性：技能资产质量与可载入性<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。<br>待核：具体操作系统、依赖版本、权限、输入规模和部署配置须按实际来源及工作负载核验。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-faqi-skill-seekers-cc1f7ed8"></a>
### Skill Seekers程序

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | Skill Seekers程序 |
| 2 | 是什么 | 现有登记将其界定为软件工件：指固定submodule修订的软件实现；多个CLI入口及可选MCP模块不机械复制产品身份。3.5.1仅为pyproject源码声明，不是已核发布或运行版。MCP头注释34项与静态40个装饰函数、health返回2.1.1均不作为运行清单或身份版本证明。<br>此处复述登记边界，不证明当前可安装、可运行或有效。 |
| 3 | 为什么 | 待核：未记录为何采用该程序/配置；重要性范围与分级依据不等于采用动机。 |
| 4 | 怎么做 | 待核：登记冻结了源码选区，但没有验证该对象当前完整的调用方式、输入输出与安全前提；选区本身不是操作手册。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 法器对象ID=faqi-skill-seekers；本体类型=software-artifact；版本声明=3.5.1（仅源码声明）；本地入口=.github/tools/external/Skill&#95;Seekers-development；当前运行实例/部署状态未在对象记录中声明。；当前资源关联ID=repo-rules-scaffolds-skills-cd973130（关联不等于许可或运行证明）。<br>Vibe Coding 重要性暂定：玄阶中级（grade&#95;id=faqi-xuan-intermediate；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：外部知识转可复用技能；分级依据：增加Agent可复用的领域能力和上下文资产；需特定工作流，不能替代通用推理与工具执行。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。<br>关联资源ID：repo-rules-scaffolds-skills-cd973130。资源链接/本地关联不证明许可、兼容性或功能等价。<br>来源ID：S16, S14, S15, S42, S44, S45, S46, S47, S48, S49, S50, S66, S67, S68, S69, S70, S71, S72, S73。 |
| 7 | 出处 | 固定实现/佐证来源记录：{<br>  "id": "S16",<br>  "purpose": "implementation",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/cli/main.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "8c02660dacd304f51fe8c4a9685d3f6d5324a7eef7779b6baa7325827bf01985",<br>  "lines": &#91;<br>    39,<br>    116<br>  &#93;,<br>  "selection&#95;sha256": "60fba27fbe444499a1e95b5dc69edc8b0d34d6c26a30039dcbf9d9205ffdfb14"<br>}；{<br>  "id": "S14",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/pyproject.toml",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "40820d20d8f56c1dc24c8f432141fa438d54473acbfecfa716fc9d188cbc8294",<br>  "lines": &#91;<br>    1,<br>    15<br>  &#93;,<br>  "selection&#95;sha256": "8fc8e7df82f18edc826b13f63f097661c1f40b19d2e7ab576e25854b453919e3"<br>}；{<br>  "id": "S15",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/pyproject.toml",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "40820d20d8f56c1dc24c8f432141fa438d54473acbfecfa716fc9d188cbc8294",<br>  "lines": &#91;<br>    301,<br>    327<br>  &#93;,<br>  "selection&#95;sha256": "ac6771e334ffad6fe8cb4934797de797375c87d4c33a16afff72de8d1642893f"<br>}；{<br>  "id": "S42",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/LICENSE",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "d131d0e96700cd78f8b3fa7ed79a47b019a0653066500faff376233246b6504d",<br>  "lines": &#91;<br>    1,<br>    22<br>  &#93;,<br>  "selection&#95;sha256": "d131d0e96700cd78f8b3fa7ed79a47b019a0653066500faff376233246b6504d"<br>}；{<br>  "id": "S44",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/pyproject.toml",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "40820d20d8f56c1dc24c8f432141fa438d54473acbfecfa716fc9d188cbc8294",<br>  "lines": &#91;<br>    45,<br>    69<br>  &#93;,<br>  "selection&#95;sha256": "e892c55c18d3d786696bf226eef30e4651216b0b71b89f35aa957f486ce0210f"<br>}；{<br>  "id": "S45",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/cli/main.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "8c02660dacd304f51fe8c4a9685d3f6d5324a7eef7779b6baa7325827bf01985",<br>  "lines": &#91;<br>    41,<br>    66<br>  &#93;,<br>  "selection&#95;sha256": "67527b228def54d21c5adc56b822ae446b51e24d18b4ca82b4a66669ca184d17"<br>}；{<br>  "id": "S46",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/cli/agent&#95;client.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "2fff7e6de630b6c8871db3419661195125c6128ac71d4d76f04e7561f7bdac17",<br>  "lines": &#91;<br>    35,<br>    91<br>  &#93;,<br>  "selection&#95;sha256": "8273620e89e199a39cd5b2afd65dcfe4483d6b463ab3435f2dceb59270ec5a59"<br>}；{<br>  "id": "S47",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/cli/agent&#95;client.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "2fff7e6de630b6c8871db3419661195125c6128ac71d4d76f04e7561f7bdac17",<br>  "lines": &#91;<br>    175,<br>    200<br>  &#93;,<br>  "selection&#95;sha256": "e1dffcec8fd29c41210478f2516c1a970fa0082d0c5666b8f2f47657e7226608"<br>}；{<br>  "id": "S48",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/cli/agent&#95;client.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "2fff7e6de630b6c8871db3419661195125c6128ac71d4d76f04e7561f7bdac17",<br>  "lines": &#91;<br>    286,<br>    415<br>  &#93;,<br>  "selection&#95;sha256": "24bbde0e597053cc6a0430fb83f870b0007bc5d1fac7916645caa6687d65c153"<br>}；{<br>  "id": "S49",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/cli/install&#95;skill.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "146be443d3b73b1e5c706b105fd0780831275baa6d0d61424b3c10d03dfa79aa",<br>  "lines": &#91;<br>    83,<br>    156<br>  &#93;,<br>  "selection&#95;sha256": "5d2fde106240cae8b78d502c274a07a764ff5a2f4e745f3f5a977af08dae7cf5"<br>}；{<br>  "id": "S50",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/cli/upload&#95;skill.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "2967da60c32c2495ea993f9122c6472d76ab86d3bcae878831fbeb07c55b0d1e",<br>  "lines": &#91;<br>    33,<br>    89<br>  &#93;,<br>  "selection&#95;sha256": "1893b3f3bfc12dc0ef7ff0b2f2e94d1c72e216bd9d229037f8a8d70b7a18b2f5"<br>}；{<br>  "id": "S66",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/mcp/server.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "cc6c4f24e5b91ab158f2bfbc4ebb27a38ce84d2937473dd85a6c2d035fc3b851",<br>  "lines": &#91;<br>    217,<br>    232<br>  &#93;,<br>  "selection&#95;sha256": "3656ba540327c3b7a1d33dffb02caba7b39ad65539fedb8c1d4d653d6304c994"<br>}；{<br>  "id": "S67",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/mcp/server&#95;fastmcp.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "19ba3010ea3bc5101953e44070932ec239d67908e1a0e992437665f98b827200",<br>  "lines": &#91;<br>    1,<br>    195<br>  &#93;,<br>  "selection&#95;sha256": "4aac45465ef6f0be7dd815096a3b9a9fdd1d7dbb53022f407691cf5786305d89"<br>}；{<br>  "id": "S68",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/mcp/server&#95;fastmcp.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "19ba3010ea3bc5101953e44070932ec239d67908e1a0e992437665f98b827200",<br>  "lines": &#91;<br>    1648,<br>    1835<br>  &#93;,<br>  "selection&#95;sha256": "06302c5f4aeec783710f5fc8c98d27be93d48c13d10fab5b677a743590787a94"<br>}；{<br>  "id": "S69",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/mcp/server&#95;fastmcp.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "19ba3010ea3bc5101953e44070932ec239d67908e1a0e992437665f98b827200",<br>  "lines": &#91;<br>    887,<br>    1050<br>  &#93;,<br>  "selection&#95;sha256": "21c671d1565867a5787f19da94e5cebefbb52993f3833f323afcc324ed59fb5e"<br>}；{<br>  "id": "S70",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/mcp/tools/packaging&#95;tools.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "7654385b60889705d98a3cc8e92602d13cadaf920ead26561e7fbb3a349a1fab",<br>  "lines": &#91;<br>    32,<br>    173<br>  &#93;,<br>  "selection&#95;sha256": "a042393939aa45cc7c4b046630c5a32b418895e25421f49b070c66fc6d116f9f"<br>}；{<br>  "id": "S71",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/mcp/tools/packaging&#95;tools.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "7654385b60889705d98a3cc8e92602d13cadaf920ead26561e7fbb3a349a1fab",<br>  "lines": &#91;<br>    232,<br>    298<br>  &#93;,<br>  "selection&#95;sha256": "c1abd4a79a92647fd3a4044f1cddc566c6dd953c3aa5d6c6824db8d9e27ba109"<br>}；{<br>  "id": "S72",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/mcp/tools/scraping&#95;tools.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "0073daae89b191d907fb080daf78f044d55d6890a8c929e7dcdc10c9ff19a735",<br>  "lines": &#91;<br>    211,<br>    310<br>  &#93;,<br>  "selection&#95;sha256": "361fb788f3029d6990b596a7675a68eb4f81df8d1e70404a6489780f93276f9d"<br>}；{<br>  "id": "S73",<br>  "purpose": "support",<br>  "path": ".github/tools/external/Skill&#95;Seekers-development/src/skill&#95;seekers/mcp/tools/packaging&#95;tools.py",<br>  "repository": ".github/tools/external/Skill&#95;Seekers-development",<br>  "revision": "26638b248279a3b001b651475e0f28975f5ff069",<br>  "sha256": "7654385b60889705d98a3cc8e92602d13cadaf920ead26561e7fbb3a349a1fab",<br>  "lines": &#91;<br>    433,<br>    904<br>  &#93;,<br>  "selection&#95;sha256": "5eef32044bf73950d2c4168ff30faa18e8064400aa0ee4f78dff9029d4fae074"<br>}<br>本地入口记录：{<br>  "path": ".github/tools/external/Skill&#95;Seekers-development",<br>  "objects": &#91;<br>    "faqi-skill-seekers"<br>  &#93;,<br>  "sources": &#91;<br>    "S14",<br>    "S15",<br>    "S16",<br>    "S42",<br>    "S44",<br>    "S45",<br>    "S46",<br>    "S47",<br>    "S48",<br>    "S49",<br>    "S50",<br>    "S66",<br>    "S67",<br>    "S68",<br>    "S69",<br>    "S70",<br>    "S71",<br>    "S72",<br>    "S73"<br>  &#93;,<br>  "boundary": "源码内容与仓库载体、接口规范、抓取过程、输入资料和生成Skill分开。",<br>  "pending": &#91;<br>    "2026-10-14：S45–S50绑定固定CLI路由、AgentClient与install/upload静态选区。CLI映射包含create/enhance/package/upload/install/install-agent等；AgentClient的auto模式按环境密钥选择API或本地代理，API路径将prompt发送给provider，本地subprocess.run未显式限制env；Claude预设含--dangerously-skip-permissions，Codex含--full-auto和--skip-git-repo-check。install将auto&#95;upload设为默认true（可用--no-upload），upload路径调用目标adaptor并可从环境变量取key。仅静态审阅，未运行、联网、上传或读取凭据；完整MCP链路、数据范围/来源授权、子进程权限、环境隔离、外部与本地写入及恢复路径仍待审。",<br>    "仓库LICENSE标注MIT，但版权行保留&#91;Your Name/Username&#93;占位符；权利主体与授权未核，不作许可证批准依据。",<br>    "固定pyproject将PyMuPDF&gt;=1.24.14列为核心依赖；2026-10-14本地Python 3.12.3环境未安装PyMuPDF（pip另有&#126;umpy无效发行警告），运行/doctor/PDF路径未验证。这是环境观察，不等于上游实现缺陷。",<br>    "2026-10-15：在Python 3.12.3环境运行python3 -m pip show PyMuPDF仍显示未安装；未安装依赖、未运行Skill Seekers。运行验证仍为false；此项只是目标环境依赖存在性检查，不是程序测试。",<br>    "2026-10-16：S66–S73只静态复核固定pin的MCP兼容入口、FastMCP、抓取及package/upload/install选区。默认stdio，HTTP默认127.0.0.1:8000，选区配置通配CORS；回环监听与CORS不等于认证授权。package默认auto&#95;upload=true，命中平台密钥时加入上传标志；upload显式api&#95;key被放入--api-key进程参数，Popen未显式限定env，凭据暴露与环境继承边界待核，未读取任何真实值。install除抓取、AI增强和打包外，还含条件上传及marketplace发布分支，auto&#95;upload=false不关闭前序步骤或独立发布支路；scrape&#95;docs的unlimited临时配置写入先于dry&#95;run分支，不能把预览声明推广为零I/O或可完整回滚。源码注释34工具、静态40装饰函数和health的2.1.1字符串都不是运行清单或已核版本。未导入、执行、启服务、抓取、上传或安装；认证、数据来源授权、完整下游副作用、超时/取消及恢复仍待独立验证。"<br>  &#93;<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "faqi-skill-seekers",<br>  "grade&#95;id": "faqi-xuan-intermediate",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：外部知识转可复用技能",<br>  "basis": "增加Agent可复用的领域能力和上下文资产；需特定工作流，不能替代通用推理与工具执行。"<br>}<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：登记未记录设计者为何选择该结构/接口/依赖；不能从被登记为重要推断其设计意图。 |
| 11 | 内部如何实现？ | 待核：当前仅有固定源码选区及SHA登记；尚未沿调用者、数据流、状态与失败路径完成实现链分析。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 登记边界（原字段）：指固定submodule修订的软件实现；多个CLI入口及可选MCP模块不机械复制产品身份。3.5.1仅为pyproject源码声明，不是已核发布或运行版。MCP头注释34项与静态40个装饰函数、health返回2.1.1均不作为运行清单或身份版本证明。<br>重要性纳入范围：Vibe Coding重要性：外部知识转可复用技能<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。<br>待核：具体操作系统、依赖版本、权限、输入规模和部署配置须按实际来源及工作负载核验。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-faqi-claude-skill-init-3a642a5d"></a>
### 官方Skill初始化脚本

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | 官方Skill初始化脚本 |
| 2 | 是什么 | 现有登记将其界定为软件工件：只纳入skill-creator下生成目录/模板的独立Python程序，不把官方Skill集合、自然语言方法、模板或其他全部辅助脚本称作同一程序。<br>此处复述登记边界，不证明当前可安装、可运行或有效。 |
| 3 | 为什么 | 待核：未记录为何采用该程序/配置；重要性范围与分级依据不等于采用动机。 |
| 4 | 怎么做 | 待核：登记冻结了源码选区，但没有验证该对象当前完整的调用方式、输入输出与安全前提；选区本身不是操作手册。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 法器对象ID=faqi-claude-skill-init；本体类型=software-artifact；版本声明=未声明；本地入口=.github/tools/external/claude-official-skills；当前运行实例/部署状态未在对象记录中声明。<br>Vibe Coding 重要性暂定：玄阶初级（grade&#95;id=faqi-xuan-initial；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：特定Skill模板初始化；分级依据：降低Claude Skill结构初始化成本，作用范围绑定特定生态，可手工完成且不影响其他Agent的基础闭环。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。<br>来源ID：S23, S22, S43, S51。 |
| 7 | 出处 | 固定实现/佐证来源记录：{<br>  "id": "S23",<br>  "purpose": "implementation",<br>  "path": ".github/tools/external/claude-official-skills/skills/skill-creator/scripts/init&#95;skill.py",<br>  "repository": ".github/tools/external/claude-official-skills",<br>  "revision": "1ed29a03dc852d30fa6ef2ca53a67dc2c2c2c563",<br>  "sha256": "cf12790f1d4958799281920d599f56aea38fb5c26e2812a61dd740bf3d4b6b99",<br>  "lines": &#91;<br>    194,<br>    304<br>  &#93;,<br>  "selection&#95;sha256": "f3ef6ff82946a9596d5cacfc1ed0405765187e5ffec5a4ede6c15f5e8dd248dd"<br>}；{<br>  "id": "S22",<br>  "purpose": "support",<br>  "path": ".github/tools/external/claude-official-skills/README.md",<br>  "repository": ".github/tools/external/claude-official-skills",<br>  "revision": "1ed29a03dc852d30fa6ef2ca53a67dc2c2c2c563",<br>  "sha256": "d7c5c2f9b248c7c0b31f093cf22b9a7407f5b093c8ca9ebe75a5b6845b02b76e",<br>  "lines": &#91;<br>    1,<br>    28<br>  &#93;,<br>  "selection&#95;sha256": "672c572d34a077a534754b7311d19db68a8402c86fe64e35be5e80da3ae7453a"<br>}；{<br>  "id": "S43",<br>  "purpose": "support",<br>  "path": ".github/tools/external/claude-official-skills/skills/skill-creator/LICENSE.txt",<br>  "repository": ".github/tools/external/claude-official-skills",<br>  "revision": "1ed29a03dc852d30fa6ef2ca53a67dc2c2c2c563",<br>  "sha256": "58d1e17ffe5109a7ae296caafcadfdbe6a7d176f0bc4ab01e12a689b0499d8bd",<br>  "lines": &#91;<br>    1,<br>    203<br>  &#93;,<br>  "selection&#95;sha256": "58d1e17ffe5109a7ae296caafcadfdbe6a7d176f0bc4ab01e12a689b0499d8bd"<br>}；{<br>  "id": "S51",<br>  "purpose": "support",<br>  "path": ".github/tools/external/claude-official-skills/skills/skill-creator/SKILL.md",<br>  "repository": ".github/tools/external/claude-official-skills",<br>  "revision": "1ed29a03dc852d30fa6ef2ca53a67dc2c2c2c563",<br>  "sha256": "d57b6e3a44535b9c0ef454dad5c86f5df78185fc80a65c7092885b4b5e10f81b",<br>  "lines": &#91;<br>    263,<br>    275<br>  &#93;,<br>  "selection&#95;sha256": "a8130ff1f013777e2c076569f5567924a4a0f3b23df7134ab4b0b99dd1aa86e9"<br>}<br>本地入口记录：{<br>  "path": ".github/tools/external/claude-official-skills",<br>  "objects": &#91;<br>    "faqi-claude-skill-init"<br>  &#93;,<br>  "sources": &#91;<br>    "S22",<br>    "S23",<br>    "S43",<br>    "S51"<br>  &#93;,<br>  "boundary": "集合入口不等于法器身份；指令内容与脚本实现分别判断。",<br>  "pending": &#91;<br>    "README明确部分文档Skill仅source-available，不能把整个集合称为同一开源许可证；skill-creator/LICENSE.txt提供Apache 2.0文本，但其附录版权字段为通用占位符，不能单独证明权利主体或完成全量许可审查。",<br>    "本次不批准再分发/商用许可。",<br>    "S51绑定skill-creator/SKILL.md步骤3和调用形式，证实该文档要求执行S23；它不验证S23实际输入校验或路径限制，且本次未执行脚本。",<br>    "2026-10-14：固定pin 1ed29a03dc852d30fa6ef2ca53a67dc2c2c2c563的S23（init&#95;skill.py:194-303）静态复核：CLI提示skill&#95;name应为小写kebab-case，但main未校验；函数直接拼接Path(path).resolve()/skill&#95;name且未检查目标仍在指定父目录内，若调用方传入含../或绝对路径的名称，输出可越出预期目录。目录/模板创建中途失败只返回错误，不回滚部分输出。风险取决于调用方输入控制；未运行脚本、未创建测试文件，不作可利用性或运行安全结论。其余辅助脚本仍未逐模块展开。"<br>  &#93;<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "faqi-claude-skill-init",<br>  "grade&#95;id": "faqi-xuan-initial",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：特定Skill模板初始化",<br>  "basis": "降低Claude Skill结构初始化成本，作用范围绑定特定生态，可手工完成且不影响其他Agent的基础闭环。"<br>}<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：登记未记录设计者为何选择该结构/接口/依赖；不能从被登记为重要推断其设计意图。 |
| 11 | 内部如何实现？ | 待核：当前仅有固定源码选区及SHA登记；尚未沿调用者、数据流、状态与失败路径完成实现链分析。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 登记边界（原字段）：只纳入skill-creator下生成目录/模板的独立Python程序，不把官方Skill集合、自然语言方法、模板或其他全部辅助脚本称作同一程序。<br>重要性纳入范围：Vibe Coding重要性：特定Skill模板初始化<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。<br>待核：具体操作系统、依赖版本、权限、输入规模和部署配置须按实际来源及工作负载核验。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-faqi-codex-config-installer-2dcddf43"></a>
### Codex配置安装与恢复脚本

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | Codex配置安装与恢复脚本 |
| 2 | 是什么 | 现有登记将其界定为软件工件：纳入安装脚本的程序指令；不是Codex CLI实现，不包含账号授权，safe/power配置、全局指令文本另作规约内容。备份/覆盖能力尚未运行验证。<br>此处复述登记边界，不证明当前可安装、可运行或有效。 |
| 3 | 为什么 | 待核：未记录为何采用该程序/配置；重要性范围与分级依据不等于采用动机。 |
| 4 | 怎么做 | 待核：登记冻结了源码选区，但没有验证该对象当前完整的调用方式、输入输出与安全前提；选区本身不是操作手册。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 法器对象ID=faqi-codex-config-installer；本体类型=software-artifact；版本声明=未声明；本地入口=.github/tools/config/.codex；当前运行实例/部署状态未在对象记录中声明。<br>Vibe Coding 重要性暂定：玄阶初级（grade&#95;id=faqi-xuan-initial；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：特定Agent接入配置；分级依据：降低特定Agent初始配置成本，但只服务候选运行时且可手工替代；不属于核心模型推理或执行闭环。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。<br>来源ID：S06, S05。 |
| 7 | 出处 | 固定实现/佐证来源记录：{<br>  "id": "S06",<br>  "purpose": "implementation",<br>  "path": ".github/tools/config/.codex/install.sh",<br>  "repository": ".",<br>  "revision": "0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2",<br>  "sha256": "a2ba28d5a48d46aa7d508408519be117f8726c8d66e632d8736deab9175b04a4",<br>  "lines": &#91;<br>    43,<br>    100<br>  &#93;,<br>  "selection&#95;sha256": "99ccf88c8d5ec6f7b7eda53fc4fd3af29a0ca08d9eef74ad3283cdf649d6a7cf"<br>}；{<br>  "id": "S05",<br>  "purpose": "support",<br>  "path": ".github/tools/config/.codex/README.md",<br>  "repository": ".",<br>  "revision": "0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2",<br>  "sha256": "4cd23bbafa069d8bd651e9997951ac99252cf13310d1c9fda14dcf01de818a53",<br>  "lines": &#91;<br>    1,<br>    78<br>  &#93;,<br>  "selection&#95;sha256": "b290d2842b0290ee9701e41c046634d2cd90684c0c53d1e97e3781a05d695e87"<br>}<br>本地入口记录：{<br>  "path": ".github/tools/config/.codex",<br>  "objects": &#91;<br>    "faqi-codex-config-installer"<br>  &#93;,<br>  "sources": &#91;<br>    "S05",<br>    "S06"<br>  &#93;,<br>  "boundary": "配置与AGENTS文本不等于CLI；脚本本身有独立程序所指。",<br>  "pending": &#91;<br>    "Codex实际程序、已安装版本、权限及账户不由本目录证明。"<br>  &#93;<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "faqi-codex-config-installer",<br>  "grade&#95;id": "faqi-xuan-initial",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：特定Agent接入配置",<br>  "basis": "降低特定Agent初始配置成本，但只服务候选运行时且可手工替代；不属于核心模型推理或执行闭环。"<br>}<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：登记未记录设计者为何选择该结构/接口/依赖；不能从被登记为重要推断其设计意图。 |
| 11 | 内部如何实现？ | 待核：当前仅有固定源码选区及SHA登记；尚未沿调用者、数据流、状态与失败路径完成实现链分析。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 登记边界（原字段）：纳入安装脚本的程序指令；不是Codex CLI实现，不包含账号授权，safe/power配置、全局指令文本另作规约内容。备份/覆盖能力尚未运行验证。<br>重要性纳入范围：Vibe Coding重要性：特定Agent接入配置<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。<br>待核：具体操作系统、依赖版本、权限、输入规模和部署配置须按实际来源及工作负载核验。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-faqi-skill-seekers-adapter-eb5e7e6f"></a>
### Skill Seekers本地运行适配脚本

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | Skill Seekers本地运行适配脚本 |
| 2 | 是什么 | 现有登记将其界定为软件工件：设置venv/PYTHONPATH并exec上游CLI的本地适配程序。指令内容不同于上游核心，不能把封装当同一副本，也不因同一用途合并其他生成脚本。<br>此处复述登记边界，不证明当前可安装、可运行或有效。 |
| 3 | 为什么 | 待核：未记录为何采用该程序/配置；重要性范围与分级依据不等于采用动机。 |
| 4 | 怎么做 | 待核：登记冻结了源码选区，但没有验证该对象当前完整的调用方式、输入输出与安全前提；选区本身不是操作手册。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 法器对象ID=faqi-skill-seekers-adapter；本体类型=software-artifact；版本声明=未声明；本地入口=.github/skills/auto-skill；当前运行实例/部署状态未在对象记录中声明。<br>Vibe Coding 重要性暂定：玄阶初级（grade&#95;id=faqi-xuan-initial；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：Skill Seekers本地适配入口；分级依据：便于调用特定知识转技能工具；范围受上游工具限制，可直接调用或人工替代。不代表效能评级、运行结果或质量结论。<br>既有关系记录：{<br>  "subject": "faqi-skill-seekers-adapter",<br>  "predicate": "requires",<br>  "target&#95;label": "链接源码中的skill&#95;seekers.cli.main",<br>  "related&#95;object&#95;id": "faqi-skill-seekers",<br>  "evidence": "S10",<br>  "boundary": "源码路径确由软链接指到选定submodule；这是静态加载意图，venv实际依赖、Python解析和运行结果未核。"<br>}<br>来源ID：S10, S07。 |
| 7 | 出处 | 固定实现/佐证来源记录：{<br>  "id": "S10",<br>  "purpose": "implementation",<br>  "path": ".github/skills/auto-skill/scripts/skill-seekers.sh",<br>  "repository": ".",<br>  "revision": "0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2",<br>  "sha256": "fdbf73b1faa1a0f445663b5c7c1c9792bbfb6dcdf5f5308198503e14ea0c64dc",<br>  "lines": &#91;<br>    28,<br>    66<br>  &#93;,<br>  "selection&#95;sha256": "f678142dddda161372feb5c5af96bbbf5e1b3e76b9e2c7dc905a4d1ba18070f2"<br>}；{<br>  "id": "S07",<br>  "purpose": "support",<br>  "path": ".github/skills/auto-skill/README.md",<br>  "repository": ".",<br>  "revision": "0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2",<br>  "sha256": "2fd869316c0469d9c4079cd9a19c41698b501bca6ddd2b6cc03617e3f96218f0",<br>  "lines": &#91;<br>    1,<br>    21<br>  &#93;,<br>  "selection&#95;sha256": "2fd869316c0469d9c4079cd9a19c41698b501bca6ddd2b6cc03617e3f96218f0"<br>}<br>本地入口记录：{<br>  "path": ".github/skills/auto-skill",<br>  "objects": &#91;<br>    "faqi-auto-skill-create",<br>    "faqi-auto-skill-validate",<br>    "faqi-skill-seekers-adapter"<br>  &#93;,<br>  "sources": &#91;<br>    "S07",<br>    "S08",<br>    "S09",<br>    "S10"<br>  &#93;,<br>  "boundary": "Skill说明/规约与三个独立入口脚本分离，不把整Skill包登记成一件软件。",<br>  "pending": &#91;<br>    "其他辅助模块未逐模块登记，不能将本次选区称为全包能力审查。"<br>  &#93;<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "faqi-skill-seekers-adapter",<br>  "grade&#95;id": "faqi-xuan-initial",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：Skill Seekers本地适配入口",<br>  "basis": "便于调用特定知识转技能工具；范围受上游工具限制，可直接调用或人工替代。"<br>}<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：登记未记录设计者为何选择该结构/接口/依赖；不能从被登记为重要推断其设计意图。 |
| 11 | 内部如何实现？ | 待核：当前仅有固定源码选区及SHA登记；尚未沿调用者、数据流、状态与失败路径完成实现链分析。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 登记边界（原字段）：设置venv/PYTHONPATH并exec上游CLI的本地适配程序。指令内容不同于上游核心，不能把封装当同一副本，也不因同一用途合并其他生成脚本。<br>重要性纳入范围：Vibe Coding重要性：Skill Seekers本地适配入口<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。<br>待核：具体操作系统、依赖版本、权限、输入规模和部署配置须按实际来源及工作负载核验。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |
