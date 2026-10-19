<!-- generated: sync-faqi-catalog.py -->
# Vibe Coding法器重要性总表：地阶

本页包含12项地阶对象。分级仅表示重要性暂定，不代表效能验证。
- [返回总索引](README.md)；其他阶：[天阶](tian.md)、[玄阶](xuan.md)、[黄阶](huang.md)

## 地阶对象

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
