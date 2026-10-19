<!-- generated: sync-faqi-catalog.py -->
# Vibe Coding法器重要性总表

## 字多不看

当前30个对象分别使用v0的15项说明表；分级仅表示“Vibe Coding 重要性暂定”，不代表效能验证。
原始登记、来源及历史见[data.json](data.json)；来源初审与当前迁移位置分开，视图不产生运行、许可或效果批准。

## 快速导航

- [法器总表](#法器总表)
- [原始说明](#原始说明)

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

- [法器总表](#法器总表)
- [原始说明](#原始说明)
- [faqi-system](#doc-faqi-system)
  - [vibe-coding-法器体系说明](#doc-faqi-system-vibe-coding-法器体系说明)
  - [一句话](#doc-faqi-system-一句话)
  - [字多不看](#doc-faqi-system-字多不看)
  - [对象边界](#doc-faqi-system-对象边界)
  - [重要性分级](#doc-faqi-system-重要性分级)
  - [重要性与效能评级](#doc-faqi-system-重要性与效能评级)
  - [选用流程](#doc-faqi-system-选用流程)
  - [skill-seekers-mcp-static-review](#doc-faqi-system-skill-seekers-mcp-static-review)
  - [固定源码复核skill-seekers-mcp](#doc-faqi-system-固定源码复核skill-seekers-mcp)
  - [登记与维护](#doc-faqi-system-登记与维护)

</details>

## 使用方式

原始数据只在data.json维护；运行make sync-faqi-catalog更新本文件。

## 正文

## 法器总表

- [2.2 云端模型服务/API与固定模型版本](#v0-faqi-dep-category-cloud-model-api-1a52191c)
- [Pi Agent CLI（当前 PATH 实例）](#v0-faqi-dep-pi-cli-7a8190bb)
- [2.2 本地模型权重、Tokenizer与推理引擎](#v0-faqi-dep-category-local-model-stack-7430e743)
- [Codex CLI（依赖图替代项）](#v0-faqi-dep-codex-cli-89544cbf)
- [GNU Bash](#v0-faqi-dep-bash-9e17a7e4)
- [3.2 Terminal Emulator / PTY](#v0-faqi-dep-category-terminal-pty-3d912d9d)
- [Git 本地客户端](#v0-faqi-dep-git-client-817eaef2)
- [8 CPU/GPU、内存、存储、网络、电力与数据中心](#v0-faqi-dep-category-infrastructure-92099635)
- [4.2 包注册表、Git源与可信缓存](#v0-faqi-dep-category-package-sources-de4ecd15)
- [Node.js 运行时](#v0-faqi-dep-nodejs-runtime-154fe616)
- [npm / npx 工具](#v0-faqi-dep-npm-npx-99c5e69b)
- [Python 运行时](#v0-faqi-dep-python-runtime-c49ee719)
- [GNU Make](#v0-faqi-dep-gnu-make-a64dde37)
- [Ubuntu 用户空间发行版](#v0-faqi-dep-ubuntu-userland-27a7ecd2)
- [WSL2 Linux 内核](#v0-faqi-dep-wsl2-kernel-dc978cb1)
- [WSL 2 承载平台](#v0-faqi-dep-wsl2-platform-116a484c)
- [7.1 Git托管、CI Runner与CI/CD平台](#v0-faqi-dep-category-ci-platform-e3564493)
- [2.3 检索/索引/记忆与向量库](#v0-faqi-dep-category-retrieval-memory-da201109)
- [7.2-7.3 制品注册表、部署目标、产品运行时、数据库与外部API](#v0-faqi-dep-category-deployment-data-35c30956)
- [auto-skill模板生成脚本](#v0-faqi-faqi-auto-skill-create-ffe7ec4d)
- [auto-skill结构校验脚本](#v0-faqi-faqi-auto-skill-validate-5244b18f)
- [Skill Seekers程序](#v0-faqi-faqi-skill-seekers-cc1f7ed8)
- [官方Skill初始化脚本](#v0-faqi-faqi-claude-skill-init-3a642a5d)
- [Codex配置安装与恢复脚本](#v0-faqi-faqi-codex-config-installer-2dcddf43)
- [Skill Seekers本地运行适配脚本](#v0-faqi-faqi-skill-seekers-adapter-eb5e7e6f)
- [tmux 当前运行实例](#v0-faqi-dep-tmux-runtime-8bd62e08)
- [auto-tmux命令封装程序](#v0-faqi-faqi-auto-tmux-09bb1add)
- [tmux终端复用程序](#v0-faqi-faqi-tmux-fbe1a81c)
- [oh-my-tmux可执行配置程序](#v0-faqi-faqi-oh-my-tmux-3ab56947)
- [提示词格式转换程序](#v0-faqi-faqi-prompt-converter-43a9d077)

<a id="v0-faqi-dep-category-cloud-model-api-1a52191c"></a>
### 2.2 云端模型服务/API与固定模型版本

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | 2.2 云端模型服务/API与固定模型版本 |
| 2 | 是什么 | 依赖图将其作为抽象依赖类别登记：2.2 云端模型服务/API与固定模型版本；纳入依据：用户确认此依赖类别已核并要求纳入；服务/API与模型制品仍分开登记；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。 |
| 3 | 为什么 | 待核：抽象类别的纳入依据已记录，但没有具体采用动机；不把范围理由改写成产品用途。 |
| 4 | 怎么做 | 不适用：本条是抽象依赖类别，不指定唯一可执行产品、安装步骤或操作流程；具体实现需另行识别。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖类别ID=dep-category-cloud-model-api；类别节点=2.2 云端模型服务/API与固定模型版本；纳入状态=user&#95;confirmed&#95;in&#95;scope。这是抽象类别，不是具体产品或运行实例。<br>Vibe Coding 重要性暂定：天阶高级（grade&#95;id=faqi-tian-advanced；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：核心模型推理与代码生成；分级依据：提供理解需求、推理和生成代码的核心智能能力；没有模型推理路径即失去Vibe Coding的定义性特征，供应商与模型可替换。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖类别来源与登记记录：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>类别登记：{<br>  "id": "dep-category-cloud-model-api",<br>  "node": "2.2 云端模型服务/API与固定模型版本",<br>  "disposition": "user&#95;confirmed&#95;in&#95;scope",<br>  "reason": "用户确认此依赖类别已核并要求纳入；服务/API与模型制品仍分开登记；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-category-cloud-model-api",<br>  "grade&#95;id": "faqi-tian-advanced",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：核心模型推理与代码生成",<br>  "basis": "提供理解需求、推理和生成代码的核心智能能力；没有模型推理路径即失去Vibe Coding的定义性特征，供应商与模型可替换。"<br>}<br>类别纳入状态仅表示范围登记，不指向已部署的具体产品。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 不适用：该条是类别节点而非具名实现，当前材料不能支持具体设计选择解释。 |
| 11 | 内部如何实现？ | 不适用：抽象类别没有单一内部实现；不得以任一供应商/实现代表整个类别。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 类别依据（原记录）：用户确认此依赖类别已核并要求纳入；服务/API与模型制品仍分开登记；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。<br>纳入状态：user&#95;confirmed&#95;in&#95;scope；类别不是具体实现或部署。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-pi-cli-7a8190bb"></a>
### Pi Agent CLI（当前 PATH 实例）

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | Pi Agent CLI（当前 PATH 实例） |
| 2 | 是什么 | 现有依赖图将其记录为2.1 Agent运行时 / Pi Agent节点；身份状态与证据字段：pi --version 输出 1.1.0；type -a 显示多个同名入口，本记录只绑定当前 shell 选中的入口；先前环境记录为 1.0.4，宿主/路径差异待核，不将此版本绑定到会话服务端。 |
| 3 | 为什么 | 待核：观察记录未说明采用动机；节点、版本和重要性依据不能替代问题价值证据。 |
| 4 | 怎么做 | 待核：依赖图节点/观测版本不描述端到端使用步骤；当前没有同版本、同环境的运行操作记录。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖图对象ID=dep-pi-cli；图节点=2.1 Agent运行时 / Pi Agent；身份状态=runtime&#95;observed；观测版本=1.1.0；相关本地对象=未关联。<br>Vibe Coding 重要性暂定：天阶高级（grade&#95;id=faqi-tian-advanced；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：当前核心Agent运行与工具编排；分级依据：直接承接需求、上下文、模型调用和工具执行循环；当前环境的核心交互入口，缺失会改变Vibe Coding核心形态。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖图来源：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>依赖图对象记录：{<br>  "id": "dep-pi-cli",<br>  "name": "Pi Agent CLI（当前 PATH 实例）",<br>  "type&#95;id": "software-artifact",<br>  "graph&#95;node": "2.1 Agent运行时 / Pi Agent",<br>  "identity&#95;status": "runtime&#95;observed",<br>  "version": "1.1.0",<br>  "evidence": "pi --version 输出 1.1.0；type -a 显示多个同名入口，本记录只绑定当前 shell 选中的入口；先前环境记录为 1.0.4，宿主/路径差异待核，不将此版本绑定到会话服务端。",<br>  "resource&#95;ids": &#91;&#93;,<br>  "related&#95;object&#95;id": null,<br>  "grade&#95;id": null,<br>  "grade&#95;status": "pending",<br>  "grade&#95;reason": "分级量表仍为 draft，初/中/高结果带阈值未校准；本条未建立任务族效果合同。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-pi-cli",<br>  "grade&#95;id": "faqi-tian-advanced",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：当前核心Agent运行与工具编排",<br>  "basis": "直接承接需求、上下文、模型调用和工具执行循环；当前环境的核心交互入口，缺失会改变Vibe Coding核心形态。"<br>}<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：依赖图记录不含设计决策依据；不得从依赖关系反推设计意图。 |
| 11 | 内部如何实现？ | 待核：已登记的是观察到的节点、版本与关系；没有足以说明内部调用、数据流和状态机制的证据。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 观察证据/边界（原记录）：pi --version 输出 1.1.0；type -a 显示多个同名入口，本记录只绑定当前 shell 选中的入口；先前环境记录为 1.0.4，宿主/路径差异待核，不将此版本绑定到会话服务端。<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。<br>重要性纳入范围：Vibe Coding重要性：当前核心Agent运行与工具编排<br>待核：版本、平台、配置、权限、协议及工作负载条件尚未按具体环境验证。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-category-local-model-stack-7430e743"></a>
### 2.2 本地模型权重、Tokenizer与推理引擎

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | 2.2 本地模型权重、Tokenizer与推理引擎 |
| 2 | 是什么 | 依赖图将其作为抽象依赖类别登记：2.2 本地模型权重、Tokenizer与推理引擎；纳入依据：用户确认此依赖类别已核并要求纳入；模型制品、Tokenizer与推理程序分别判断；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。 |
| 3 | 为什么 | 待核：抽象类别的纳入依据已记录，但没有具体采用动机；不把范围理由改写成产品用途。 |
| 4 | 怎么做 | 不适用：本条是抽象依赖类别，不指定唯一可执行产品、安装步骤或操作流程；具体实现需另行识别。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖类别ID=dep-category-local-model-stack；类别节点=2.2 本地模型权重、Tokenizer与推理引擎；纳入状态=user&#95;confirmed&#95;in&#95;scope。这是抽象类别，不是具体产品或运行实例。<br>Vibe Coding 重要性暂定：天阶中级（grade&#95;id=faqi-tian-intermediate；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：本地/离线模型推理路径；分级依据：可提供核心模型推理并支持本地化、隐私或离线需求；在通用工作流中可由云端推理替代，故低于定义性核心路径。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖类别来源与登记记录：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>类别登记：{<br>  "id": "dep-category-local-model-stack",<br>  "node": "2.2 本地模型权重、Tokenizer与推理引擎",<br>  "disposition": "user&#95;confirmed&#95;in&#95;scope",<br>  "reason": "用户确认此依赖类别已核并要求纳入；模型制品、Tokenizer与推理程序分别判断；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-category-local-model-stack",<br>  "grade&#95;id": "faqi-tian-intermediate",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：本地/离线模型推理路径",<br>  "basis": "可提供核心模型推理并支持本地化、隐私或离线需求；在通用工作流中可由云端推理替代，故低于定义性核心路径。"<br>}<br>类别纳入状态仅表示范围登记，不指向已部署的具体产品。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 不适用：该条是类别节点而非具名实现，当前材料不能支持具体设计选择解释。 |
| 11 | 内部如何实现？ | 不适用：抽象类别没有单一内部实现；不得以任一供应商/实现代表整个类别。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 类别依据（原记录）：用户确认此依赖类别已核并要求纳入；模型制品、Tokenizer与推理程序分别判断；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。<br>纳入状态：user&#95;confirmed&#95;in&#95;scope；类别不是具体实现或部署。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-codex-cli-89544cbf"></a>
### Codex CLI（依赖图替代项）

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | Codex CLI（依赖图替代项） |
| 2 | 是什么 | 现有依赖图将其记录为2.1 Agent运行时 / Codex替代项节点；身份状态与证据字段：依赖图及外部资源行指向 Codex CLI 候选；当前安装身份、可执行入口、版本与来源未核。 |
| 3 | 为什么 | 待核：观察记录未说明采用动机；节点、版本和重要性依据不能替代问题价值证据。 |
| 4 | 怎么做 | 待核：依赖图节点/观测版本不描述端到端使用步骤；当前没有同版本、同环境的运行操作记录。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖图对象ID=dep-codex-cli；图节点=2.1 Agent运行时 / Codex替代项；身份状态=named&#95;candidate；观测版本=未记录；相关本地对象=未关联。；关联资源ID=tools-platforms-codex-cli-362bc20a。<br>Vibe Coding 重要性暂定：天阶中级（grade&#95;id=faqi-tian-intermediate；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：替代Agent运行时；分级依据：若选用可承担AI代码协作与工具编排核心；当前仅具名候选且可与其他运行时替换，低于已用核心路径。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。<br>关联资源ID：tools-platforms-codex-cli-362bc20a。资源链接/本地关联不证明许可、兼容性或功能等价。 |
| 7 | 出处 | 依赖图来源：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>依赖图对象记录：{<br>  "id": "dep-codex-cli",<br>  "name": "Codex CLI（依赖图替代项）",<br>  "type&#95;id": "software-artifact",<br>  "graph&#95;node": "2.1 Agent运行时 / Codex替代项",<br>  "identity&#95;status": "named&#95;candidate",<br>  "version": null,<br>  "evidence": "依赖图及外部资源行指向 Codex CLI 候选；当前安装身份、可执行入口、版本与来源未核。",<br>  "resource&#95;ids": &#91;<br>    "tools-platforms-codex-cli-362bc20a"<br>  &#93;,<br>  "related&#95;object&#95;id": null,<br>  "grade&#95;id": null,<br>  "grade&#95;status": "pending",<br>  "grade&#95;reason": "精确实现/版本、任务合同及分级量表阈值待核。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-codex-cli",<br>  "grade&#95;id": "faqi-tian-intermediate",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：替代Agent运行时",<br>  "basis": "若选用可承担AI代码协作与工具编排核心；当前仅具名候选且可与其他运行时替换，低于已用核心路径。"<br>}<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：依赖图记录不含设计决策依据；不得从依赖关系反推设计意图。 |
| 11 | 内部如何实现？ | 待核：已登记的是观察到的节点、版本与关系；没有足以说明内部调用、数据流和状态机制的证据。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 观察证据/边界（原记录）：依赖图及外部资源行指向 Codex CLI 候选；当前安装身份、可执行入口、版本与来源未核。<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。<br>重要性纳入范围：Vibe Coding重要性：替代Agent运行时<br>待核：版本、平台、配置、权限、协议及工作负载条件尚未按具体环境验证。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-bash-9e17a7e4"></a>
### GNU Bash

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | GNU Bash |
| 2 | 是什么 | 现有依赖图将其记录为6.2 Shell与命令解释器节点；身份状态与证据字段：bash --version 输出 GNU bash 5.2.21。 |
| 3 | 为什么 | 待核：观察记录未说明采用动机；节点、版本和重要性依据不能替代问题价值证据。 |
| 4 | 怎么做 | 待核：依赖图节点/观测版本不描述端到端使用步骤；当前没有同版本、同环境的运行操作记录。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖图对象ID=dep-bash；图节点=6.2 Shell与命令解释器；身份状态=runtime&#95;observed；观测版本=5.2.21；相关本地对象=未关联。<br>Vibe Coding 重要性暂定：地阶高级（grade&#95;id=faqi-di-advanced；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：Agent命令执行与脚本交互；分级依据：直接承接终端命令、开发脚本和验证操作，是当前Agent落地代码动作的高重要性接口；Shell实现可替代但该角色不可缺。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖图来源：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>依赖图对象记录：{<br>  "id": "dep-bash",<br>  "name": "GNU Bash",<br>  "type&#95;id": "software-artifact",<br>  "graph&#95;node": "6.2 Shell与命令解释器",<br>  "identity&#95;status": "runtime&#95;observed",<br>  "version": "5.2.21",<br>  "evidence": "bash --version 输出 GNU bash 5.2.21。",<br>  "resource&#95;ids": &#91;&#93;,<br>  "related&#95;object&#95;id": null,<br>  "grade&#95;id": null,<br>  "grade&#95;status": "pending",<br>  "grade&#95;reason": "版本观测不等于具体任务效果；分级量表阈值未校准。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-bash",<br>  "grade&#95;id": "faqi-di-advanced",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：Agent命令执行与脚本交互",<br>  "basis": "直接承接终端命令、开发脚本和验证操作，是当前Agent落地代码动作的高重要性接口；Shell实现可替代但该角色不可缺。"<br>}<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：依赖图记录不含设计决策依据；不得从依赖关系反推设计意图。 |
| 11 | 内部如何实现？ | 待核：已登记的是观察到的节点、版本与关系；没有足以说明内部调用、数据流和状态机制的证据。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 观察证据/边界（原记录）：bash --version 输出 GNU bash 5.2.21。<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。<br>重要性纳入范围：Vibe Coding重要性：Agent命令执行与脚本交互<br>待核：版本、平台、配置、权限、协议及工作负载条件尚未按具体环境验证。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-category-terminal-pty-3d912d9d"></a>
### 3.2 Terminal Emulator / PTY

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | 3.2 Terminal Emulator / PTY |
| 2 | 是什么 | 依赖图将其作为抽象依赖类别登记：3.2 Terminal Emulator / PTY；纳入依据：用户确认此依赖类别已核并要求纳入；终端模拟器与PTY系统接口分开分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。 |
| 3 | 为什么 | 待核：抽象类别的纳入依据已记录，但没有具体采用动机；不把范围理由改写成产品用途。 |
| 4 | 怎么做 | 不适用：本条是抽象依赖类别，不指定唯一可执行产品、安装步骤或操作流程；具体实现需另行识别。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖类别ID=dep-category-terminal-pty；类别节点=3.2 Terminal Emulator / PTY；纳入状态=user&#95;confirmed&#95;in&#95;scope。这是抽象类别，不是具体产品或运行实例。<br>Vibe Coding 重要性暂定：地阶高级（grade&#95;id=faqi-di-advanced；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：Agent调用工具与执行开发命令；分级依据：把Agent计划转成真实文件、构建和测试操作的关键执行边界；没有等价工具执行通道，代码闭环无法完成。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖类别来源与登记记录：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>类别登记：{<br>  "id": "dep-category-terminal-pty",<br>  "node": "3.2 Terminal Emulator / PTY",<br>  "disposition": "user&#95;confirmed&#95;in&#95;scope",<br>  "reason": "用户确认此依赖类别已核并要求纳入；终端模拟器与PTY系统接口分开分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-category-terminal-pty",<br>  "grade&#95;id": "faqi-di-advanced",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：Agent调用工具与执行开发命令",<br>  "basis": "把Agent计划转成真实文件、构建和测试操作的关键执行边界；没有等价工具执行通道，代码闭环无法完成。"<br>}<br>类别纳入状态仅表示范围登记，不指向已部署的具体产品。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 不适用：该条是类别节点而非具名实现，当前材料不能支持具体设计选择解释。 |
| 11 | 内部如何实现？ | 不适用：抽象类别没有单一内部实现；不得以任一供应商/实现代表整个类别。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 类别依据（原记录）：用户确认此依赖类别已核并要求纳入；终端模拟器与PTY系统接口分开分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。<br>纳入状态：user&#95;confirmed&#95;in&#95;scope；类别不是具体实现或部署。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-git-client-817eaef2"></a>
### Git 本地客户端

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | Git 本地客户端 |
| 2 | 是什么 | 现有依赖图将其记录为3.2 文件与代码 / Git本地客户端与工作树节点；身份状态与证据字段：git --version 输出 git version 2.43.0。 |
| 3 | 为什么 | 待核：观察记录未说明采用动机；节点、版本和重要性依据不能替代问题价值证据。 |
| 4 | 怎么做 | 待核：依赖图节点/观测版本不描述端到端使用步骤；当前没有同版本、同环境的运行操作记录。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖图对象ID=dep-git-client；图节点=3.2 文件与代码 / Git本地客户端与工作树；身份状态=runtime&#95;observed；观测版本=2.43.0；相关本地对象=未关联。<br>Vibe Coding 重要性暂定：地阶高级（grade&#95;id=faqi-di-advanced；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：代码变更追踪、比较与恢复；分级依据：支撑审查AI改动、保留版本历史和安全回退，是可维护代码生成闭环的高重要性基础；版本控制实现可替代。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖图来源：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>依赖图对象记录：{<br>  "id": "dep-git-client",<br>  "name": "Git 本地客户端",<br>  "type&#95;id": "software-artifact",<br>  "graph&#95;node": "3.2 文件与代码 / Git本地客户端与工作树",<br>  "identity&#95;status": "runtime&#95;observed",<br>  "version": "2.43.0",<br>  "evidence": "git --version 输出 git version 2.43.0。",<br>  "resource&#95;ids": &#91;&#93;,<br>  "related&#95;object&#95;id": null,<br>  "grade&#95;id": null,<br>  "grade&#95;status": "pending",<br>  "grade&#95;reason": "版本观测不等于具体任务效果；分级量表阈值未校准。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-git-client",<br>  "grade&#95;id": "faqi-di-advanced",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：代码变更追踪、比较与恢复",<br>  "basis": "支撑审查AI改动、保留版本历史和安全回退，是可维护代码生成闭环的高重要性基础；版本控制实现可替代。"<br>}<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：依赖图记录不含设计决策依据；不得从依赖关系反推设计意图。 |
| 11 | 内部如何实现？ | 待核：已登记的是观察到的节点、版本与关系；没有足以说明内部调用、数据流和状态机制的证据。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 观察证据/边界（原记录）：git --version 输出 git version 2.43.0。<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。<br>重要性纳入范围：Vibe Coding重要性：代码变更追踪、比较与恢复<br>待核：版本、平台、配置、权限、协议及工作负载条件尚未按具体环境验证。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-category-infrastructure-92099635"></a>
### 8 CPU/GPU、内存、存储、网络、电力与数据中心

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | 8 CPU/GPU、内存、存储、网络、电力与数据中心 |
| 2 | 是什么 | 依赖图将其作为抽象依赖类别登记：8 CPU/GPU、内存、存储、网络、电力与数据中心；纳入依据：用户确认此资源类别已核并要求纳入；物理设备、基础设施与供给服务按所指分别分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。 |
| 3 | 为什么 | 待核：抽象类别的纳入依据已记录，但没有具体采用动机；不把范围理由改写成产品用途。 |
| 4 | 怎么做 | 不适用：本条是抽象依赖类别，不指定唯一可执行产品、安装步骤或操作流程；具体实现需另行识别。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖类别ID=dep-category-infrastructure；类别节点=8 CPU/GPU、内存、存储、网络、电力与数据中心；纳入状态=user&#95;confirmed&#95;in&#95;scope。这是抽象类别，不是具体产品或运行实例。<br>Vibe Coding 重要性暂定：地阶中级（grade&#95;id=faqi-di-intermediate；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：计算、存储与网络承载；分级依据：为模型调用、代码执行及数据交换提供资源底座；实现可跨云、主机和本地环境替换，故不是单一核心产品。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖类别来源与登记记录：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>类别登记：{<br>  "id": "dep-category-infrastructure",<br>  "node": "8 CPU/GPU、内存、存储、网络、电力与数据中心",<br>  "disposition": "user&#95;confirmed&#95;in&#95;scope",<br>  "reason": "用户确认此资源类别已核并要求纳入；物理设备、基础设施与供给服务按所指分别分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-category-infrastructure",<br>  "grade&#95;id": "faqi-di-intermediate",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：计算、存储与网络承载",<br>  "basis": "为模型调用、代码执行及数据交换提供资源底座；实现可跨云、主机和本地环境替换，故不是单一核心产品。"<br>}<br>类别纳入状态仅表示范围登记，不指向已部署的具体产品。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 不适用：该条是类别节点而非具名实现，当前材料不能支持具体设计选择解释。 |
| 11 | 内部如何实现？ | 不适用：抽象类别没有单一内部实现；不得以任一供应商/实现代表整个类别。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 类别依据（原记录）：用户确认此资源类别已核并要求纳入；物理设备、基础设施与供给服务按所指分别分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。<br>纳入状态：user&#95;confirmed&#95;in&#95;scope；类别不是具体实现或部署。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-category-package-sources-de4ecd15"></a>
### 4.2 包注册表、Git源与可信缓存

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | 4.2 包注册表、Git源与可信缓存 |
| 2 | 是什么 | 依赖图将其作为抽象依赖类别登记：4.2 包注册表、Git源与可信缓存；纳入依据：用户确认此依赖类别已核并要求纳入；注册表、Git来源与缓存分开分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。 |
| 3 | 为什么 | 待核：抽象类别的纳入依据已记录，但没有具体采用动机；不把范围理由改写成产品用途。 |
| 4 | 怎么做 | 不适用：本条是抽象依赖类别，不指定唯一可执行产品、安装步骤或操作流程；具体实现需另行识别。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖类别ID=dep-category-package-sources；类别节点=4.2 包注册表、Git源与可信缓存；纳入状态=user&#95;confirmed&#95;in&#95;scope。这是抽象类别，不是具体产品或运行实例。<br>Vibe Coding 重要性暂定：地阶中级（grade&#95;id=faqi-di-intermediate；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：依赖获取、锁定与复现；分级依据：支持安装成熟组件、解析代码依赖和重建开发环境；具体注册表与来源有替代，不直接承担AI生成。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖类别来源与登记记录：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>类别登记：{<br>  "id": "dep-category-package-sources",<br>  "node": "4.2 包注册表、Git源与可信缓存",<br>  "disposition": "user&#95;confirmed&#95;in&#95;scope",<br>  "reason": "用户确认此依赖类别已核并要求纳入；注册表、Git来源与缓存分开分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-category-package-sources",<br>  "grade&#95;id": "faqi-di-intermediate",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：依赖获取、锁定与复现",<br>  "basis": "支持安装成熟组件、解析代码依赖和重建开发环境；具体注册表与来源有替代，不直接承担AI生成。"<br>}<br>类别纳入状态仅表示范围登记，不指向已部署的具体产品。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 不适用：该条是类别节点而非具名实现，当前材料不能支持具体设计选择解释。 |
| 11 | 内部如何实现？ | 不适用：抽象类别没有单一内部实现；不得以任一供应商/实现代表整个类别。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 类别依据（原记录）：用户确认此依赖类别已核并要求纳入；注册表、Git来源与缓存分开分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。<br>纳入状态：user&#95;confirmed&#95;in&#95;scope；类别不是具体实现或部署。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-nodejs-runtime-154fe616"></a>
### Node.js 运行时

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | Node.js 运行时 |
| 2 | 是什么 | 现有依赖图将其记录为4.3 语言与运行时节点；身份状态与证据字段：node --version 输出 v22.23.2。 |
| 3 | 为什么 | 待核：观察记录未说明采用动机；节点、版本和重要性依据不能替代问题价值证据。 |
| 4 | 怎么做 | 待核：依赖图节点/观测版本不描述端到端使用步骤；当前没有同版本、同环境的运行操作记录。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖图对象ID=dep-nodejs-runtime；图节点=4.3 语言与运行时；身份状态=runtime&#95;observed；观测版本=22.23.2；相关本地对象=未关联。<br>Vibe Coding 重要性暂定：地阶中级（grade&#95;id=faqi-di-intermediate；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：前端及工具链代码运行；分级依据：支撑前端、Node项目和本仓Markdown工具链；具体语言环境可替代，重要性低于通用Agent与终端执行核心。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖图来源：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>依赖图对象记录：{<br>  "id": "dep-nodejs-runtime",<br>  "name": "Node.js 运行时",<br>  "type&#95;id": "software-artifact",<br>  "graph&#95;node": "4.3 语言与运行时",<br>  "identity&#95;status": "runtime&#95;observed",<br>  "version": "22.23.2",<br>  "evidence": "node --version 输出 v22.23.2。",<br>  "resource&#95;ids": &#91;&#93;,<br>  "related&#95;object&#95;id": null,<br>  "grade&#95;id": null,<br>  "grade&#95;status": "pending",<br>  "grade&#95;reason": "版本观测不等于具体任务效果；分级量表阈值未校准。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-nodejs-runtime",<br>  "grade&#95;id": "faqi-di-intermediate",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：前端及工具链代码运行",<br>  "basis": "支撑前端、Node项目和本仓Markdown工具链；具体语言环境可替代，重要性低于通用Agent与终端执行核心。"<br>}<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：依赖图记录不含设计决策依据；不得从依赖关系反推设计意图。 |
| 11 | 内部如何实现？ | 待核：已登记的是观察到的节点、版本与关系；没有足以说明内部调用、数据流和状态机制的证据。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 观察证据/边界（原记录）：node --version 输出 v22.23.2。<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。<br>重要性纳入范围：Vibe Coding重要性：前端及工具链代码运行<br>待核：版本、平台、配置、权限、协议及工作负载条件尚未按具体环境验证。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-npm-npx-99c5e69b"></a>
### npm / npx 工具

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | npm / npx 工具 |
| 2 | 是什么 | 现有依赖图将其记录为4.2 包管理器与依赖解析器节点；身份状态与证据字段：npm --version 与 npx --version 均输出 10.9.8；登记为同一当前工具链版本观测，不把命令入口重复计数为两件法器。 |
| 3 | 为什么 | 待核：观察记录未说明采用动机；节点、版本和重要性依据不能替代问题价值证据。 |
| 4 | 怎么做 | 待核：依赖图节点/观测版本不描述端到端使用步骤；当前没有同版本、同环境的运行操作记录。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖图对象ID=dep-npm-npx；图节点=4.2 包管理器与依赖解析器；身份状态=runtime&#95;observed；观测版本=10.9.8；相关本地对象=未关联。<br>Vibe Coding 重要性暂定：地阶中级（grade&#95;id=faqi-di-intermediate；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：Node依赖解析与工具调用；分级依据：让Node生态依赖和命令行工具可安装、解析与调用；作用范围依赖项目技术栈，可由其他生态包管理器替代。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖图来源：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>依赖图对象记录：{<br>  "id": "dep-npm-npx",<br>  "name": "npm / npx 工具",<br>  "type&#95;id": "software-artifact",<br>  "graph&#95;node": "4.2 包管理器与依赖解析器",<br>  "identity&#95;status": "runtime&#95;observed",<br>  "version": "10.9.8",<br>  "evidence": "npm --version 与 npx --version 均输出 10.9.8；登记为同一当前工具链版本观测，不把命令入口重复计数为两件法器。",<br>  "resource&#95;ids": &#91;&#93;,<br>  "related&#95;object&#95;id": null,<br>  "grade&#95;id": null,<br>  "grade&#95;status": "pending",<br>  "grade&#95;reason": "版本观测不等于具体任务效果；分级量表阈值未校准。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-npm-npx",<br>  "grade&#95;id": "faqi-di-intermediate",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：Node依赖解析与工具调用",<br>  "basis": "让Node生态依赖和命令行工具可安装、解析与调用；作用范围依赖项目技术栈，可由其他生态包管理器替代。"<br>}<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：依赖图记录不含设计决策依据；不得从依赖关系反推设计意图。 |
| 11 | 内部如何实现？ | 待核：已登记的是观察到的节点、版本与关系；没有足以说明内部调用、数据流和状态机制的证据。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 观察证据/边界（原记录）：npm --version 与 npx --version 均输出 10.9.8；登记为同一当前工具链版本观测，不把命令入口重复计数为两件法器。<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。<br>重要性纳入范围：Vibe Coding重要性：Node依赖解析与工具调用<br>待核：版本、平台、配置、权限、协议及工作负载条件尚未按具体环境验证。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-python-runtime-c49ee719"></a>
### Python 运行时

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | Python 运行时 |
| 2 | 是什么 | 现有依赖图将其记录为4.3 语言与运行时节点；身份状态与证据字段：python3 --version 输出 Python 3.12.3。 |
| 3 | 为什么 | 待核：观察记录未说明采用动机；节点、版本和重要性依据不能替代问题价值证据。 |
| 4 | 怎么做 | 待核：依赖图节点/观测版本不描述端到端使用步骤；当前没有同版本、同环境的运行操作记录。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖图对象ID=dep-python-runtime；图节点=4.3 语言与运行时；身份状态=runtime&#95;observed；观测版本=3.12.3；相关本地对象=未关联。<br>Vibe Coding 重要性暂定：地阶中级（grade&#95;id=faqi-di-intermediate；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：脚本、工具与项目代码运行；分级依据：支撑本仓工具及大量Python项目的执行和验证；语言运行时可按项目替代，重要但非所有Vibe Coding任务必需。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖图来源：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>依赖图对象记录：{<br>  "id": "dep-python-runtime",<br>  "name": "Python 运行时",<br>  "type&#95;id": "software-artifact",<br>  "graph&#95;node": "4.3 语言与运行时",<br>  "identity&#95;status": "runtime&#95;observed",<br>  "version": "3.12.3",<br>  "evidence": "python3 --version 输出 Python 3.12.3。",<br>  "resource&#95;ids": &#91;&#93;,<br>  "related&#95;object&#95;id": null,<br>  "grade&#95;id": null,<br>  "grade&#95;status": "pending",<br>  "grade&#95;reason": "版本观测不等于具体任务效果；分级量表阈值未校准。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-python-runtime",<br>  "grade&#95;id": "faqi-di-intermediate",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：脚本、工具与项目代码运行",<br>  "basis": "支撑本仓工具及大量Python项目的执行和验证；语言运行时可按项目替代，重要但非所有Vibe Coding任务必需。"<br>}<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：依赖图记录不含设计决策依据；不得从依赖关系反推设计意图。 |
| 11 | 内部如何实现？ | 待核：已登记的是观察到的节点、版本与关系；没有足以说明内部调用、数据流和状态机制的证据。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 观察证据/边界（原记录）：python3 --version 输出 Python 3.12.3。<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。<br>重要性纳入范围：Vibe Coding重要性：脚本、工具与项目代码运行<br>待核：版本、平台、配置、权限、协议及工作负载条件尚未按具体环境验证。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-gnu-make-a64dde37"></a>
### GNU Make

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | GNU Make |
| 2 | 是什么 | 现有依赖图将其记录为4.3 构建系统节点；身份状态与证据字段：make --version 输出 GNU Make 4.3。 |
| 3 | 为什么 | 待核：观察记录未说明采用动机；节点、版本和重要性依据不能替代问题价值证据。 |
| 4 | 怎么做 | 待核：依赖图节点/观测版本不描述端到端使用步骤；当前没有同版本、同环境的运行操作记录。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖图对象ID=dep-gnu-make；图节点=4.3 构建系统；身份状态=runtime&#95;observed；观测版本=4.3；相关本地对象=未关联。<br>Vibe Coding 重要性暂定：地阶初级（grade&#95;id=faqi-di-initial；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：可重复构建与检查入口；分级依据：把构建和验证命令组织成可重复入口有助于交付，但Make可由其他任务运行器或脚本替代。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖图来源：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>依赖图对象记录：{<br>  "id": "dep-gnu-make",<br>  "name": "GNU Make",<br>  "type&#95;id": "software-artifact",<br>  "graph&#95;node": "4.3 构建系统",<br>  "identity&#95;status": "runtime&#95;observed",<br>  "version": "4.3",<br>  "evidence": "make --version 输出 GNU Make 4.3。",<br>  "resource&#95;ids": &#91;&#93;,<br>  "related&#95;object&#95;id": null,<br>  "grade&#95;id": null,<br>  "grade&#95;status": "pending",<br>  "grade&#95;reason": "版本观测不等于具体任务效果；分级量表阈值未校准。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-gnu-make",<br>  "grade&#95;id": "faqi-di-initial",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：可重复构建与检查入口",<br>  "basis": "把构建和验证命令组织成可重复入口有助于交付，但Make可由其他任务运行器或脚本替代。"<br>}<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：依赖图记录不含设计决策依据；不得从依赖关系反推设计意图。 |
| 11 | 内部如何实现？ | 待核：已登记的是观察到的节点、版本与关系；没有足以说明内部调用、数据流和状态机制的证据。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 观察证据/边界（原记录）：make --version 输出 GNU Make 4.3。<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。<br>重要性纳入范围：Vibe Coding重要性：可重复构建与检查入口<br>待核：版本、平台、配置、权限、协议及工作负载条件尚未按具体环境验证。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-ubuntu-userland-27a7ecd2"></a>
### Ubuntu 用户空间发行版

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | Ubuntu 用户空间发行版 |
| 2 | 是什么 | 现有依赖图将其记录为6.1 Linux发行版 / Ubuntu节点；身份状态与证据字段：/etc/os-release 报告 Ubuntu 24.04.3 LTS（VERSION&#95;ID=24.04）。 |
| 3 | 为什么 | 待核：观察记录未说明采用动机；节点、版本和重要性依据不能替代问题价值证据。 |
| 4 | 怎么做 | 待核：依赖图节点/观测版本不描述端到端使用步骤；当前没有同版本、同环境的运行操作记录。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖图对象ID=dep-ubuntu-userland；图节点=6.1 Linux发行版 / Ubuntu；身份状态=runtime&#95;observed；观测版本=24.04.3 LTS；相关本地对象=未关联。<br>Vibe Coding 重要性暂定：地阶初级（grade&#95;id=faqi-di-initial；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：当前Linux用户空间；分级依据：承载当前工具链和本地命令，但同类操作系统环境可以替代，重要性来自运行基座而非该发行版身份。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖图来源：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>依赖图对象记录：{<br>  "id": "dep-ubuntu-userland",<br>  "name": "Ubuntu 用户空间发行版",<br>  "type&#95;id": "software-artifact",<br>  "graph&#95;node": "6.1 Linux发行版 / Ubuntu",<br>  "identity&#95;status": "runtime&#95;observed",<br>  "version": "24.04.3 LTS",<br>  "evidence": "/etc/os-release 报告 Ubuntu 24.04.3 LTS（VERSION&#95;ID=24.04）。",<br>  "resource&#95;ids": &#91;&#93;,<br>  "related&#95;object&#95;id": null,<br>  "grade&#95;id": null,<br>  "grade&#95;status": "pending",<br>  "grade&#95;reason": "版本观测不等于具体任务效果；分级量表阈值未校准。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-ubuntu-userland",<br>  "grade&#95;id": "faqi-di-initial",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：当前Linux用户空间",<br>  "basis": "承载当前工具链和本地命令，但同类操作系统环境可以替代，重要性来自运行基座而非该发行版身份。"<br>}<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：依赖图记录不含设计决策依据；不得从依赖关系反推设计意图。 |
| 11 | 内部如何实现？ | 待核：已登记的是观察到的节点、版本与关系；没有足以说明内部调用、数据流和状态机制的证据。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 观察证据/边界（原记录）：/etc/os-release 报告 Ubuntu 24.04.3 LTS（VERSION&#95;ID=24.04）。<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。<br>重要性纳入范围：Vibe Coding重要性：当前Linux用户空间<br>待核：版本、平台、配置、权限、协议及工作负载条件尚未按具体环境验证。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-wsl2-kernel-dc978cb1"></a>
### WSL2 Linux 内核

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | WSL2 Linux 内核 |
| 2 | 是什么 | 现有依赖图将其记录为6.1 WSL / 版本对应的Linux内核节点；身份状态与证据字段：uname -r 输出 6.6.87.2-microsoft-standard-WSL2；不据内核版本推断 Windows/WSL 产品版本。 |
| 3 | 为什么 | 待核：观察记录未说明采用动机；节点、版本和重要性依据不能替代问题价值证据。 |
| 4 | 怎么做 | 待核：依赖图节点/观测版本不描述端到端使用步骤；当前没有同版本、同环境的运行操作记录。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖图对象ID=dep-wsl2-kernel；图节点=6.1 WSL / 版本对应的Linux内核；身份状态=runtime&#95;observed；观测版本=6.6.87.2-microsoft-standard-WSL2；相关本地对象=未关联。<br>Vibe Coding 重要性暂定：地阶初级（grade&#95;id=faqi-di-initial；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：当前运行环境内核；分级依据：提供当前WSL用户空间的执行底座，但存在其他内核和宿主替代，不属于AI编程核心能力。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖图来源：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>依赖图对象记录：{<br>  "id": "dep-wsl2-kernel",<br>  "name": "WSL2 Linux 内核",<br>  "type&#95;id": "software-artifact",<br>  "graph&#95;node": "6.1 WSL / 版本对应的Linux内核",<br>  "identity&#95;status": "runtime&#95;observed",<br>  "version": "6.6.87.2-microsoft-standard-WSL2",<br>  "evidence": "uname -r 输出 6.6.87.2-microsoft-standard-WSL2；不据内核版本推断 Windows/WSL 产品版本。",<br>  "resource&#95;ids": &#91;&#93;,<br>  "related&#95;object&#95;id": null,<br>  "grade&#95;id": null,<br>  "grade&#95;status": "pending",<br>  "grade&#95;reason": "版本观测不等于具体任务效果；分级量表阈值未校准。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-wsl2-kernel",<br>  "grade&#95;id": "faqi-di-initial",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：当前运行环境内核",<br>  "basis": "提供当前WSL用户空间的执行底座，但存在其他内核和宿主替代，不属于AI编程核心能力。"<br>}<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：依赖图记录不含设计决策依据；不得从依赖关系反推设计意图。 |
| 11 | 内部如何实现？ | 待核：已登记的是观察到的节点、版本与关系；没有足以说明内部调用、数据流和状态机制的证据。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 观察证据/边界（原记录）：uname -r 输出 6.6.87.2-microsoft-standard-WSL2；不据内核版本推断 Windows/WSL 产品版本。<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。<br>重要性纳入范围：Vibe Coding重要性：当前运行环境内核<br>待核：版本、平台、配置、权限、协议及工作负载条件尚未按具体环境验证。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-dep-wsl2-platform-116a484c"></a>
### WSL 2 承载平台

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | WSL 2 承载平台 |
| 2 | 是什么 | 现有依赖图将其记录为6.1 Windows主机 / WSL节点；身份状态与证据字段：uname -r 含 microsoft-standard-WSL2，确认当前 Linux 内核运行在 WSL2 兼容环境；Windows宿主版本及 WSL 产品版本未核。 |
| 3 | 为什么 | 待核：观察记录未说明采用动机；节点、版本和重要性依据不能替代问题价值证据。 |
| 4 | 怎么做 | 待核：依赖图节点/观测版本不描述端到端使用步骤；当前没有同版本、同环境的运行操作记录。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖图对象ID=dep-wsl2-platform；图节点=6.1 Windows主机 / WSL；身份状态=runtime&#95;observed；观测版本=未记录；相关本地对象=未关联。<br>Vibe Coding 重要性暂定：地阶初级（grade&#95;id=faqi-di-initial；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：当前宿主环境实现；分级依据：为当前工具链提供运行宿主，但Linux、macOS或原生Windows等环境可替代，不是Vibe Coding定义性能力。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖图来源：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>依赖图对象记录：{<br>  "id": "dep-wsl2-platform",<br>  "name": "WSL 2 承载平台",<br>  "type&#95;id": "software-artifact",<br>  "graph&#95;node": "6.1 Windows主机 / WSL",<br>  "identity&#95;status": "runtime&#95;observed",<br>  "version": null,<br>  "evidence": "uname -r 含 microsoft-standard-WSL2，确认当前 Linux 内核运行在 WSL2 兼容环境；Windows宿主版本及 WSL 产品版本未核。",<br>  "resource&#95;ids": &#91;&#93;,<br>  "related&#95;object&#95;id": null,<br>  "grade&#95;id": null,<br>  "grade&#95;status": "pending",<br>  "grade&#95;reason": "承载平台精确版本、任务合同及分级量表阈值待核。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-wsl2-platform",<br>  "grade&#95;id": "faqi-di-initial",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：当前宿主环境实现",<br>  "basis": "为当前工具链提供运行宿主，但Linux、macOS或原生Windows等环境可替代，不是Vibe Coding定义性能力。"<br>}<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：依赖图记录不含设计决策依据；不得从依赖关系反推设计意图。 |
| 11 | 内部如何实现？ | 待核：已登记的是观察到的节点、版本与关系；没有足以说明内部调用、数据流和状态机制的证据。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 观察证据/边界（原记录）：uname -r 含 microsoft-standard-WSL2，确认当前 Linux 内核运行在 WSL2 兼容环境；Windows宿主版本及 WSL 产品版本未核。<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。<br>重要性纳入范围：Vibe Coding重要性：当前宿主环境实现<br>待核：版本、平台、配置、权限、协议及工作负载条件尚未按具体环境验证。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

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

<a id="v0-faqi-dep-tmux-runtime-8bd62e08"></a>
### tmux 当前运行实例

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | tmux 当前运行实例 |
| 2 | 是什么 | 现有依赖图将其记录为3.2 命令/终端 / tmux复用支路节点；身份状态与证据字段：2026-10-15T00:45:37Z观察：PATH入口与realpath均为/usr/bin/tmux；dpkg确认由tmux 3.4-1ubuntu0.1（amd64）提供，二进制SHA-256为034b15c64035f783d43862f2775eb4828f61571ca62c8199796000b97d556ecd。关联的faqi-tmux固定submodule为615c27c11789948df2db09e113e882f82dfb3e1c，其configure.ac声明next-3.7；本机运行实例与该固定来源并非同一版本，烟测不验证submodule实现或效果。 |
| 3 | 为什么 | 待核：观察记录未说明采用动机；节点、版本和重要性依据不能替代问题价值证据。 |
| 4 | 怎么做 | 待核：依赖图节点/观测版本不描述端到端使用步骤；当前没有同版本、同环境的运行操作记录。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 依赖图对象ID=dep-tmux-runtime；图节点=3.2 命令/终端 / tmux复用支路；身份状态=runtime&#95;observed；观测版本=3.4；相关本地对象=faqi-tmux。<br>Vibe Coding 重要性暂定：黄阶高级（grade&#95;id=faqi-huang-advanced；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：长任务与多会话终端复用；分级依据：可持久化和并行组织终端工作，复杂协作时有价值；普通单会话开发可替代，不属于核心生成链。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。 |
| 7 | 出处 | 依赖图来源：{<br>  "source&#95;path": ".github/docs/gongfa/technology-stack.md",<br>  "source&#95;sha256": "88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2",<br>  "source&#95;anchor": "reference-technology-stack-十六技术栈的层级结构",<br>  "observed&#95;at": "2026-10-10T12:14:00Z"<br>}<br>依赖图对象记录：{<br>  "id": "dep-tmux-runtime",<br>  "name": "tmux 当前运行实例",<br>  "type&#95;id": "software-artifact",<br>  "graph&#95;node": "3.2 命令/终端 / tmux复用支路",<br>  "identity&#95;status": "runtime&#95;observed",<br>  "version": "3.4",<br>  "evidence": "2026-10-15T00:45:37Z观察：PATH入口与realpath均为/usr/bin/tmux；dpkg确认由tmux 3.4-1ubuntu0.1（amd64）提供，二进制SHA-256为034b15c64035f783d43862f2775eb4828f61571ca62c8199796000b97d556ecd。关联的faqi-tmux固定submodule为615c27c11789948df2db09e113e882f82dfb3e1c，其configure.ac声明next-3.7；本机运行实例与该固定来源并非同一版本，烟测不验证submodule实现或效果。",<br>  "resource&#95;ids": &#91;&#93;,<br>  "related&#95;object&#95;id": "faqi-tmux",<br>  "grade&#95;id": null,<br>  "grade&#95;status": "pending",<br>  "grade&#95;reason": "运行实例与固定源码身份尚未桥接；任务族结果带与分级量表阈值未校准。"<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "dep-tmux-runtime",<br>  "grade&#95;id": "faqi-huang-advanced",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：长任务与多会话终端复用",<br>  "basis": "可持久化和并行组织终端工作，复杂协作时有价值；普通单会话开发可替代，不属于核心生成链。"<br>}<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：依赖图记录不含设计决策依据；不得从依赖关系反推设计意图。 |
| 11 | 内部如何实现？ | 待核：已登记的是观察到的节点、版本与关系；没有足以说明内部调用、数据流和状态机制的证据。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 观察证据/边界（原记录）：2026-10-15T00:45:37Z观察：PATH入口与realpath均为/usr/bin/tmux；dpkg确认由tmux 3.4-1ubuntu0.1（amd64）提供，二进制SHA-256为034b15c64035f783d43862f2775eb4828f61571ca62c8199796000b97d556ecd。关联的faqi-tmux固定submodule为615c27c11789948df2db09e113e882f82dfb3e1c，其configure.ac声明next-3.7；本机运行实例与该固定来源并非同一版本，烟测不验证submodule实现或效果。<br>版本/身份字段仅按依赖图记录呈现；未据此推断当前环境中正在运行。<br>重要性纳入范围：Vibe Coding重要性：长任务与多会话终端复用<br>待核：版本、平台、配置、权限、协议及工作负载条件尚未按具体环境验证。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-faqi-auto-tmux-09bb1add"></a>
### auto-tmux命令封装程序

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | auto-tmux命令封装程序 |
| 2 | 是什么 | 现有登记将其界定为软件工件：指统一操控脚本，不是SKILL.md、tmux二进制、session/pane或某次操作；支持多命令不增加身份。未发送按键、创建会话或读取pane。<br>此处复述登记边界，不证明当前可安装、可运行或有效。 |
| 3 | 为什么 | 待核：未记录为何采用该程序/配置；重要性范围与分级依据不等于采用动机。 |
| 4 | 怎么做 | 待核：登记冻结了源码选区，但没有验证该对象当前完整的调用方式、输入输出与安全前提；选区本身不是操作手册。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 法器对象ID=faqi-auto-tmux；本体类型=software-artifact；版本声明=未声明；本地入口=.github/skills/auto-tmux；当前运行实例/部署状态未在对象记录中声明。<br>Vibe Coding 重要性暂定：黄阶高级（grade&#95;id=faqi-huang-advanced；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：多会话终端协作自动化；分级依据：多会话与worker协作在复杂并行时有用，但基础单Agent编码有替代路径；本级只表达工作流重要性，不评价实现质量或效能。不代表效能评级、运行结果或质量结论。<br>既有关系记录：{<br>  "subject": "faqi-auto-tmux",<br>  "predicate": "requires",<br>  "target&#95;label": "tmux程序（运行版本未知）",<br>  "related&#95;object&#95;id": "faqi-tmux",<br>  "evidence": "S13",<br>  "boundary": "脚本调用PATH中的tmux；本地上游源码仅作相关参照，不证明实际安装二进制来自该修订。"<br>}<br>来源ID：S12, S11。 |
| 7 | 出处 | 固定实现/佐证来源记录：{<br>  "id": "S12",<br>  "purpose": "implementation",<br>  "path": ".github/skills/auto-tmux/scripts/auto-tmux.sh",<br>  "repository": ".",<br>  "revision": "0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2",<br>  "sha256": "f473fddada7a7f5fd85afe94deccd16e2aba26195423dc87afbac176315b6567",<br>  "lines": &#91;<br>    701,<br>    725<br>  &#93;,<br>  "selection&#95;sha256": "701db6430b20faa4bf2477001f584b15a1dea31e6c4a9d32747be343988dd3c2"<br>}；{<br>  "id": "S11",<br>  "purpose": "support",<br>  "path": ".github/skills/auto-tmux/README.md",<br>  "repository": ".",<br>  "revision": "0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2",<br>  "sha256": "d21ca4f1c4adb6a799a76f7a7446b1ebca70d2402f73e80600cda1c2a6d24c25",<br>  "lines": &#91;<br>    1,<br>    18<br>  &#93;,<br>  "selection&#95;sha256": "0c0e46b950949789a6b85addd85f3a9ec0b2945e6a44134f82c7b46acc59b308"<br>}<br>本地入口记录：{<br>  "path": ".github/skills/auto-tmux",<br>  "objects": &#91;<br>    "faqi-auto-tmux"<br>  &#93;,<br>  "sources": &#91;<br>    "S11",<br>    "S12",<br>    "S13"<br>  &#93;,<br>  "boundary": "Skill方法/规约、执行脚本、被依赖程序及运行入口分别指认。",<br>  "pending": &#91;<br>    "蜂群附属脚本不逐一登记，不启动蜂群，也不将蜂群状态/日志算软件。",<br>    "2026-10-13：将本工作分支内26个.sh入口的Git执行模式从100644改为100755；auto-tmux doctor、26个脚本bash -n及两个help入口通过。完整技能validator与tmux smoke未运行，运行效果仍待验证。"<br>  &#93;<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "faqi-auto-tmux",<br>  "grade&#95;id": "faqi-huang-advanced",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：多会话终端协作自动化",<br>  "basis": "多会话与worker协作在复杂并行时有用，但基础单Agent编码有替代路径；本级只表达工作流重要性，不评价实现质量或效能。"<br>}<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：登记未记录设计者为何选择该结构/接口/依赖；不能从被登记为重要推断其设计意图。 |
| 11 | 内部如何实现？ | 待核：当前仅有固定源码选区及SHA登记；尚未沿调用者、数据流、状态与失败路径完成实现链分析。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 登记边界（原字段）：指统一操控脚本，不是SKILL.md、tmux二进制、session/pane或某次操作；支持多命令不增加身份。未发送按键、创建会话或读取pane。<br>重要性纳入范围：Vibe Coding重要性：多会话终端协作自动化<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。<br>待核：具体操作系统、依赖版本、权限、输入规模和部署配置须按实际来源及工作负载核验。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-faqi-tmux-fbe1a81c"></a>
### tmux终端复用程序

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | tmux终端复用程序 |
| 2 | 是什么 | 现有登记将其界定为软件工件：指固定源码修订的程序内容，不是物理终端、pane、socket地址或一次会话。Git describe的邻近tag不作为已核发布版本。<br>此处复述登记边界，不证明当前可安装、可运行或有效。 |
| 3 | 为什么 | 待核：未记录为何采用该程序/配置；重要性范围与分级依据不等于采用动机。 |
| 4 | 怎么做 | 待核：登记冻结了源码选区，但没有验证该对象当前完整的调用方式、输入输出与安全前提；选区本身不是操作手册。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 法器对象ID=faqi-tmux；本体类型=software-artifact；版本声明=未声明；本地入口=.github/tools/external/tmux；当前运行实例/部署状态未在对象记录中声明。；当前资源关联ID=repo-rules-scaffolds-tmux-9f36981a（关联不等于许可或运行证明）。<br>Vibe Coding 重要性暂定：黄阶高级（grade&#95;id=faqi-huang-advanced；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：可选的多会话终端复用；分级依据：支持持久终端与多窗口工作流，复杂长任务可受益；普通编码闭环有替代方案，不属定义性核心。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。<br>关联资源ID：repo-rules-scaffolds-tmux-9f36981a。资源链接/本地关联不证明许可、兼容性或功能等价。<br>来源ID：S21, S20, S40, S41, S52, S53, S54, S55, S56, S57, S58, S59, S60, S61, S62, S63, S64。 |
| 7 | 出处 | 固定实现/佐证来源记录：{<br>  "id": "S21",<br>  "purpose": "implementation",<br>  "path": ".github/tools/external/tmux/tmux.c",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "58a9bef0d1d424fd2e2a79c6d998dab96aab81ee771b7c2653928451f3bf11a8",<br>  "lines": &#91;<br>    350,<br>    492<br>  &#93;,<br>  "selection&#95;sha256": "cd3c886c9a155f70dcddaeec88b4a86253c565b2e18753327f83446d92a7e8f4"<br>}；{<br>  "id": "S20",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/README",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "9fb75e6c7f10c25b73e41b8214336d0dc2acfbe4c99984514ccaf7327192d53e",<br>  "lines": &#91;<br>    1,<br>    20<br>  &#93;,<br>  "selection&#95;sha256": "68e51dd5a0148fa1d22f5c7565d3da74dc6619207d1c5238658d5fd873c63e5b"<br>}；{<br>  "id": "S40",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/tmux.c",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "58a9bef0d1d424fd2e2a79c6d998dab96aab81ee771b7c2653928451f3bf11a8",<br>  "lines": &#91;<br>    1,<br>    18<br>  &#93;,<br>  "selection&#95;sha256": "26f34506da997905b214b2878416c618a92298533aca335c60c509e5e0993904"<br>}；{<br>  "id": "S41",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/COPYING",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "c031bd37f464c534277814f6aa38686fa023d094261d57fd2545ad592bb53ccd",<br>  "lines": &#91;<br>    1,<br>    19<br>  &#93;,<br>  "selection&#95;sha256": "c031bd37f464c534277814f6aa38686fa023d094261d57fd2545ad592bb53ccd"<br>}；{<br>  "id": "S52",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/README",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "9fb75e6c7f10c25b73e41b8214336d0dc2acfbe4c99984514ccaf7327192d53e",<br>  "lines": &#91;<br>    84,<br>    88<br>  &#93;,<br>  "selection&#95;sha256": "68980459b47c2af6f48f099a70fa4472b3b6e5066006f7fdf5f63f675dc1f02d"<br>}；{<br>  "id": "S53",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/compat/explicit&#95;bzero.c",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "7e30bc63946093cd6ed7cb4ce01d2f8c6e329ab173a20df250da60bb0a3c757b",<br>  "lines": &#91;<br>    1,<br>    6<br>  &#93;,<br>  "selection&#95;sha256": "02fedc95bf0da5dffe09623d9cb71bc7ebbb8bfd31f5e4fb5a23b135d7f36d0e"<br>}；{<br>  "id": "S54",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/compat/getopt&#95;long.c",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "0486066fe70fb5a81d79971842f171e3bdcb570dbcab22ce51c1394235b8d21f",<br>  "lines": &#91;<br>    1,<br>    98<br>  &#93;,<br>  "selection&#95;sha256": "32af441d6bffc37dbac1c14d03edf334137d91c95fa06c335479fd9c80d7fcb4"<br>}；{<br>  "id": "S55",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/xmalloc.c",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "8ed468e9903b8abf18d5d5b76d99f030713fc479d02dc107ec3dbaa3a01c702b",<br>  "lines": &#91;<br>    1,<br>    15<br>  &#93;,<br>  "selection&#95;sha256": "f28a22fd0a1176583b24e17d8536acaba14afb635f4b253aa9653770cb1449ba"<br>}；{<br>  "id": "S56",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/logo/LICENSE",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "5fdf604dee98da6f827ea924cf5ae19a9da31555d3814143f2cc6f8e7ee05752",<br>  "lines": &#91;<br>    1,<br>    14<br>  &#93;,<br>  "selection&#95;sha256": "5fdf604dee98da6f827ea924cf5ae19a9da31555d3814143f2cc6f8e7ee05752"<br>}；{<br>  "id": "S57",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/mdoc2man.awk",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "602f3d31ffec414850e697b73f1885e967698ac0cbe8f09efd14800e55abe7ea",<br>  "lines": &#91;<br>    1,<br>    23<br>  &#93;,<br>  "selection&#95;sha256": "1d4514630b480519684226c19c6ead79afcc30d0a5857601aa2e40b3831f7b92"<br>}；{<br>  "id": "S58",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/tmux.1",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "f2966da7a8267abc9aaa216a7a7b46d4d914d60114058dc046c4ff1c75ac9422",<br>  "lines": &#91;<br>    1,<br>    15<br>  &#93;,<br>  "selection&#95;sha256": "04972c3c428ff5c92813b5cc03ee0aca9fb4d67f9efcadc6b08ba9ae9ad1a6db"<br>}；{<br>  "id": "S59",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/example&#95;tmux.conf",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "0ab7c28342180d485434c3d8e286508a1e1c87ac9a2c8f2dc78bcf477a2de437",<br>  "lines": &#91;<br>    1,<br>    5<br>  &#93;,<br>  "selection&#95;sha256": "c29f86d0a16523c1ec7df3be70be2c1b0c7c60aa5da95abb23ff3239289beb78"<br>}；{<br>  "id": "S60",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/tools/24-bit-color.sh",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "cee34d321461577c2455573ec58537833f5968cebe7df8d53aabf08b0e0d9ccf",<br>  "lines": &#91;<br>    1,<br>    15<br>  &#93;,<br>  "selection&#95;sha256": "d78c7405e325b792164f733359cfb3339460776aaee44586bddb7d221c15f354"<br>}；{<br>  "id": "S61",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/README.ja",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "c341a10636227e426a759da4b80b754258ef31f1554a9ac369a79c5afeeadeb6",<br>  "lines": &#91;<br>    59,<br>    60<br>  &#93;,<br>  "selection&#95;sha256": "63f1ffb13bd10f6b3a2052d09b4d9c336c41c45262363e035e25a362ffd5c73a"<br>}；{<br>  "id": "S62",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/logo/tmux-logo-1-color.eps",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "f4da0cd411ea21140efbb3ebd5fc9a76c87183c8eceb7902e6f08d061c17235b",<br>  "lines": &#91;<br>    1,<br>    20<br>  &#93;,<br>  "selection&#95;sha256": "2c23a57c4e1dfdf7fdf3d45d0d4cb092413835ab36eb320a3cc25d80b393f0d4"<br>}；{<br>  "id": "S63",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/logo/tmux-logo.eps",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "13ecb5c04f2b40f5dca7dc7e9be3986de3d7641c6494cc3f139669a3e90dd144",<br>  "lines": &#91;<br>    1,<br>    20<br>  &#93;,<br>  "selection&#95;sha256": "2c23a57c4e1dfdf7fdf3d45d0d4cb092413835ab36eb320a3cc25d80b393f0d4"<br>}；{<br>  "id": "S64",<br>  "purpose": "support",<br>  "path": ".github/tools/external/tmux/logo/tmux-logomark.eps",<br>  "repository": ".github/tools/external/tmux",<br>  "revision": "615c27c11789948df2db09e113e882f82dfb3e1c",<br>  "sha256": "f5afbd939a1675b5b1293cd642273d8b0b9555b906683970b5e7a34f802674fd",<br>  "lines": &#91;<br>    1,<br>    20<br>  &#93;,<br>  "selection&#95;sha256": "ecbd0ccba3e5665b62c06509dd78ed90525ad60737c63c29d089fb8b54e23b5b"<br>}<br>本地入口记录：{<br>  "path": ".github/tools/external/tmux",<br>  "objects": &#91;<br>    "faqi-tmux"<br>  &#93;,<br>  "sources": &#91;<br>    "S20",<br>    "S21",<br>    "S40",<br>    "S41",<br>    "S52",<br>    "S53",<br>    "S54",<br>    "S55",<br>    "S56",<br>    "S57",<br>    "S58",<br>    "S59",<br>    "S60",<br>    "S61",<br>    "S62",<br>    "S63",<br>    "S64"<br>  &#93;,<br>  "boundary": "tmux程序与配置、操控封装、终端会话和显示记录分开。",<br>  "pending": &#91;<br>    "S40仅绑定tmux.c文件头许可选区；S41明确COPYING仅供信息参考、许可依文件头。2026-10-15第一轮固定pin许可清点见S52–S56；此轮未覆盖全部313文件、非C/H/Y资产、所有上游来源及再分发兼容性，limits.license&#95;approved仍为false。",<br>    "2026-10-15：pin 615c27c11789948df2db09e113e882f82dfb3e1c有313个tracked文件、无嵌套gitlink。对196个C/H/Y文件作固定字面扫描：182个含ISC式授权句、13个含BSD式再分发句（compat/daemon-darwin.c与compat/getopt&#95;long.c同时含两种），另有xmalloc.c（S55）/xmalloc.h（sha256 8d0a589c43e16549174b0ffb0b59a8581af00d99eb912205bfb4f293502bbeae）的Tatu Ylonen特殊使用与命名条件、compat/explicit&#95;bzero.c的Public domain声明；BSD式文件为compat/bitstring.h、compat/daemon-darwin.c、compat/daemon.c、compat/getline.c、compat/getopt&#95;long.c、compat/memmem.c、compat/queue.h、compat/strcasestr.c、compat/strsep.c、compat/tree.h、compat/unvis.c、compat/vis.c、compat/vis.h。README (S52)、COPYING (S41) 与 README.ja（sha256 c341a10636227e426a759da4b80b754258ef31f1554a9ac369a79c5afeeadeb6）列举的ISC例外不同；README.ja还列出SYNCING（sha256 5243f70e3adbb2f7554e99889d3ea9b5b719d50108ac127db1392ced65e7c61c），本轮未见该文件头许可声明；FAQ/TODO未跟踪。logo/LICENSE由S56单独绑定。getopt&#95;long.c（S54）自述来源于OpenSSH commit b5b405fee7f3e79d44e2d2971a4b6b4cc53f112e，本轮未独立比对上游。该清点是有限静态检索而非法律兼容性意见；正式许可批准、完整文件级/第三方依赖审查仍未完成。",<br>    "2026-10-15第二轮固定pin非C/H/Y许可线索见S57–S64：仅审117个非C/H/Y tracked文件中的8个选区。mdoc2man.awk与tmux.1含逐文件版权、permission及免责声明；example&#95;tmux.conf由作者声明Public domain；tools/24-bit-color.sh标注来源为iTerm2的master并称“presumably covered”于其LICENSE，未冻结或核对上游修订/条款；README.ja:59将本文件、CHANGES、FAQ、SYNCING、TODO列为ISC许可对象，与英文COPYING/README的列举不同；三个EPS文件头各自声明Apple 2000–2004 Copyright/All Rights Reserved，未证实logo/LICENSE是否覆盖。未审其余非C/H/Y文件、其他二进制资产及第三方依赖；不构成完整文件/权利/再分发兼容性审查，limits.license&#95;approved仍为false。"<br>  &#93;<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "faqi-tmux",<br>  "grade&#95;id": "faqi-huang-advanced",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：可选的多会话终端复用",<br>  "basis": "支持持久终端与多窗口工作流，复杂长任务可受益；普通编码闭环有替代方案，不属定义性核心。"<br>}<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：登记未记录设计者为何选择该结构/接口/依赖；不能从被登记为重要推断其设计意图。 |
| 11 | 内部如何实现？ | 待核：当前仅有固定源码选区及SHA登记；尚未沿调用者、数据流、状态与失败路径完成实现链分析。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 登记边界（原字段）：指固定源码修订的程序内容，不是物理终端、pane、socket地址或一次会话。Git describe的邻近tag不作为已核发布版本。<br>重要性纳入范围：Vibe Coding重要性：可选的多会话终端复用<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。<br>待核：具体操作系统、依赖版本、权限、输入规模和部署配置须按实际来源及工作负载核验。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-faqi-oh-my-tmux-3ab56947"></a>
### oh-my-tmux可执行配置程序

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | oh-my-tmux可执行配置程序 |
| 2 | 是什么 | 现有登记将其界定为软件工件：配置文件含run、cut&#124;sh调用链及可执行shell指令，按实际程序内容归software-artifact，不能仅因.conf后缀归纯规约；不是tmux本身。仓内.logo许可证另由S65绑定；其指向可变tmux/master路径，具体SVG来源关系与许可覆盖范围未核，不能据此批准仓库整体再分发。<br>此处复述登记边界，不证明当前可安装、可运行或有效。 |
| 3 | 为什么 | 待核：未记录为何采用该程序/配置；重要性范围与分级依据不等于采用动机。 |
| 4 | 怎么做 | 待核：登记冻结了源码选区，但没有验证该对象当前完整的调用方式、输入输出与安全前提；选区本身不是操作手册。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 法器对象ID=faqi-oh-my-tmux；本体类型=software-artifact；版本声明=未声明；本地入口=.github/tools/external/.tmux；当前运行实例/部署状态未在对象记录中声明。<br>Vibe Coding 重要性暂定：黄阶中级（grade&#95;id=faqi-huang-intermediate；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：终端复用器体验配置；分级依据：改善tmux使用便利性，但不提供模型推理或核心代码执行能力，可由其他终端配置替代。不代表效能评级、运行结果或质量结论。<br>既有关系记录：{<br>  "subject": "faqi-oh-my-tmux",<br>  "predicate": "requires",<br>  "target&#95;label": "tmux&gt;=2.6及awk/perl/grep/sed",<br>  "related&#95;object&#95;id": "faqi-tmux",<br>  "evidence": "S17",<br>  "boundary": "README声明版本下限，不将配置修订误写成tmux版本，也不保证当前环境满足依赖。"<br>}<br>来源ID：S18, S17, S19, S37, S38, S39, S65。 |
| 7 | 出处 | 固定实现/佐证来源记录：{<br>  "id": "S18",<br>  "purpose": "implementation",<br>  "path": ".github/tools/external/.tmux/.tmux.conf",<br>  "repository": ".github/tools/external/.tmux",<br>  "revision": "87dcd13a28aeb5f18baee630e24b3f5765ae3a4f",<br>  "sha256": "6807d44735b7b11e64c4488a0c3fdcbd2809cc73efedcc349d098e80a690aeeb",<br>  "lines": &#91;<br>    150,<br>    190<br>  &#93;,<br>  "selection&#95;sha256": "e39dd4f98da410b88e110772d21d1eb14d3bfb6e2c6e8c36e2cb19129d9c98f8"<br>}；{<br>  "id": "S17",<br>  "purpose": "support",<br>  "path": ".github/tools/external/.tmux/README.md",<br>  "repository": ".github/tools/external/.tmux",<br>  "revision": "87dcd13a28aeb5f18baee630e24b3f5765ae3a4f",<br>  "sha256": "10b0cca6bb2a4ab7af39d76d27f51b91ca1df4dead015315400041695c9471e7",<br>  "lines": &#91;<br>    9,<br>    78<br>  &#93;,<br>  "selection&#95;sha256": "243d5ab2936723c61f781dd6906e61de92cceea6069e570ca107b6c19236aeb7"<br>}；{<br>  "id": "S19",<br>  "purpose": "support",<br>  "path": ".github/tools/external/.tmux/.tmux.conf",<br>  "repository": ".github/tools/external/.tmux",<br>  "revision": "87dcd13a28aeb5f18baee630e24b3f5765ae3a4f",<br>  "sha256": "6807d44735b7b11e64c4488a0c3fdcbd2809cc73efedcc349d098e80a690aeeb",<br>  "lines": &#91;<br>    1829,<br>    1891<br>  &#93;,<br>  "selection&#95;sha256": "3065f39bd62e8cb3bb4095dfaf9784840368d5760137ad01d3f96eb55ede68a1"<br>}；{<br>  "id": "S37",<br>  "purpose": "support",<br>  "path": ".github/tools/external/.tmux/.tmux.conf",<br>  "repository": ".github/tools/external/.tmux",<br>  "revision": "87dcd13a28aeb5f18baee630e24b3f5765ae3a4f",<br>  "sha256": "6807d44735b7b11e64c4488a0c3fdcbd2809cc73efedcc349d098e80a690aeeb",<br>  "lines": &#91;<br>    1,<br>    8<br>  &#93;,<br>  "selection&#95;sha256": "e9e4b5dd6be906cfd6c4e4fe0a1063332cad79bf10898087c7c88eee87fb11aa"<br>}；{<br>  "id": "S38",<br>  "purpose": "support",<br>  "path": ".github/tools/external/.tmux/LICENSE.MIT",<br>  "repository": ".github/tools/external/.tmux",<br>  "revision": "87dcd13a28aeb5f18baee630e24b3f5765ae3a4f",<br>  "sha256": "f4c34427d3e29630cece9bca418eda48ac298867630cd6698d73e0f04642d1d0",<br>  "lines": &#91;<br>    1,<br>    19<br>  &#93;,<br>  "selection&#95;sha256": "f4c34427d3e29630cece9bca418eda48ac298867630cd6698d73e0f04642d1d0"<br>}；{<br>  "id": "S39",<br>  "purpose": "support",<br>  "path": ".github/tools/external/.tmux/LICENSE.WTFPLv2",<br>  "repository": ".github/tools/external/.tmux",<br>  "revision": "87dcd13a28aeb5f18baee630e24b3f5765ae3a4f",<br>  "sha256": "ee820ff0db4ce628569e0975ac27dc926052a9f85d102b101edb104311ef4d90",<br>  "lines": &#91;<br>    1,<br>    14<br>  &#93;,<br>  "selection&#95;sha256": "ee820ff0db4ce628569e0975ac27dc926052a9f85d102b101edb104311ef4d90"<br>}；{<br>  "id": "S65",<br>  "purpose": "support",<br>  "path": ".github/tools/external/.tmux/.logo/LICENSE",<br>  "repository": ".github/tools/external/.tmux",<br>  "revision": "87dcd13a28aeb5f18baee630e24b3f5765ae3a4f",<br>  "sha256": "6ae92da1ac8fc251f218491c42048d258d50d57bc685beb871fb09adf0bcea3e",<br>  "lines": &#91;<br>    1,<br>    17<br>  &#93;,<br>  "selection&#95;sha256": "6ae92da1ac8fc251f218491c42048d258d50d57bc685beb871fb09adf0bcea3e"<br>}<br>本地入口记录：{<br>  "path": ".github/tools/external/.tmux",<br>  "objects": &#91;<br>    "faqi-oh-my-tmux"<br>  &#93;,<br>  "sources": &#91;<br>    "S17",<br>    "S18",<br>    "S19",<br>    "S37",<br>    "S38",<br>    "S39"<br>  &#93;,<br>  "boundary": "配置数据与嵌入程序按实际所指区分；本条纳入可执行配置程序，未安装或source配置。",<br>  "pending": &#91;<br>    "源码含条件性kill-server；纳入不等于可安全对当前会话执行。"<br>  &#93;<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "faqi-oh-my-tmux",<br>  "grade&#95;id": "faqi-huang-intermediate",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：终端复用器体验配置",<br>  "basis": "改善tmux使用便利性，但不提供模型推理或核心代码执行能力，可由其他终端配置替代。"<br>}<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：登记未记录设计者为何选择该结构/接口/依赖；不能从被登记为重要推断其设计意图。 |
| 11 | 内部如何实现？ | 待核：当前仅有固定源码选区及SHA登记；尚未沿调用者、数据流、状态与失败路径完成实现链分析。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 登记边界（原字段）：配置文件含run、cut&#124;sh调用链及可执行shell指令，按实际程序内容归software-artifact，不能仅因.conf后缀归纯规约；不是tmux本身。仓内.logo许可证另由S65绑定；其指向可变tmux/master路径，具体SVG来源关系与许可覆盖范围未核，不能据此批准仓库整体再分发。<br>重要性纳入范围：Vibe Coding重要性：终端复用器体验配置<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。<br>待核：具体操作系统、依赖版本、权限、输入规模和部署配置须按实际来源及工作负载核验。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

<a id="v0-faqi-faqi-prompt-converter-43a9d077"></a>
### 提示词格式转换程序

| 序号 | 说明项 | 内容 |
|:---:|:---|:---|
| 1 | 工具的名称 | 提示词格式转换程序 |
| 2 | 是什么 | 现有登记将其界定为软件工件：指main.py及其转换实现所表达的程序内容；Excel、Markdown和JSONL是输入/输出，不随转换模式复制工具身份。未验证转换正确性。<br>此处复述登记边界，不证明当前可安装、可运行或有效。 |
| 3 | 为什么 | 待核：未记录为何采用该程序/配置；重要性范围与分级依据不等于采用动机。 |
| 4 | 怎么做 | 待核：登记冻结了源码选区，但没有验证该对象当前完整的调用方式、输入输出与安全前提；选区本身不是操作手册。 |
| 5 | 扩展 | 待核：既有对象登记/依赖图未提供经核实的可选能力、扩展方式或组合契约；不把佐证依赖当作默认启用能力。 |
| 6 | 关联信息 | 法器对象ID=faqi-prompt-converter；本体类型=software-artifact；版本声明=未声明；本地入口=.github/tools/prompts-library；当前运行实例/部署状态未在对象记录中声明。<br>Vibe Coding 重要性暂定：黄阶初级（grade&#95;id=faqi-huang-initial；状态=user&#95;directed&#95;provisional）；范围：Vibe Coding重要性：提示词资产格式迁移的辅助支路；分级依据：只负责格式转换，能维护和复用提示词资产但不参与模型推理或代码执行；替代方式多，属低重要性辅助。不代表效能评级、运行结果或质量结论。<br>既有关系记录：未记录对象关系。<br>来源ID：S02, S01。 |
| 7 | 出处 | 固定实现/佐证来源记录：{<br>  "id": "S02",<br>  "purpose": "implementation",<br>  "path": ".github/tools/prompts-library/main.py",<br>  "repository": ".",<br>  "revision": "0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2",<br>  "sha256": "ed0113d3ecbe9c9d4ca48ee7dde2c76c9a6fd1f54a1ae890fd3689d617347691",<br>  "lines": &#91;<br>    625,<br>    689<br>  &#93;,<br>  "selection&#95;sha256": "757b82c3bba30f1d62359c39f7c110d425463326e854acef2de085f14d90cf6d"<br>}；{<br>  "id": "S01",<br>  "purpose": "support",<br>  "path": ".github/tools/prompts-library/README.md",<br>  "repository": ".",<br>  "revision": "0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2",<br>  "sha256": "4c2d5f97a6cfa67e033e166676d12eeaab6a562fa83c39b0f2474ae2afbcdae2",<br>  "lines": &#91;<br>    1,<br>    95<br>  &#93;,<br>  "selection&#95;sha256": "4c2d5f97a6cfa67e033e166676d12eeaab6a562fa83c39b0f2474ae2afbcdae2"<br>}<br>本地入口记录：{<br>  "path": ".github/tools/prompts-library",<br>  "objects": &#91;<br>    "faqi-prompt-converter"<br>  &#93;,<br>  "sources": &#91;<br>    "S01",<br>    "S02"<br>  &#93;,<br>  "boundary": "纳入程序，不把提示词资产或生成目录当工具实现。",<br>  "pending": &#91;&#93;<br>}<br>重要性分级记录：{<br>  "subject&#95;id": "faqi-prompt-converter",<br>  "grade&#95;id": "faqi-huang-initial",<br>  "assignment&#95;status": "user&#95;directed&#95;provisional",<br>  "scope": "Vibe Coding重要性：提示词资产格式迁移的辅助支路",<br>  "basis": "只负责格式转换，能维护和复用提示词资产但不参与模型推理或代码执行；替代方式多，属低重要性辅助。"<br>}<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。 |
| 8 | 相关图书 | 待核：法器登记未提供与本对象直接对应且核验过的作者、书名、版本或章节；技术来源见第7项，不臆造图书。 |
| 9 | 它要解决什么问题？ | 待核：当前登记记录的是对象边界/依赖角色及重要性范围，不足以单独定义问题场景、输入约束和目标结果。 |
| 10 | 为什么这样设计？ | 待核：登记未记录设计者为何选择该结构/接口/依赖；不能从被登记为重要推断其设计意图。 |
| 11 | 内部如何实现？ | 待核：当前仅有固定源码选区及SHA登记；尚未沿调用者、数据流、状态与失败路径完成实现链分析。 |
| 12 | 付出了什么代价？ | 待核：没有完成针对该对象的资源、时间、维护成本或副作用测量；不能将源码规模、级别或依赖数量冒充运行成本。 |
| 13 | 比较不同技术与方法。 | 待核：尚未为相同问题与环境建立可比替代方案；依赖关系或资源登记不代表优劣比较。 |
| 14 | 提炼共同规律。 | 待核：缺少有界、同口径的多方案比较；不从单个实现或抽象类别推出普遍规律。 |
| 15 | 明确这些规律成立的前提与适用条件。 | 登记边界（原字段）：指main.py及其转换实现所表达的程序内容；Excel、Markdown和JSONL是输入/输出，不随转换模式复制工具身份。未验证转换正确性。<br>重要性纳入范围：Vibe Coding重要性：提示词资产格式迁移的辅助支路<br>运行/部署状态未由此登记证明；版本或路径记录不等于本次运行验证。<br>待核：具体操作系统、依赖版本、权限、输入规模和部署配置须按实际来源及工作负载核验。<br>若建立共同规律，须先核实同一问题、版本、环境、权限、协议及工作负载，并记录反例/不适用条件。 |

## 原始说明

> 文集保留历史正文；已退役实现的相关链接指向已发布的固定Git修订，不是当前安装或运行入口。现存程序以Extensions清单为准。

<a id="doc-faqi-system"></a>
## Vibe Coding 法器体系说明

原始文集：`.github/docs/gongfa/faqi-system.md`；下文为阅读呈现，原字节和来源保存在[data.json](data.json)。

<a id="doc-faqi-system-vibe-coding-法器体系说明"></a>
**Vibe Coding 法器体系说明**

本文说明法器总表的对象边界、重要性分级和维护入口；具体来源事实与逐条分组以登记源和生成总表为准。

<a id="doc-faqi-system-一句话"></a>
**一句话**

法器总表整理 Vibe Coding 流程中使用或依赖的工具、可调用入口及依赖类别，帮助读者理解它们在工作流中的位置。品级按对 Vibe Coding 的重要性暂定，不代表工具质量、运行可用性或任务效果。

<a id="doc-faqi-system-字多不看"></a>
**字多不看**

- 当前实现退役补充：用户点名的chat-vault、my-nvim、codex-config、MCPlayerTransfer、XHS-image-to-PDF-conversion、两个xhs图文HTML及html-tools-main说明共8项已移除。对应当前路径和实现绑定已清理；原来源、选区、初审、排除与重要性保留为历史，不表示Codex安装器或这些旧工具仍可使用。
- 当前实现退役：原auto-skill模板生成/结构校验、Skill Seekers本地适配和auto-tmux命令封装已经从Extensions移除。原30项重要性及固定来源初审保留为历史，不表示这些旧程序当前可执行；两个Skill改用原生工具与规范指令，独立初始化器和锁定上游继续保留。
- 方法和能力要求归功法；工具、软件入口及依赖类别按其真实所指另行整理，不因出现在同一依赖图就变成同一种对象。
- 当前 30 项按重要性分为天阶 4 项、地阶 12 项、玄阶 9 项、黄阶 5 项；品级、名称、重要性范围与分级依据见[法器浏览表](#法器总表)，完整登记见[法器登记源](data.json)。
- 天阶强调模型推理与 Agent 协作；地阶强调代码操作、工具执行和运行基础；玄阶强调上下文、验证、复用与产品交付；黄阶强调可替代的专用或便利能力。
- 每阶高级、中级、初级表示该阶内的重要性次序，不是测试结果带或效能等级。
- 当前重要性分级与正式任务效果评级是两条独立轴；正式效能量表仍为 draft，阈值尚未校准。

<a id="doc-faqi-system-对象边界"></a>
**对象边界**

“法器”是本项目用于组织 Vibe Coding 工具与依赖能力的领域称呼，不等同于某个统一产品类别。登记必须按具体所指区分程序内容、当前运行实例、模型制品、服务/API、硬件资源、候选对象和抽象依赖类别。

总表中的不同记录不能仅凭名称、依赖图位置或功能相似而合并：

- **来源限定实现**：绑定选定的仓内来源和代码内容，不自动代表本机运行版本。
- **运行实例或具名候选**：记录实际观察到的入口，或依赖图中指向的候选；候选身份、版本和来源可能仍待核。
- **依赖类别**：例如模型服务、CI 平台、终端接口或检索记忆。用户确认类别纳入范围，不等于确认了某个产品、部署、账号或可用实现。
- **外部资源行**：索引原资源记录，不等同于一件独立法器，也不单独证明能力、许可或运行效果。

法器不替代功法、任务合同或权限。建议使用某种工具，不代表它是唯一依赖、已获授权或已通过验证；执行一个过程也不自动证明预期效果。

<a id="doc-faqi-system-重要性分级"></a>
**重要性分级**

本次排序面向一般 Vibe Coding 工作流，综合考虑条目在核心闭环中的作用、对代码执行和验证的支撑程度、适用范围及可替代性。分级是用户确认的导航性判断，并非从版本新旧、依赖图深度、代码规模或烟测结果计算出来的分数。

| 品级方向 | 重要性含义 | 常见角色 |
|---|---|---|
| 天阶 | 决定核心 AI 协作链能否成立 | 模型推理、Agent 运行与编排 |
| 地阶 | 支撑代码真正被操作、运行和管理 | 终端命令、PTY、版本控制、语言与运行环境 |
| 玄阶 | 扩展复杂任务的上下文、质量和交付范围 | 检索记忆、自动验证、技能复用、部署与数据集成 |
| 黄阶 | 对特定工作方式有帮助，但通常存在替代路径 | 多会话终端、专用适配与格式转换 |

同阶内按高级、中级、初级表示重要性由高到低。等级只表示相对工作流位置：某项黄阶工具仍可能是某个具体任务的必要条件；高阶条目也不因此成为质量更好或已经可用的产品。

浏览表列品级、名称、重要性范围和分级依据；当前明细及每项完整登记以[登记源](data.json)为准。登记中的 10 项来源限定实现、13 条本地路径记录、12 项依赖图具名对象/运行观察和 8 项用户确认的依赖类别属于不同计数视角；依赖图另有 9 条本地关联，只表达关系、不重复计作对象；本地范围排除另有 9 条。158 条外部资源行也不等同于 158 件法器。

<a id="doc-faqi-system-重要性与效能评级"></a>
**重要性与效能评级**

| 维度 | 回答的问题 | 当前状态 |
|---|---|---|
| 重要性分级 | 该工具或类别在 Vibe Coding 工作流中有多关键、可由什么替代？ | 已按用户要求形成暂定排序，见法器总表。 |
| 正式效能评级 | 某一固定实现、版本和任务环境是否达到明确效果合同？ | 量表仍为 draft；任务合同、基线和阈值未校准，当前没有正式效能结论。 |

来源审查、版本观察、静态阅读或单次烟测都不能替代固定任务合同和可复核的效果证据。登记状态也不等于独立审查、运行验证、许可证批准或安全授权。正式效能规约及证据条件见[统一本体中的法器品级规约](../gongfa/README.md#doc-cultivation-ontology-taxonomy-法器品级规约)。

<a id="doc-faqi-system-选用流程"></a>
**选用流程**

1. 先定义要完成的任务、验收条件、环境和权限边界，不从最高品级反推工具选择。
2. 从总表识别可能的工具或依赖类别，再核实具体实现、来源、版本和可用性；抽象类别不能直接当成已安装产品。
3. 检查数据、网络、外部副作用、许可和恢复方式。类别纳入或版本观察不构成批准。
4. 在适用任务中运行有界验证，保留成功与失败证据；验证范围不得超过实际测试的输入和环境。
5. 若要提出正式效能评级，另按固定任务合同、合理基线、校准阈值和可复核结果评定，不沿用本页的重要性分组。

<a id="doc-faqi-system-skill-seekers-mcp-static-review"></a>

<a id="doc-faqi-system-固定源码复核skill-seekers-mcp"></a>
**固定源码复核：Skill Seekers MCP**

2026-10-16对固定 pin `26638b248279a3b001b651475e0f28975f5ff069` 新增 S66–S73 支持选区，
完整路径、一基半开行号、文件及选区 SHA 见[登记源](data.json)。这些仍支持同一件程序，不新增运行实例或品级。

- **入口与版本**：兼容入口转交 FastMCP；是否实际加载取决于依赖和运行环境。头注释写34个工具，静态可见40个装饰函数，
  health 返回版本字符串2.1.1；它们不等于运行工具清单，也不能替代 pyproject 的3.5.1源码声明或实际版本核验。
- **监听与授权**：默认 stdio，HTTP 默认 `127.0.0.1:8000`；选区启用通配 CORS。
  回环地址只限制默认监听范围，CORS 不是身份认证或调用授权，不能据此断言服务已安全隔离。
- **打包与凭据**：package 默认允许在存在平台密钥时上传；upload 的显式密钥会进入 `--api-key` 子进程参数，
  Popen 没有显式收窄继承环境。这是源码风险线索，不是已观察到密钥泄露；本轮没有读取实际凭据。
- **副作用与预览**：install 还编排抓取、AI增强、打包、条件上传及独立 marketplace 发布。
  `auto_upload=False` 不关闭前序步骤或发布支路；scrape_docs 在 unlimited 模式先写临时配置，不能把 dry_run 声明理解为零 I/O。
  部分输出使用成功字符串或路径回退，不等于阶段完成、产物存在及外部效果均被独立核实。
- **结论边界**：本轮未导入或执行被审程序、启服务、抓取、上传或安装。
  数据来源授权、认证、下游调用、环境隔离、超时/取消、异常清理和恢复仍待独立验证；不提升运行、效果、独立审查或许可批准状态。

<a id="doc-faqi-system-登记与维护"></a>
**登记与维护**

- [法器登记源](data.json)是唯一可编辑总登记；字段边界见[Schema](data.json)。
- [法器浏览表](#法器总表)由登记源生成，仅列品级、名称和解释；解释展示重要性范围与分级依据，完整字段以[法器登记源](data.json)及各来源所有者的数据为准，不手工编辑。
- 外部资源的原始名称、地址、状态和风险仍由[外部资源登记](../external-resources/README.md)维护。
- 正文类型及正式效能规约以[修仙领域统一本体](../gongfa/README.md#doc-cultivation-ontology-taxonomy)为准；本页不另建分类树或实现身份库。

更新登记或生成视图时使用：

```bash
make sync-faqi-catalog
make check-faqi-catalog
make test-faqi-catalog
```
