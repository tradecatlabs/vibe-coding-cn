<!-- generated: sync-faqi-catalog.py -->
# Vibe Coding法器总分类与重要性分级表

本视图由[法器总分类登记](../metadata/faqi.json)与外部资源原表生成；仅修改登记数据，不手改此文件。
类型复用[唯一本体](../docs/gongfa/cultivation-ontology-taxonomy.md#唯一分类树)。对象身份、依赖角色与重要性分级分开；品级表示Vibe Coding重要性，不表示实现质量或任务效能。

## 总体概览

登记版本：2；更新：2026-10-11T06:19:20+00:00；依赖图观测：2026-10-10T12:14:00Z。
本地来源实现 10 条，依赖图具名对象/实例 13 条，仓内实现关联到图节点 9 条，用户确认纳入的依赖类别 8 条，重要性分级记录 31 条，外部资源逐行分流 158 条。
外部资源行是来源候选或入口，不等同独立法器对象；依赖图深度、节点数量、版本新旧均不推出重要性。

## 重要性分级口径

按用户指令，以Vibe Coding核心闭环重要性、对模型/Agent/工具执行/代码验证的作用及可替代性分层。天阶为定义性AI模型与Agent协作核心；地阶为代码变更、命令执行与运行基础；玄阶为上下文、质量、复用和产品交付增强；黄阶为可替代的专用或便利性支路。各阶高级、中级、初级表示该阶内重要性由高到低。
当前分布：天阶5条（高级2、中级3）；地阶12条（高级3、中级5、初级4）；玄阶9条（高级2、中级4、初级3）；黄阶5条（高级3、中级1、初级1）。这是用户指定的重要性分类，不代表功能质量、实际效果、具体身份已核或正式效能评级；正式效能规约仍为draft且阈值未校准。

## 按天地玄黄品级主键汇总

依赖角色和重要性决定暂定分组；任务烟测、版本观测及来源审查仅作独立事实，不直接决定品级。

### 天阶

| 品级ID                 | 对象ID                         | 对象                                  | 本体类型          | 赋级状态           | 评定范围                                       | 依据与限制                                                                                                      |
|:-----------------------|:-------------------------------|:--------------------------------------|:------------------|:-------------------|:-----------------------------------------------|:----------------------------------------------------------------------------------------------------------------|
| faqi-tian-advanced     | dep-category-cloud-model-api   | 2.2 云端模型服务/API与固定模型版本    | 依赖类别          | 用户指定重要性暂定 | Vibe Coding重要性：核心模型推理与代码生成      | 提供理解需求、推理和生成代码的核心智能能力；没有模型推理路径即失去Vibe Coding的定义性特征，供应商与模型可替换。 |
| faqi-tian-advanced     | dep-pi-cli                     | Pi Agent CLI（当前 PATH 实例）        | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：当前核心Agent运行与工具编排 | 直接承接需求、上下文、模型调用和工具执行循环；当前环境的核心交互入口，缺失会改变Vibe Coding核心形态。           |
| faqi-tian-intermediate | dep-category-local-model-stack | 2.2 本地模型权重、Tokenizer与推理引擎 | 依赖类别          | 用户指定重要性暂定 | Vibe Coding重要性：本地/离线模型推理路径       | 可提供核心模型推理并支持本地化、隐私或离线需求；在通用工作流中可由云端推理替代，故低于定义性核心路径。          |
| faqi-tian-intermediate | dep-claude-code                | Claude Code（依赖图替代项）           | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：替代Agent运行时             | 若选用可承担AI代码协作与工具编排核心；当前仅具名候选且可与其他运行时替换，低于已用核心路径。                    |
| faqi-tian-intermediate | dep-codex-cli                  | Codex CLI（依赖图替代项）             | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：替代Agent运行时             | 若选用可承担AI代码协作与工具编排核心；当前仅具名候选且可与其他运行时替换，低于已用核心路径。                    |


### 地阶

| 品级ID               | 对象ID                       | 对象                                        | 本体类型          | 赋级状态           | 评定范围                                       | 依据与限制                                                                                                   |
|:---------------------|:-----------------------------|:--------------------------------------------|:------------------|:-------------------|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------|
| faqi-di-advanced     | dep-bash                     | GNU Bash                                    | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：Agent命令执行与脚本交互     | 直接承接终端命令、开发脚本和验证操作，是当前Agent落地代码动作的高重要性接口；Shell实现可替代但该角色不可缺。 |
| faqi-di-advanced     | dep-category-terminal-pty    | 3.2 Terminal Emulator / PTY                 | 依赖类别          | 用户指定重要性暂定 | Vibe Coding重要性：Agent调用工具与执行开发命令 | 把Agent计划转成真实文件、构建和测试操作的关键执行边界；没有等价工具执行通道，代码闭环无法完成。              |
| faqi-di-advanced     | dep-git-client               | Git 本地客户端                              | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：代码变更追踪、比较与恢复    | 支撑审查AI改动、保留版本历史和安全回退，是可维护代码生成闭环的高重要性基础；版本控制实现可替代。             |
| faqi-di-intermediate | dep-category-infrastructure  | 8 CPU/GPU、内存、存储、网络、电力与数据中心 | 依赖类别          | 用户指定重要性暂定 | Vibe Coding重要性：计算、存储与网络承载        | 为模型调用、代码执行及数据交换提供资源底座；实现可跨云、主机和本地环境替换，故不是单一核心产品。             |
| faqi-di-intermediate | dep-category-package-sources | 4.2 包注册表、Git源与可信缓存               | 依赖类别          | 用户指定重要性暂定 | Vibe Coding重要性：依赖获取、锁定与复现        | 支持安装成熟组件、解析代码依赖和重建开发环境；具体注册表与来源有替代，不直接承担AI生成。                     |
| faqi-di-intermediate | dep-nodejs-runtime           | Node.js 运行时                              | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：前端及工具链代码运行        | 支撑前端、Node项目和本仓Markdown工具链；具体语言环境可替代，重要性低于通用Agent与终端执行核心。              |
| faqi-di-intermediate | dep-npm-npx                  | npm / npx 工具                              | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：Node依赖解析与工具调用      | 让Node生态依赖和命令行工具可安装、解析与调用；作用范围依赖项目技术栈，可由其他生态包管理器替代。             |
| faqi-di-intermediate | dep-python-runtime           | Python 运行时                               | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：脚本、工具与项目代码运行    | 支撑本仓工具及大量Python项目的执行和验证；语言运行时可按项目替代，重要但非所有Vibe Coding任务必需。          |
| faqi-di-initial      | dep-gnu-make                 | GNU Make                                    | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：可重复构建与检查入口        | 把构建和验证命令组织成可重复入口有助于交付，但Make可由其他任务运行器或脚本替代。                             |
| faqi-di-initial      | dep-ubuntu-userland          | Ubuntu 用户空间发行版                       | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：当前Linux用户空间           | 承载当前工具链和本地命令，但同类操作系统环境可以替代，重要性来自运行基座而非该发行版身份。                   |
| faqi-di-initial      | dep-wsl2-kernel              | WSL2 Linux 内核                             | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：当前运行环境内核            | 提供当前WSL用户空间的执行底座，但存在其他内核和宿主替代，不属于AI编程核心能力。                              |
| faqi-di-initial      | dep-wsl2-platform            | WSL 2 承载平台                              | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：当前宿主环境实现            | 为当前工具链提供运行宿主，但Linux、macOS或原生Windows等环境可替代，不是Vibe Coding定义性能力。               |


### 玄阶

| 品级ID                 | 对象ID                        | 对象                                                      | 本体类型          | 赋级状态           | 评定范围                                      | 依据与限制                                                                                               |
|:-----------------------|:------------------------------|:----------------------------------------------------------|:------------------|:-------------------|:----------------------------------------------|:---------------------------------------------------------------------------------------------------------|
| faqi-xuan-advanced     | dep-category-ci-platform      | 7.1 Git托管、CI Runner与CI/CD平台                         | 依赖类别          | 用户指定重要性暂定 | Vibe Coding重要性：自动化验证、协作与持续交付 | 把代码生成接入可重复测试、审查和协作交付，显著扩展可靠使用范围；本地闭环可运行但难以替代团队级持续验证。 |
| faqi-xuan-advanced     | dep-category-retrieval-memory | 2.3 检索/索引/记忆与向量库                                | 依赖类别          | 用户指定重要性暂定 | Vibe Coding重要性：长程上下文、知识检索与记忆 | 支撑跨文件和长任务上下文保持、历史知识复用，提升复杂任务可处理范围；短任务仍可不依赖，且实现可替换。     |
| faqi-xuan-intermediate | dep-category-deployment-data  | 7.2-7.3 制品注册表、部署目标、产品运行时、数据库与外部API | 依赖类别          | 用户指定重要性暂定 | Vibe Coding重要性：从代码到产品运行与外部集成 | 支撑部署、数据库和API集成，使代码进入真实产品场景；并非每次编码必需，故属于重要交付扩展而非核心生成。    |
| faqi-xuan-intermediate | faqi-auto-skill-create        | auto-skill模板生成脚本                                    | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：技能资产扩展与复用         | 把操作知识封装为可复用Agent技能，能扩展后续任务能力；属于增益支路，不是最小编码闭环的必需组件。          |
| faqi-xuan-intermediate | faqi-auto-skill-validate      | auto-skill结构校验脚本                                    | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：技能资产质量与可载入性     | 降低扩展技能结构错误造成的接入阻断；不判断语义正确性，属于能力扩展的质量辅助。                           |
| faqi-xuan-intermediate | faqi-skill-seekers            | Skill Seekers程序                                         | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：外部知识转可复用技能       | 增加Agent可复用的领域能力和上下文资产；需特定工作流，不能替代通用推理与工具执行。                        |
| faqi-xuan-initial      | faqi-claude-skill-init        | 官方Skill初始化脚本                                       | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：特定Skill模板初始化        | 降低Claude Skill结构初始化成本，作用范围绑定特定生态，可手工完成且不影响其他Agent的基础闭环。            |
| faqi-xuan-initial      | faqi-codex-config-installer   | Codex配置安装与恢复脚本                                   | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：特定Agent接入配置          | 降低特定Agent初始配置成本，但只服务候选运行时且可手工替代；不属于核心模型推理或执行闭环。                |
| faqi-xuan-initial      | faqi-skill-seekers-adapter    | Skill Seekers本地运行适配脚本                             | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：Skill Seekers本地适配入口  | 便于调用特定知识转技能工具；范围受上游工具限制，可直接调用或人工替代。                                   |


### 黄阶

| 品级ID                  | 对象ID                | 对象                     | 本体类型          | 赋级状态           | 评定范围                                        | 依据与限制                                                                                                      |
|:------------------------|:----------------------|:-------------------------|:------------------|:-------------------|:------------------------------------------------|:----------------------------------------------------------------------------------------------------------------|
| faqi-huang-advanced     | dep-tmux-runtime      | tmux 当前运行实例        | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：长任务与多会话终端复用       | 可持久化和并行组织终端工作，复杂协作时有价值；普通单会话开发可替代，不属于核心生成链。                          |
| faqi-huang-advanced     | faqi-auto-tmux        | auto-tmux命令封装程序    | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：多会话终端协作自动化         | 能管理多会话和worker工作流，复杂并行时有用；基础单Agent编码不依赖，且当前doctor烟测失败，重要性不等于实现质量。 |
| faqi-huang-advanced     | faqi-tmux             | tmux终端复用程序         | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：可选的多会话终端复用         | 支持持久终端与多窗口工作流，复杂长任务可受益；普通编码闭环有替代方案，不属定义性核心。                          |
| faqi-huang-intermediate | faqi-oh-my-tmux       | oh-my-tmux可执行配置程序 | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：终端复用器体验配置           | 改善tmux使用便利性，但不提供模型推理或核心代码执行能力，可由其他终端配置替代。                                  |
| faqi-huang-initial      | faqi-prompt-converter | 提示词格式转换程序       | software-artifact | 用户指定重要性暂定 | Vibe Coding重要性：提示词资产格式迁移的辅助支路 | 只负责格式转换，能维护和复用提示词资产但不参与模型推理或代码执行；替代方式多，属低重要性辅助。                  |


## Vibe Coding依赖图中的现实对象

依赖图来源：[技术栈第十六节](../docs/gongfa/technology-stack.md#reference-technology-stack-%E5%8D%81%E5%85%AD%E6%8A%80%E6%9C%AF%E6%A0%88%E7%9A%84%E5%B1%82%E7%BA%A7%E7%BB%93%E6%9E%84)；SHA-256 `88ff3494095c2a794acf130d5d2ccc4eb4b67ccdc8c174e7ef09f35c11a450a2`。运行时版本观测只绑定本次命令与PATH实例，不证明依赖源码或会话服务端版本。

| 对象ID              | 对象                           | 依赖图位置                             | 本体类型          | 身份状态   | 版本                             | 品级                           |
|:--------------------|:-------------------------------|:---------------------------------------|:------------------|:-----------|:---------------------------------|:-------------------------------|
| dep-pi-cli          | Pi Agent CLI（当前 PATH 实例） | 2.1 Agent运行时 / Pi Agent             | software-artifact | 运行观测   | 1.1.0                            | 天阶高级（用户指定重要性暂定） |
| dep-codex-cli       | Codex CLI（依赖图替代项）      | 2.1 Agent运行时 / Codex替代项          | software-artifact | 具名候选   | 版本待核                         | 天阶中级（用户指定重要性暂定） |
| dep-claude-code     | Claude Code（依赖图替代项）    | 2.1 Agent运行时 / Claude Code替代项    | software-artifact | 具名候选   | 版本待核                         | 天阶中级（用户指定重要性暂定） |
| dep-wsl2-platform   | WSL 2 承载平台                 | 6.1 Windows主机 / WSL                  | software-artifact | 运行观测   | 版本待核                         | 地阶初级（用户指定重要性暂定） |
| dep-ubuntu-userland | Ubuntu 用户空间发行版          | 6.1 Linux发行版 / Ubuntu               | software-artifact | 运行观测   | 24.04.3 LTS                      | 地阶初级（用户指定重要性暂定） |
| dep-wsl2-kernel     | WSL2 Linux 内核                | 6.1 WSL / 版本对应的Linux内核          | software-artifact | 运行观测   | 6.6.87.2-microsoft-standard-WSL2 | 地阶初级（用户指定重要性暂定） |
| dep-bash            | GNU Bash                       | 6.2 Shell与命令解释器                  | software-artifact | 运行观测   | 5.2.21                           | 地阶高级（用户指定重要性暂定） |
| dep-python-runtime  | Python 运行时                  | 4.3 语言与运行时                       | software-artifact | 运行观测   | 3.12.3                           | 地阶中级（用户指定重要性暂定） |
| dep-nodejs-runtime  | Node.js 运行时                 | 4.3 语言与运行时                       | software-artifact | 运行观测   | 22.23.2                          | 地阶中级（用户指定重要性暂定） |
| dep-npm-npx         | npm / npx 工具                 | 4.2 包管理器与依赖解析器               | software-artifact | 运行观测   | 10.9.8                           | 地阶中级（用户指定重要性暂定） |
| dep-git-client      | Git 本地客户端                 | 3.2 文件与代码 / Git本地客户端与工作树 | software-artifact | 运行观测   | 2.43.0                           | 地阶高级（用户指定重要性暂定） |
| dep-gnu-make        | GNU Make                       | 4.3 构建系统                           | software-artifact | 运行观测   | 4.3                              | 地阶初级（用户指定重要性暂定） |
| dep-tmux-runtime    | tmux 当前运行实例              | 3.2 命令/终端 / tmux复用支路           | software-artifact | 运行观测   | 3.4                              | 黄阶高级（用户指定重要性暂定） |

- `dep-pi-cli`：pi --version 输出 1.1.0；type -a 显示多个同名入口，本记录只绑定当前 shell 选中的入口；先前环境记录为 1.0.4，宿主/路径差异待核，不将此版本绑定到会话服务端。；品级分组：天阶高级（用户指定重要性暂定）；正式效能仍未验证。分级量表仍为 draft，初/中/高结果带阈值未校准；本条未建立任务族效果合同。
- `dep-codex-cli`：依赖图及外部资源行指向 Codex CLI 候选；当前安装身份、可执行入口、版本与来源未核。；外部资源：tools-platforms-codex-cli-362bc20a；品级分组：天阶中级（用户指定重要性暂定）；正式效能仍未验证。精确实现/版本、任务合同及分级量表阈值待核。
- `dep-claude-code`：依赖图及外部资源行指向 Claude Code 候选；当前安装身份、可执行入口、版本与来源未核。；外部资源：tools-platforms-claude-code-11b1e88d；品级分组：天阶中级（用户指定重要性暂定）；正式效能仍未验证。精确实现/版本、任务合同及分级量表阈值待核。
- `dep-wsl2-platform`：uname -r 含 microsoft-standard-WSL2，确认当前 Linux 内核运行在 WSL2 兼容环境；Windows宿主版本及 WSL 产品版本未核。；品级分组：地阶初级（用户指定重要性暂定）；正式效能仍未验证。承载平台精确版本、任务合同及分级量表阈值待核。
- `dep-ubuntu-userland`：/etc/os-release 报告 Ubuntu 24.04.3 LTS（VERSION_ID=24.04）。；品级分组：地阶初级（用户指定重要性暂定）；正式效能仍未验证。版本观测不等于具体任务效果；分级量表阈值未校准。
- `dep-wsl2-kernel`：uname -r 输出 6.6.87.2-microsoft-standard-WSL2；不据内核版本推断 Windows/WSL 产品版本。；品级分组：地阶初级（用户指定重要性暂定）；正式效能仍未验证。版本观测不等于具体任务效果；分级量表阈值未校准。
- `dep-bash`：bash --version 输出 GNU bash 5.2.21。；品级分组：地阶高级（用户指定重要性暂定）；正式效能仍未验证。版本观测不等于具体任务效果；分级量表阈值未校准。
- `dep-python-runtime`：python3 --version 输出 Python 3.12.3。；品级分组：地阶中级（用户指定重要性暂定）；正式效能仍未验证。版本观测不等于具体任务效果；分级量表阈值未校准。
- `dep-nodejs-runtime`：node --version 输出 v22.23.2。；品级分组：地阶中级（用户指定重要性暂定）；正式效能仍未验证。版本观测不等于具体任务效果；分级量表阈值未校准。
- `dep-npm-npx`：npm --version 与 npx --version 均输出 10.9.8；登记为同一当前工具链版本观测，不把命令入口重复计数为两件法器。；品级分组：地阶中级（用户指定重要性暂定）；正式效能仍未验证。版本观测不等于具体任务效果；分级量表阈值未校准。
- `dep-git-client`：git --version 输出 git version 2.43.0。；品级分组：地阶高级（用户指定重要性暂定）；正式效能仍未验证。版本观测不等于具体任务效果；分级量表阈值未校准。
- `dep-gnu-make`：make --version 输出 GNU Make 4.3。；品级分组：地阶初级（用户指定重要性暂定）；正式效能仍未验证。版本观测不等于具体任务效果；分级量表阈值未校准。
- `dep-tmux-runtime`：tmux -V 输出 tmux 3.4；本次隔离 session smoke 不能证明二进制来自已登记 faqi-tmux 的固定源码修订。；相似本地来源参照：faqi-tmux（身份关联未证明）；品级分组：黄阶高级（用户指定重要性暂定）；正式效能仍未验证。运行实例与固定源码身份尚未桥接；任务族结果带与分级量表阈值未校准。

### 用户确认纳入的依赖类别

用户于 2026-10-10T14:28:10Z 确认此前列出的依赖类别均已核查并要求全部纳入。具体实现身份和版本仍按登记所据分别记录；品级按Vibe Coding重要性暂定，不等于效能验证。
目标/验收合同、人类授权与取舍、Agent循环、构建/验证/交付过程及反馈仍按角色、内容、过程或关系分类，不因列入依赖范围自动成为软件法器。

| 依赖图类别                                                | 纳入状态     | 分类边界                                                                                                                                         | 品级分组                       |
|:----------------------------------------------------------|:-------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------|
| 2.2 云端模型服务/API与固定模型版本                        | 用户确认纳入 | 用户确认此依赖类别已核并要求纳入；服务/API与模型制品仍分开登记；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。                          | 天阶高级（用户指定重要性暂定） |
| 2.2 本地模型权重、Tokenizer与推理引擎                     | 用户确认纳入 | 用户确认此依赖类别已核并要求纳入；模型制品、Tokenizer与推理程序分别判断；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。                 | 天阶中级（用户指定重要性暂定） |
| 3.2 Terminal Emulator / PTY                               | 用户确认纳入 | 用户确认此依赖类别已核并要求纳入；终端模拟器与PTY系统接口分开分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。                       | 地阶高级（用户指定重要性暂定） |
| 4.2 包注册表、Git源与可信缓存                             | 用户确认纳入 | 用户确认此依赖类别已核并要求纳入；注册表、Git来源与缓存分开分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。                         | 地阶中级（用户指定重要性暂定） |
| 7.1 Git托管、CI Runner与CI/CD平台                         | 用户确认纳入 | 用户确认此依赖类别已核并要求纳入；托管服务、Runner执行环境与CI/CD平台分开分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。           | 玄阶高级（用户指定重要性暂定） |
| 7.2-7.3 制品注册表、部署目标、产品运行时、数据库与外部API | 用户确认纳入 | 用户确认此可选依赖类别已核并要求纳入；注册表、部署环境、运行时、数据库与外部API分别分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。 | 玄阶中级（用户指定重要性暂定） |
| 8 CPU/GPU、内存、存储、网络、电力与数据中心               | 用户确认纳入 | 用户确认此资源类别已核并要求纳入；物理设备、基础设施与供给服务按所指分别分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。            | 地阶中级（用户指定重要性暂定） |
| 2.3 检索/索引/记忆与向量库                                | 用户确认纳入 | 用户确认此可选依赖类别已核并要求纳入；检索过程、索引、记忆内容与向量存储分别分类；本次品级按Vibe Coding重要性分组，正式效能评级另行判断。        | 玄阶高级（用户指定重要性暂定） |


### 依赖图对应的仓内来源实现

这些行指向已固定来源的本地程序内容；与上方实际运行实例分开，关联不意味着运行版相同。

| 本地对象ID                  | 名称                          | 依赖图位置                                  | 关系边界                                                     | 品级分组                       |
|:----------------------------|:------------------------------|:--------------------------------------------|:-------------------------------------------------------------|:-------------------------------|
| faqi-codex-config-installer | Codex配置安装与恢复脚本       | 2.1 Agent运行时 / Codex替代项               | 本地配置辅助脚本；不是Codex CLI实现。                        | 玄阶初级（用户指定重要性暂定） |
| faqi-auto-skill-create      | auto-skill模板生成脚本        | 2.3 Harness与上下文 / 可选Skill制作支路     | 实现仓内Skill骨架生成入口。                                  | 玄阶中级（用户指定重要性暂定） |
| faqi-auto-skill-validate    | auto-skill结构校验脚本        | 2.3 Harness与上下文 / 可选Skill制作支路     | 实现仓内Skill结构检查入口。                                  | 玄阶中级（用户指定重要性暂定） |
| faqi-skill-seekers-adapter  | Skill Seekers本地运行适配脚本 | 2.3 Harness与上下文 / Skill Seekers适配入口 | 适配到固定submodule源码；本机依赖状态另核。                  | 玄阶初级（用户指定重要性暂定） |
| faqi-skill-seekers          | Skill Seekers程序             | 2.3 Harness与上下文 / Skill Seekers上游程序 | 固定submodule中的上游程序实现。                              | 玄阶中级（用户指定重要性暂定） |
| faqi-claude-skill-init      | 官方Skill初始化脚本           | 2.3 Harness与上下文 / 可选Skill制作支路     | 第三方Skill集合中的独立初始化脚本，不等于Claude Code运行时。 | 玄阶初级（用户指定重要性暂定） |
| faqi-auto-tmux              | auto-tmux命令封装程序         | 3.2 命令/终端 / auto-tmux封装               | 依赖PATH中的tmux CLI及Shell。                                | 黄阶高级（用户指定重要性暂定） |
| faqi-oh-my-tmux             | oh-my-tmux可执行配置程序      | 3.2 命令/终端 / oh-my-tmux配置              | 依赖tmux与Shell的可执行配置，不是tmux本体。                  | 黄阶中级（用户指定重要性暂定） |
| faqi-tmux                   | tmux终端复用程序              | 3.2 命令/终端 / tmux CLI、Server、Socket    | 固定源码内容；本地运行实例来源桥接待核。                     | 黄阶高级（用户指定重要性暂定） |


## 本地来源限定法器

以下记录只指选定来源的程序指令内容；不同内容实现是否属于同一产品/派生版本，仍须另有演化证据。未出现在依赖图具体工具节点中的仓内工具仍保留在总表。

| 实现ID                      | 名称                          | 本体类型          | 实现来源ID   | 依赖图位置                                  | 品级分组                       |
|:----------------------------|:------------------------------|:------------------|:-------------|:--------------------------------------------|:-------------------------------|
| faqi-prompt-converter       | 提示词格式转换程序            | software-artifact | S02          | 图中未具名                                  | 黄阶初级（用户指定重要性暂定） |
| faqi-codex-config-installer | Codex配置安装与恢复脚本       | software-artifact | S06          | 2.1 Agent运行时 / Codex替代项               | 玄阶初级（用户指定重要性暂定） |
| faqi-auto-skill-create      | auto-skill模板生成脚本        | software-artifact | S08          | 2.3 Harness与上下文 / 可选Skill制作支路     | 玄阶中级（用户指定重要性暂定） |
| faqi-auto-skill-validate    | auto-skill结构校验脚本        | software-artifact | S09          | 2.3 Harness与上下文 / 可选Skill制作支路     | 玄阶中级（用户指定重要性暂定） |
| faqi-skill-seekers-adapter  | Skill Seekers本地运行适配脚本 | software-artifact | S10          | 2.3 Harness与上下文 / Skill Seekers适配入口 | 玄阶初级（用户指定重要性暂定） |
| faqi-auto-tmux              | auto-tmux命令封装程序         | software-artifact | S12          | 3.2 命令/终端 / auto-tmux封装               | 黄阶高级（用户指定重要性暂定） |
| faqi-skill-seekers          | Skill Seekers程序             | software-artifact | S16          | 2.3 Harness与上下文 / Skill Seekers上游程序 | 玄阶中级（用户指定重要性暂定） |
| faqi-oh-my-tmux             | oh-my-tmux可执行配置程序      | software-artifact | S18          | 3.2 命令/终端 / oh-my-tmux配置              | 黄阶中级（用户指定重要性暂定） |
| faqi-tmux                   | tmux终端复用程序              | software-artifact | S21          | 3.2 命令/终端 / tmux CLI、Server、Socket    | 黄阶高级（用户指定重要性暂定） |
| faqi-claude-skill-init      | 官方Skill初始化脚本           | software-artifact | S23          | 2.3 Harness与上下文 / 可选Skill制作支路     | 玄阶初级（用户指定重要性暂定） |

### faqi-prompt-converter

提示词格式转换程序：指main.py及其转换实现所表达的程序内容；Excel、Markdown和JSONL是输入/输出，不随转换模式复制工具身份。未验证转换正确性。
实现来源 `S02`，佐证来源 `S01`；声明版本：未核/无明确发布版本声明。
暂定品级分组：黄阶初级（用户指定重要性暂定）。

### faqi-codex-config-installer

Codex配置安装与恢复脚本：纳入安装脚本的程序指令；不是Codex CLI实现，不包含账号授权，safe/power配置、全局指令文本另作规约内容。备份/覆盖能力尚未运行验证。
实现来源 `S06`，佐证来源 `S05`；声明版本：未核/无明确发布版本声明。
暂定品级分组：玄阶初级（用户指定重要性暂定）。

### faqi-auto-skill-create

auto-skill模板生成脚本：指渲染Skill模板与建立目录的程序，不是生成出的Skill内容或整个元技能。--force可覆盖目标，未执行。
实现来源 `S08`，佐证来源 `S07`；声明版本：未核/无明确发布版本声明。
暂定品级分组：玄阶中级（用户指定重要性暂定）。

### faqi-auto-skill-validate

auto-skill结构校验脚本：指frontmatter和结构校验程序；成功结构检查不证明Skill语义、执行正确或效果。
实现来源 `S09`，佐证来源 `S07`；声明版本：未核/无明确发布版本声明。
暂定品级分组：玄阶中级（用户指定重要性暂定）。

### faqi-skill-seekers-adapter

Skill Seekers本地运行适配脚本：设置venv/PYTHONPATH并exec上游CLI的本地适配程序。指令内容不同于上游核心，不能把封装当同一副本，也不因同一用途合并其他生成脚本。
实现来源 `S10`，佐证来源 `S07`；声明版本：未核/无明确发布版本声明。
暂定品级分组：玄阶初级（用户指定重要性暂定）。

### faqi-auto-tmux

auto-tmux命令封装程序：指统一操控脚本，不是SKILL.md、tmux二进制、session/pane或某次操作；支持多命令不增加身份。未发送按键、创建会话或读取pane。
实现来源 `S12`，佐证来源 `S11`；声明版本：未核/无明确发布版本声明。
暂定品级分组：黄阶高级（用户指定重要性暂定）。

### faqi-skill-seekers

Skill Seekers程序：指固定submodule修订的软件实现；多个CLI入口及可选MCP模块不机械复制产品身份。3.5.1仅为pyproject源码声明，不是已核发布或运行版。
实现来源 `S16`，佐证来源 `S14, S15`；声明版本：3.5.1（仅源码声明）。
暂定品级分组：玄阶中级（用户指定重要性暂定）。

### faqi-oh-my-tmux

oh-my-tmux可执行配置程序：配置文件含run、cut&#124;sh调用链及可执行shell指令，按实际程序内容归software-artifact，不能仅因.conf后缀归纯规约；不是tmux本身。
实现来源 `S18`，佐证来源 `S17, S19`；声明版本：未核/无明确发布版本声明。
暂定品级分组：黄阶中级（用户指定重要性暂定）。

### faqi-tmux

tmux终端复用程序：指固定源码修订的程序内容，不是物理终端、pane、socket地址或一次会话。Git describe的邻近tag不作为已核发布版本。
实现来源 `S21`，佐证来源 `S20`；声明版本：未核/无明确发布版本声明。
暂定品级分组：黄阶高级（用户指定重要性暂定）。

### faqi-claude-skill-init

官方Skill初始化脚本：只纳入skill-creator下生成目录/模板的独立Python程序，不把官方Skill集合、自然语言方法、模板或其他全部辅助脚本称作同一程序。
实现来源 `S23`，佐证来源 `S22`；声明版本：未核/无明确发布版本声明。
暂定品级分组：玄阶初级（用户指定重要性暂定）。

## 按本次范围排除的本地程序所指

下列源码确有程序实现所指，但应用户要求不作为本清单纳入对象；不代表它们不是软件。保留排除证据，重新纳入须满足各自复核条件。

### Chat Vault同步与查询程序

入口：`tools/chat-vault`；证据选区 `S04`；佐证选区 `S03`。
按用户指定从当前法器清单排除。源码会自动探测Codex/Kiro/Gemini/Claude会话目录，将消息/cwd写入SQLite，并提供搜索、导出、watch和prune；入口在参数解析前会创建虚拟环境并安装依赖。属于私人对话数据、运行安装及持久副作用边界；未读取数据或执行，排除不等于否认其程序实现。

重新纳入前：只有明确需要纳入时，再以合成会话和隔离临时目录验证数据最小化、路径授权、日志/数据库访问控制、导出/删除语义、依赖安装副作用及恢复；不得用真实用户会话做验证。

### Minecraft基岩版角色迁移程序

入口：`tools/external/MCPlayerTransfer`；证据选区 `S34`；佐证选区 `S33`。
按用户指定从当前法器清单排除。源码对.mcworld调用ZIP extractall，读取~local_player LevelDB记录；导入会写入LevelDB并以w模式创建目标归档。未验证不可信归档路径、目标文件覆盖、存档一致性和部分失败恢复；未处理真实存档，排除不等于否认其程序实现。

重新纳入前：如明确需要纳入，先在合成存档副本中验证归档路径/资源上限、无覆盖的临时输出、LevelDB读写一致性、失败清理与可恢复性；禁止用唯一真实存档作为测试输入。

### 小红书图片ZIP转PDF程序

入口：`tools/external/XHS-image-to-PDF-conversion`；证据选区 `S36`；佐证选区 `S35`。
按用户指定从当前法器清单排除。源码把外部ZIP解到输入旁固定temp_extract，运行前会递归删除同名目录；保存PDF后会删除原ZIP，异常时也会清理临时目录。缺少路径安全、覆盖保护、备份和失败恢复证据，未处理真实文件；排除不等于否认其程序实现。

重新纳入前：如明确需要纳入，先在隔离副本验证ZIP成员路径和展开上限、唯一随机临时目录、输入/PDF不覆盖、原ZIP保留、原子输出和所有失败路径恢复；不得使用真实业务ZIP测试。

### EPUB CSS清理网页程序

入口：`tools/external/html-tools-main`；证据选区 `S25`；佐证选区 `S24`。
按用户指定从当前法器清单移除。固定来源选区仅保留为该网页实现的排除证据；未运行，不据此批准身份、依赖可用性、效果或许可。

重新纳入前：如需重新纳入，重新核定固定来源、身份、依赖和许可，并在隔离副本中验证文件读写及失败恢复；不得把源码存在当作运行证明。

### Markdown预览与文本导出网页程序

入口：`tools/external/html-tools-main`；证据选区 `S26`；佐证选区 `S24`。
按用户指定从当前法器清单移除。固定来源选区仅保留为该Markdown预览/导出实现的排除证据；未运行，不据此批准身份、依赖可用性、效果或许可。

重新纳入前：如需重新纳入，重新核定固定来源、身份、版本、依赖和许可，并在隔离输入下复核预览与导出行为；不得将源码声明当作安全或效果验证。

### 任务卡片PNG导出网页程序

入口：`tools/external/html-tools-main`；证据选区 `S27`；佐证选区 `S24`。
按用户指定从当前法器清单移除。固定来源选区仅保留为该卡片导出实现的排除证据；未运行，不据此批准身份、依赖可用性、效果或许可。

重新纳入前：如需重新纳入，重新核定固定来源、身份、依赖和许可，并用合成内容验证导出结果；不使用私人或业务资料。

### 小红书内容卡片PNG导出网页程序

入口：`tools/external/html-tools-main`；证据选区 `S28`；佐证选区 `S24`。
按用户指定从当前法器清单移除。固定来源选区仅保留为该内容卡片导出实现的排除证据；未运行，不据此批准身份、依赖可用性、效果或许可。

重新纳入前：如需重新纳入，重新核定固定来源、身份、依赖和许可，并用合成内容验证导出行为及外部脚本边界；不使用私人或业务资料。

### Markdown同步预览与PNG导出网页程序

入口：`tools/external/html-tools-main`；证据选区 `S29`；佐证选区 `S24`。
按用户指定从当前法器清单移除。固定来源选区仅保留为该Markdown同步预览/导出实现的排除证据；未运行，不据此批准身份、版本、依赖、效果或许可。

重新纳入前：如需重新纳入，重新核定固定来源、与其他页面的产品关系、版本、依赖和许可，并以隔离输入复核同步及导出行为。

### my-nvim的LazyVim引导配置程序

入口：`tools/external/my-nvim`；证据选区 `S32`；佐证选区 `S30, S31`。
按用户指定从当前法器清单移除。Lua配置程序来源仅保留为排除证据；未运行，不据此批准身份、插件依赖、效果或许可。

重新纳入前：如需重新纳入，重新核定固定来源、身份、版本、依赖和许可，并在临时HOME/隔离环境验证克隆及更新副作用；不得使用真实用户Neovim配置验证。

## 13个本地入口的分离结果

### tools/prompts-library

本次纳入对象：`faqi-prompt-converter`。纳入程序，不把提示词资产或生成目录当工具实现。
佐证来源：`S01, S02`。

### tools/chat-vault

本次纳入对象：`无（见范围排除记录）`。代码确有会话同步/查询程序所指，但按本轮用户范围排除，不作为当前法器对象。
佐证来源：`S03, S04`。
- 待核：会话文件自动探测、SQLite持久化、搜索/导出及启动时环境创建/安装涉及私人数据和副作用；未运行，也未读取用户数据。

### tools/config/.codex

本次纳入对象：`faqi-codex-config-installer`。配置与AGENTS文本不等于CLI；脚本本身有独立程序所指。
佐证来源：`S05, S06`。
- 待核：Codex实际程序、已安装版本、权限及账户不由本目录证明。

### skills/auto-skill

本次纳入对象：`faqi-auto-skill-create, faqi-auto-skill-validate, faqi-skill-seekers-adapter`。Skill说明/规约与三个独立入口脚本分离，不把整Skill包登记成一件软件。
佐证来源：`S07, S08, S09, S10`。
- 待核：其他辅助模块未逐模块登记，不能将本次选区称为全包能力审查。

### skills/auto-tmux

本次纳入对象：`faqi-auto-tmux`。Skill方法/规约、执行脚本、被依赖程序及运行入口分别指认。
佐证来源：`S11, S12, S13`。
- 待核：两个assets引用实际上是零字节普通占位文件，不是README声称的软链接；本次记录缺口，不冒称已修复或上游源码可经此引用到达。
- 待核：蜂群附属脚本不逐一登记，不启动蜂群，也不将蜂群状态/日志算软件。

### tools/external/Skill_Seekers-development

本次纳入对象：`faqi-skill-seekers`。源码内容与仓库载体、接口规范、抓取过程、输入资料和生成Skill分开。
佐证来源：`S14, S15, S16`。
- 待核：CLI与MCP各实现的完整对应关系、许可/可用性与外部I/O权限未作完整审查。

### tools/external/.tmux

本次纳入对象：`faqi-oh-my-tmux`。配置数据与嵌入程序按实际所指区分；本条纳入可执行配置程序，未安装或source配置。
佐证来源：`S17, S18, S19`。
- 待核：源码含条件性kill-server；纳入不等于可安全对当前会话执行。

### tools/external/tmux

本次纳入对象：`faqi-tmux`。tmux程序与配置、操控封装、终端会话和显示记录分开。
佐证来源：`S20, S21`。

### tools/external/claude-official-skills

本次纳入对象：`faqi-claude-skill-init`。集合入口不等于法器身份；指令内容与脚本实现分别判断。
佐证来源：`S22, S23`。
- 待核：README明确部分文档Skill仅source-available，不能把整个集合称为同一开源许可证；本次不批准再分发/商用许可。
- 待核：其余辅助脚本未逐模块展开。

### tools/external/html-tools-main

本次纳入对象：`无（见范围排除记录）`。五个不同页面实现均按用户指定从当前法器清单排除；排除不否认其程序实现。
佐证来源：`S24, S25, S26, S27, S28, S29`。
- 待核：如需重新纳入，须逐项复核来源内容、身份、版本、依赖及许可；未进行运行或效果验证。
- 待核：两个Markdown相关实现以及文件名“1.0”的产品同一/版本演化仍待核，不自动合并或填predecessor。

### tools/external/my-nvim

本次纳入对象：`无（见范围排除记录）`。配置程序按用户指定从当前法器清单排除；不代表宿主Neovim、LazyVim依赖或整个仓库内容一并纳入/排除。
佐证来源：`S30, S31, S32`。
- 待核：如需重新纳入，须复核固定来源、身份、版本、依赖及许可；配置可能克隆插件并检查更新，未运行或验证效果。

### tools/external/MCPlayerTransfer

本次纳入对象：`无（见范围排除记录）`。代码确有存档角色提取/导入程序所指，但按本轮用户范围排除，不作为当前法器对象。
佐证来源：`S33, S34`。
- 待核：对压缩包extractall、LevelDB角色写入及目标归档直接写入的路径安全、覆盖、完整性和失败恢复未测试。

### tools/external/XHS-image-to-PDF-conversion

本次纳入对象：`无（见范围排除记录）`。代码确有ZIP图片转PDF程序所指，但按本轮用户范围排除，不作为当前法器对象。
佐证来源：`S35, S36`。
- 待核：源码固定temp_extract并先递归删除同名目录，解压外部ZIP、写PDF且成功后删除原ZIP；未运行或验证恢复。

## 静态依赖与引用入口

`requires`只记录源码/说明声明的依赖；相关本地实现ID是源码参照，不证明运行时加载了该版本，更不证明实际使用、符合协议或已获权限。

| 主体实现                   | 谓词     | 依赖所指                               | 相关来源实现       | 证据ID   |
|:---------------------------|:---------|:---------------------------------------|:-------------------|:---------|
| faqi-auto-tmux             | requires | tmux程序（运行版本未知）               | faqi-tmux          | S13      |
| faqi-oh-my-tmux            | requires | tmux&gt;=2.6及awk/perl/grep/sed        | faqi-tmux          | S17      |
| faqi-skill-seekers-adapter | requires | 链接源码中的skill&#95;seekers.cli.main | faqi-skill-seekers | S10      |

- `faqi-auto-tmux`：脚本调用PATH中的tmux；本地上游源码仅作相关参照，不证明实际安装二进制来自该修订。
- `faqi-oh-my-tmux`：README声明版本下限，不将配置修订误写成tmux版本，也不保证当前环境满足依赖。
- `faqi-skill-seekers-adapter`：源码路径确由软链接指到选定submodule；这是静态加载意图，venv实际依赖、Python解析和运行结果未核。

- `skills/auto-skill/scripts/Skill_Seekers-development`：`symlink`；目标 `../../../tools/external/Skill_Seekers-development`。同一仓库源码的引用入口，不新增法器副本；封装脚本另有指令内容。
- `skills/claude-official-skills`：`symlink`；目标 `../tools/external/claude-official-skills`。指向Skill集合而非一件软件，不能再因引用入口登记整集合。
- `skills/auto-tmux/assets/oh-my-tmux`：`empty-placeholder`；目标 `无`。实际Git模式100644、0字节；README称软链接，但此路径不能提供上游来源到达证据。
- `skills/auto-tmux/assets/tmux-src`：`empty-placeholder`；目标 `无`。实际Git模式100644、0字节；独立tmux源码已按真实submodule审，不把占位文件算副本。

## 158条外部资源逐行分流

名称、原ID、状态、验证状态与风险只读自原YAML。`active`与`imported-unverified`不证明可用、许可或推荐。
未核远端实现/版本的候选不登记为本地法器；模型名称所指与聊天平台分开。资料排除仅针对当前条目所指，不断言整个仓库没有程序。
同名或同网址只产生重复入口核查线索，不自动合并软件身份；网络/金融分流不授权开户、交易、账户读取或实际网络操作。

### 软件实现候选

原行明确描述程序、编辑器、CLI、插件、库或生成工具，保留软件实现候选；只有名称/介绍地址，未核具体实现、版本、许可证或能力，不直接赋型/登记。

| 原资源ID                                            | 名称                  | 原状态       | 原验证状态          | 原风险标记   |
|:----------------------------------------------------|:----------------------|:-------------|:--------------------|:-------------|
| tools-platforms-codex-cli-362bc20a                  | Codex CLI             | active       | imported-unverified | 无           |
| tools-platforms-droid-1b66f6e0                      | Droid                 | active       | imported-unverified | 无           |
| tools-platforms-docusaurus-09c54423                 | Docusaurus            | active       | imported-unverified | 无           |
| tools-platforms-vitepress-da10a919                  | VitePress             | active       | imported-unverified | 无           |
| tools-platforms-lazyvim-2f22a781                    | LazyVim               | active       | imported-unverified | 无           |
| tools-platforms-neovim-a8b85739                     | Neovim                | active       | imported-unverified | 无           |
| tools-platforms-pearai-0683754c                     | PearAI                | active       | imported-unverified | 无           |
| tools-platforms-vs-code-e8f2d385                    | VS Code               | active       | imported-unverified | 无           |
| tools-platforms-void-b1594346                       | Void                  | active       | imported-unverified | 无           |
| tools-platforms-django-e05156b6                     | Django                | active       | imported-unverified | 无           |
| tools-platforms-excalidraw-02ba0cb2                 | Excalidraw            | active       | imported-unverified | 无           |
| tools-platforms-mermaid-cc6f6e7e                    | Mermaid               | active       | imported-unverified | 无           |
| tools-platforms-dbeaver-aa2fc821                    | DBeaver               | active       | imported-unverified | 无           |
| tools-platforms-tableplus-9950f31a                  | TablePlus             | active       | imported-unverified | 无           |
| tools-platforms-warp-14bec77a                       | Warp                  | active       | imported-unverified | 无           |
| tools-platforms-claude-code-11b1e88d                | Claude Code           | active       | imported-unverified | 无           |
| tools-platforms-opencode-ada070db                   | OpenCode              | active       | imported-unverified | 无           |
| tools-platforms-gemini-cli-d077e5cc                 | Gemini CLI            | active       | imported-unverified | 无           |
| tools-platforms-gemini-cli-row40-d077e5cc           | Gemini CLI            | active       | imported-unverified | 无           |
| tools-platforms-qwen-cli-a1b92a34                   | Qwen CLI              | active       | imported-unverified | 无           |
| tools-platforms-bito-0c0619b5                       | Bito                  | active       | imported-unverified | 无           |
| tools-platforms-codeium-668488a9                    | Codeium               | active       | imported-unverified | 无           |
| tools-platforms-continue-edb7b3bf                   | Continue              | active       | imported-unverified | 无           |
| tools-platforms-cursor-8ebf3977                     | Cursor                | active       | imported-unverified | 无           |
| tools-platforms-zed-07b4820e                        | Zed                   | active       | imported-unverified | 无           |
| tools-platforms-chatgpt-exporter-a03efe97           | ChatGPT Exporter      | active       | imported-unverified | 无           |
| repo-rules-scaffolds-autogen-fc00be5e               | autogen               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-browser-use-268f0f95           | browser-use           | active       | imported-unverified | 无           |
| repo-rules-scaffolds-crewai-d9a56566                | crewai                | active       | imported-unverified | 无           |
| repo-rules-scaffolds-dspy-d8bdba82                  | dspy                  | active       | imported-unverified | 无           |
| repo-rules-scaffolds-langchain-089a07ab             | langchain             | active       | imported-unverified | 无           |
| repo-rules-scaffolds-pydantic-ai-cb69369e           | pydantic-ai           | active       | imported-unverified | 无           |
| repo-rules-scaffolds-smolagents-790ade5e            | smolagents            | active       | imported-unverified | 无           |
| repo-rules-scaffolds-aider-adccc23a                 | aider                 | active       | imported-unverified | 无           |
| repo-rules-scaffolds-claude-code-ef1ef8b6           | claude-code           | active       | imported-unverified | 无           |
| repo-rules-scaffolds-cline-644a6623                 | cline                 | active       | imported-unverified | 无           |
| repo-rules-scaffolds-continue-d5516851              | continue              | active       | imported-unverified | 无           |
| repo-rules-scaffolds-gemini-cli-be45a9ce            | gemini-cli            | active       | imported-unverified | 无           |
| repo-rules-scaffolds-gpt-engineer-eaa2e8a8          | gpt-engineer          | active       | imported-unverified | 无           |
| repo-rules-scaffolds-oh-my-opencode-0348827b        | oh-my-opencode        | active       | imported-unverified | 无           |
| repo-rules-scaffolds-open-interpreter-a514262e      | open-interpreter      | active       | imported-unverified | 无           |
| repo-rules-scaffolds-opencode-e1b762af              | opencode              | active       | imported-unverified | 无           |
| repo-rules-scaffolds-spec-kit-a9a40ae2              | spec-kit              | active       | imported-unverified | 无           |
| repo-rules-scaffolds-avante-nvim-29a0c49f           | avante.nvim           | active       | imported-unverified | 无           |
| repo-rules-scaffolds-codecompanion-nvim-a6f68dc2    | codecompanion.nvim    | active       | imported-unverified | 无           |
| repo-rules-scaffolds-codeium-b0b85053               | codeium               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-copilot-vim-c06b7933           | copilot.vim           | active       | imported-unverified | 无           |
| repo-rules-scaffolds-gitingest-ee7a3f76             | gitingest             | active       | imported-unverified | 无           |
| repo-rules-scaffolds-jan-c4cdcb50                   | jan                   | active       | imported-unverified | 无           |
| repo-rules-scaffolds-lmstudio-8b9fe81d              | lmstudio              | active       | imported-unverified | 无           |
| repo-rules-scaffolds-localai-ea1fbd8b               | localai               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-ollama-33222b83                | ollama                | active       | imported-unverified | 无           |
| repo-rules-scaffolds-repomix-5aa70b79               | repomix               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-text-generation-webui-8ec0aebb | text-generation-webui | active       | imported-unverified | 无           |
| repo-rules-scaffolds-anythingllm-a3e8a5fc           | AnythingLLM           | active       | imported-unverified | 无           |
| repo-rules-scaffolds-dify-4f89d10f                  | Dify                  | active       | imported-unverified | 无           |
| repo-rules-scaffolds-privategpt-c615ca94            | PrivateGPT            | active       | imported-unverified | 无           |
| repo-rules-scaffolds-quivr-5cc2ab96                 | Quivr                 | active       | imported-unverified | 无           |
| repo-rules-scaffolds-ragflow-c92a0918               | RAGFlow               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-devdocs-62126dcb               | DevDocs               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-create-next-app-1bebc93a       | create-next-app       | active       | imported-unverified | 无           |
| repo-rules-scaffolds-create-t3-app-daf8fe4b         | create-t3-app         | active       | imported-unverified | 无           |
| repo-rules-scaffolds-shadcn-ui-d7cf613e             | shadcn/ui             | active       | imported-unverified | 无           |
| repo-rules-scaffolds-vite-3e45b462                  | vite                  | active       | imported-unverified | 无           |
| repo-rules-scaffolds-codex-e3c8be51                 | openai/codex          | active       | imported-unverified | 无           |
| repo-rules-scaffolds-roo-code-36e77dcc              | RooCodeInc/Roo-Code   | needs-review | imported-unverified | 无           |
| network-payment-services-flclash-a974428b           | FlClash               | active       | imported-unverified | 无           |

- `tools-platforms-codex-cli-362bc20a`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/0`。描述混有“最强模型”、CLI、配置与旧地址；只保留CLI候选，不使用宣传赋级，本地Codex安装脚本不等于CLI。
- `tools-platforms-droid-1b66f6e0`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/5`。
- `tools-platforms-docusaurus-09c54423`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/13`。
- `tools-platforms-vitepress-da10a919`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/15`。
- `tools-platforms-lazyvim-2f22a781`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/17`。
- `tools-platforms-neovim-a8b85739`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/18`。
- `tools-platforms-pearai-0683754c`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/19`。
- `tools-platforms-vs-code-e8f2d385`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/20`。
- `tools-platforms-void-b1594346`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/21`。
- `tools-platforms-django-e05156b6`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/22`。
- `tools-platforms-excalidraw-02ba0cb2`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/23`。
- `tools-platforms-mermaid-cc6f6e7e`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/24`。
- `tools-platforms-dbeaver-aa2fc821`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/26`。
- `tools-platforms-tableplus-9950f31a`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/27`。
- `tools-platforms-warp-14bec77a`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/28`。
- `tools-platforms-claude-code-11b1e88d`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/30`。
- `tools-platforms-opencode-ada070db`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/32`。官网品牌与另行opencode-ai/opencode仓库不能凭同名自动合并，需核来源与演化。
- `tools-platforms-gemini-cli-d077e5cc`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/31`。与另一Gemini CLI行指同一官网，属于重复介绍线索，不把两个资源ID登记为两程序。
- `tools-platforms-gemini-cli-row40-d077e5cc`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/38`。与前一Gemini CLI行同名同网址，原ID仍保留；还需与GitHub实现核具体版本。
- `tools-platforms-qwen-cli-a1b92a34`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/39`。
- `tools-platforms-bito-0c0619b5`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/41`。
- `tools-platforms-codeium-668488a9`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/42`。
- `tools-platforms-continue-edb7b3bf`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/43`。
- `tools-platforms-cursor-8ebf3977`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/59`。
- `tools-platforms-zed-07b4820e`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/62`。
- `tools-platforms-chatgpt-exporter-a03efe97`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/68`。
- `repo-rules-scaffolds-autogen-fc00be5e`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/5`。
- `repo-rules-scaffolds-browser-use-268f0f95`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/6`。
- `repo-rules-scaffolds-crewai-d9a56566`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/7`。
- `repo-rules-scaffolds-dspy-d8bdba82`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/8`。
- `repo-rules-scaffolds-langchain-089a07ab`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/9`。
- `repo-rules-scaffolds-pydantic-ai-cb69369e`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/10`。
- `repo-rules-scaffolds-smolagents-790ade5e`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/11`。
- `repo-rules-scaffolds-aider-adccc23a`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/12`。
- `repo-rules-scaffolds-claude-code-ef1ef8b6`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/13`。
- `repo-rules-scaffolds-cline-644a6623`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/14`。
- `repo-rules-scaffolds-continue-d5516851`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/15`。
- `repo-rules-scaffolds-gemini-cli-be45a9ce`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/16`。
- `repo-rules-scaffolds-gpt-engineer-eaa2e8a8`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/17`。
- `repo-rules-scaffolds-oh-my-opencode-0348827b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/18`。
- `repo-rules-scaffolds-open-interpreter-a514262e`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/19`。
- `repo-rules-scaffolds-opencode-e1b762af`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/20`。仓库URL为opencode-ai/opencode；不据名称与opencode.ai官网或其他研究来源认定同一实现。
- `repo-rules-scaffolds-spec-kit-a9a40ae2`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/21`。
- `repo-rules-scaffolds-avante-nvim-29a0c49f`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/24`。
- `repo-rules-scaffolds-codecompanion-nvim-a6f68dc2`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/25`。
- `repo-rules-scaffolds-codeium-b0b85053`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/26`。此行指codeium.vim插件，不能与Codeium平台或Windsurf品牌合并。
- `repo-rules-scaffolds-copilot-vim-c06b7933`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/27`。
- `repo-rules-scaffolds-gitingest-ee7a3f76`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/41`。
- `repo-rules-scaffolds-jan-c4cdcb50`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/42`。
- `repo-rules-scaffolds-lmstudio-8b9fe81d`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/43`。
- `repo-rules-scaffolds-localai-ea1fbd8b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/44`。
- `repo-rules-scaffolds-ollama-33222b83`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/45`。
- `repo-rules-scaffolds-repomix-5aa70b79`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/46`。
- `repo-rules-scaffolds-text-generation-webui-8ec0aebb`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/47`。
- `repo-rules-scaffolds-anythingllm-a3e8a5fc`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/55`。
- `repo-rules-scaffolds-dify-4f89d10f`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/56`。
- `repo-rules-scaffolds-privategpt-c615ca94`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/57`。
- `repo-rules-scaffolds-quivr-5cc2ab96`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/58`。
- `repo-rules-scaffolds-ragflow-c92a0918`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/59`。
- `repo-rules-scaffolds-devdocs-62126dcb`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/60`。
- `repo-rules-scaffolds-create-next-app-1bebc93a`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/65`。链接是CLI文档，文档不是程序；条目所指的生成器实现仍需版本核查。
- `repo-rules-scaffolds-create-t3-app-daf8fe4b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/66`。
- `repo-rules-scaffolds-shadcn-ui-d7cf613e`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/68`。
- `repo-rules-scaffolds-vite-3e45b462`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/69`。
- `repo-rules-scaffolds-codex-e3c8be51`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/81`。
- `repo-rules-scaffolds-roo-code-36e77dcc`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/82`。原描述称archive且status=needs-review；仅保留源码候选，不冒称当前可用或已核归档状态。
- `network-payment-services-flclash-a974428b`：[原始资源行](../assets/external-resources/network-payment-services.yml) `/resources/1`。源码候选仅指代理客户端内容，不授权代理连接或实际网络配置。

### 托管入口候选

按原行服务功能与网址保留托管入口候选；网址不是实现、部署或设备证据，平台/模型/账号/实际调用仍需分离，未访问账户或核部署版本。

| 原资源ID                                     | 名称           | 原状态   | 原验证状态          | 原风险标记   |
|:---------------------------------------------|:---------------|:---------|:--------------------|:-------------|
| tools-platforms-apps-script-e6b8bbbb         | Apps Script    | active   | imported-unverified | 无           |
| tools-platforms-google-sheets-32b827b0       | Google Sheets  | active   | imported-unverified | 无           |
| tools-platforms-mintlify-0f0b6833            | Mintlify       | active   | imported-unverified | 无           |
| tools-platforms-mermaid-chart-302f49f0       | Mermaid Chart  | active   | imported-unverified | 无           |
| tools-platforms-zread-6c1ee1d6               | Zread          | active   | imported-unverified | 无           |
| tools-platforms-notebooklm-e1b56ba1          | NotebookLM     | active   | imported-unverified | 无           |
| tools-platforms-kimi-53c18eae                | Kimi           | active   | imported-unverified | 无           |
| tools-platforms-chatglm-cn-ebc410ba          | 智谱清言       | active   | imported-unverified | 无           |
| tools-platforms-www-doubao-com-b4d6c78b      | 豆包           | active   | imported-unverified | 无           |
| tools-platforms-tongyi-aliyun-com-a528848f   | 通义千问       | active   | imported-unverified | 无           |
| tools-platforms-ai-studio-2cd869be           | AI Studio      | active   | imported-unverified | 无           |
| tools-platforms-antigravity-528a772a         | antigravity    | active   | imported-unverified | 无           |
| tools-platforms-chatgpt-935111f5             | ChatGPT        | active   | imported-unverified | 无           |
| tools-platforms-claude-13dd5e3a              | Claude         | active   | imported-unverified | 无           |
| tools-platforms-gemini-dc8a36f7              | Gemini         | active   | imported-unverified | 无           |
| tools-platforms-bolt-new-06379d16            | Bolt.new       | active   | imported-unverified | 无           |
| tools-platforms-devin-f5a69caf               | Devin          | active   | imported-unverified | 无           |
| tools-platforms-lovable-5eb584a1             | Lovable        | active   | imported-unverified | 无           |
| tools-platforms-replit-agent-bbd1c2ac        | Replit Agent   | active   | imported-unverified | 无           |
| tools-platforms-v0-by-vercel-fe818ef0        | v0 by Vercel   | active   | imported-unverified | 无           |
| repo-rules-scaffolds-github-e755441d         | GitHub         | active   | imported-unverified | 无           |
| repo-rules-scaffolds-github-copilot-102fb5f8 | GitHub Copilot | active   | imported-unverified | 无           |

- `tools-platforms-apps-script-e6b8bbbb`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/2`。
- `tools-platforms-google-sheets-32b827b0`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/8`。
- `tools-platforms-mintlify-0f0b6833`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/14`。
- `tools-platforms-mermaid-chart-302f49f0`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/10`。
- `tools-platforms-zread-6c1ee1d6`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/16`。
- `tools-platforms-notebooklm-e1b56ba1`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/25`。
- `tools-platforms-kimi-53c18eae`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/33`。仅保留平台网址候选；Kimi K2.5能力描述与服务实现/实际加载模型未核。
- `tools-platforms-chatglm-cn-ebc410ba`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/34`。平台与GLM-4描述不作为同一对象/版本证据。
- `tools-platforms-www-doubao-com-b4d6c78b`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/35`。模型与聊天客户端品牌并置，当前只保留网页入口候选。
- `tools-platforms-tongyi-aliyun-com-a528848f`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/36`。Qwen模型、聊天服务及免费额度声明分别核，不继承“免费”或能力主张。
- `tools-platforms-ai-studio-2cd869be`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/37`。AI Studio入口、Gemini模型与免费额度不是同一实体。
- `tools-platforms-antigravity-528a772a`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/40`。
- `tools-platforms-chatgpt-935111f5`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/45`。保留对话入口候选，不据GPT-5.1/支持Codex描述批准具体模型或CLI版本。
- `tools-platforms-claude-13dd5e3a`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/46`。保留平台入口候选，不沿用Opus4.6能力/Artifacts宣传为实现效果。
- `tools-platforms-gemini-dc8a36f7`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/47`。模型名、免费额度与长上下文宣传未核，网页入口与模型内容分开。
- `tools-platforms-bolt-new-06379d16`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/63`。
- `tools-platforms-devin-f5a69caf`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/64`。
- `tools-platforms-lovable-5eb584a1`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/65`。
- `tools-platforms-replit-agent-bbd1c2ac`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/66`。
- `tools-platforms-v0-by-vercel-fe818ef0`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/67`。
- `repo-rules-scaffolds-github-e755441d`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/2`。
- `repo-rules-scaffolds-github-copilot-102fb5f8`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/71`。订阅/服务入口与copilot.vim插件、模型或免费资格分别核，原免费描述未核。

### 排除：资料/规约内容

当前条目所指为知识、教程、索引、规则、提示词或模板内容，不作为法器程序登记；不删除原资源，也不断言整个仓库没有程序，其内具体实现须另选来源。

| 原资源ID                                                            | 名称                                   | 原状态       | 原验证状态          | 原风险标记             |
|:--------------------------------------------------------------------|:---------------------------------------|:-------------|:--------------------|:-----------------------|
| tools-platforms-prompt-jsonl-8e9b2066                               | prompt&#95;jsonl                       | needs-review | imported-unverified | non-url-locator        |
| tools-platforms-bilibili-23287176                                   | Bilibili                               | active       | imported-unverified | 无                     |
| tools-platforms-z-library-31b0d982                                  | Z-Library                              | active       | imported-unverified | access-legality-review |
| repo-rules-scaffolds-vibe-coding-e16848e0                           | Vibe Coding 指南                       | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-github-com-e0a40b2e                            | 开发者基础知识库                       | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-mcaf-47f07717                                  | MCAF                                   | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-github-topics-bcc7e192                         | GitHub Topics                          | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-github-trending-d46be94c                       | GitHub Trending                        | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-mcp-servers-d91d6430                   | awesome-mcp-servers                    | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-2025-ai-engineer-reading-list-70f4fbd3         | 2025 AI Engineer Reading List          | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-ai-547bb859                                    | AI 编程最佳实践                        | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-ai-engineering-d04a5b40                        | ai-engineering                         | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-explorables-2cedba5b                   | awesome-explorables                    | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-llm-02e83378                           | awesome-llm                            | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-generative-ai-for-beginners-3b1db321           | generative-ai-for-beginners            | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-llm-course-9227aca8                            | llm-course                             | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-lovable-for-beginners-38de2782                 | lovable-for-beginners                  | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-prompt-engineering-guide-5130a915              | prompt-engineering-guide               | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-vibe-vibe-c80a5961                             | vibe-vibe                              | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-chatgpt-prompts-ebaf3df7               | awesome-chatgpt-prompts                | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-chatgpt-prompts-zh-966cbb5b            | awesome-chatgpt-prompts-zh             | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-claude-code-system-prompts-3f0438e1            | claude-code-system-prompts             | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-system-prompts-and-models-of-ai-tools-8290b642 | system-prompts-and-models-of-ai-tools  | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-cursorrules-7f259f16                   | awesome-cursorrules                    | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-cursor-directory-807839d9                      | cursor.directory                       | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-dotcursorrules-ad20d456                        | dotcursorrules                         | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-langgpt-d6b7fb87                               | LangGPT                                | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-chatgpt-prompts-4c4b8064               | Awesome ChatGPT Prompts                | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-system-prompts-b5948bc8                        | System Prompts 仓库                    | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-easy-vibe-3c217e96                             | datawhalechina/easy-vibe               | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-ai-guide-c12bbbfd                              | liyupi/ai-guide                        | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-vibe-coding-guide-cf65840a                     | wendy7756/vibe-coding-guide            | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-ai-coding-c221421b                             | Daotin/ai-coding                       | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-vibe-coding-skill-a5e7c42d                     | earyantLe/vibe-coding-skill            | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-vibe-coding-e5ab67eb                   | filipecalegario/awesome-vibe-coding    | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-vibe-coding-e3ea2b5b                   | ai-for-developers/awesome-vibe-coding  | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-claude-code-best-practice-01224898             | shanraisshan/claude-code-best-practice | active       | imported-unverified | 无                     |
| repo-rules-scaffolds-awesome-claude-code-5e3406a1                   | hesreallyhim/awesome-claude-code       | active       | imported-unverified | 无                     |

- `tools-platforms-prompt-jsonl-8e9b2066`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/1`。
- `tools-platforms-bilibili-23287176`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/3`。
- `tools-platforms-z-library-31b0d982`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/12`。按本条“电子书资源”所指排除程序登记；保留access-legality-review，不批准访问/下载或许可。
- `repo-rules-scaffolds-vibe-coding-e16848e0`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/0`。
- `repo-rules-scaffolds-github-com-e0a40b2e`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/3`。
- `repo-rules-scaffolds-mcaf-47f07717`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/4`。
- `repo-rules-scaffolds-github-topics-bcc7e192`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/22`。
- `repo-rules-scaffolds-github-trending-d46be94c`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/23`。
- `repo-rules-scaffolds-awesome-mcp-servers-d91d6430`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/28`。
- `repo-rules-scaffolds-2025-ai-engineer-reading-list-70f4fbd3`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/30`。
- `repo-rules-scaffolds-ai-547bb859`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/31`。
- `repo-rules-scaffolds-ai-engineering-d04a5b40`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/32`。
- `repo-rules-scaffolds-awesome-explorables-2cedba5b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/34`。
- `repo-rules-scaffolds-awesome-llm-02e83378`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/35`。
- `repo-rules-scaffolds-generative-ai-for-beginners-3b1db321`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/36`。
- `repo-rules-scaffolds-llm-course-9227aca8`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/37`。
- `repo-rules-scaffolds-lovable-for-beginners-38de2782`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/38`。
- `repo-rules-scaffolds-prompt-engineering-guide-5130a915`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/39`。
- `repo-rules-scaffolds-vibe-vibe-c80a5961`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/40`。
- `repo-rules-scaffolds-awesome-chatgpt-prompts-ebaf3df7`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/48`。与另一f/awesome-chatgpt-prompts行是重复来源线索；保原两ID，不登记两个工具。
- `repo-rules-scaffolds-awesome-chatgpt-prompts-zh-966cbb5b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/49`。
- `repo-rules-scaffolds-claude-code-system-prompts-3f0438e1`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/50`。
- `repo-rules-scaffolds-system-prompts-and-models-of-ai-tools-8290b642`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/51`。
- `repo-rules-scaffolds-awesome-cursorrules-7f259f16`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/52`。
- `repo-rules-scaffolds-cursor-directory-807839d9`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/53`。
- `repo-rules-scaffolds-dotcursorrules-ad20d456`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/54`。
- `repo-rules-scaffolds-langgpt-d6b7fb87`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/61`。
- `repo-rules-scaffolds-awesome-chatgpt-prompts-4c4b8064`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/63`。原description=null；仅依原名称和仓库路径关联提示词合集线索，不补造产品能力。
- `repo-rules-scaffolds-system-prompts-b5948bc8`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/64`。原description=null；与另一同URL条目关联提示词来源线索，不声称模型参数或工具实现。
- `repo-rules-scaffolds-easy-vibe-3c217e96`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/72`。
- `repo-rules-scaffolds-ai-guide-c12bbbfd`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/73`。
- `repo-rules-scaffolds-vibe-coding-guide-cf65840a`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/74`。
- `repo-rules-scaffolds-ai-coding-c221421b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/75`。
- `repo-rules-scaffolds-vibe-coding-skill-a5e7c42d`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/76`。
- `repo-rules-scaffolds-awesome-vibe-coding-e5ab67eb`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/79`。
- `repo-rules-scaffolds-awesome-vibe-coding-e3ea2b5b`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/80`。
- `repo-rules-scaffolds-claude-code-best-practice-01224898`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/83`。
- `repo-rules-scaffolds-awesome-claude-code-5e3406a1`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/84`。

### 排除：模型名称所指

当前名义所指是模型名称/版本，不当作法器程序；未取得参数/结构版本证据，不批准model-artifact实例，所附平台URL不证明模型与服务同一。

| 原资源ID                                 | 名称            | 原状态       | 原验证状态          | 原风险标记   |
|:-----------------------------------------|:----------------|:-------------|:--------------------|:-------------|
| tools-platforms-claude-opus-4-6-f751380c | Claude Opus 4.6 | active       | imported-unverified | 无           |
| tools-platforms-gpt-5-1-codex-1ad522a5   | GPT-5.1 Codex   | needs-review | imported-unverified | missing-link |
| tools-platforms-gemini-2-5-pro-0661c69f  | Gemini 2.5 Pro  | needs-review | imported-unverified | missing-link |
| tools-platforms-dall-e-3-26dc583b        | DALL-E 3        | active       | imported-unverified | 无           |

- `tools-platforms-claude-opus-4-6-f751380c`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/4`。claude.ai平台不是Opus参数内容或具体模型版本的验证证据。
- `tools-platforms-gpt-5-1-codex-1ad522a5`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/6`。
- `tools-platforms-gemini-2-5-pro-0661c69f`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/7`。
- `tools-platforms-dall-e-3-26dc583b`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/48`。名称指模型，但网址是chatgpt.com；图像模型与其调用平台必须分离。

### 待核：对象身份

信息不足、对象名/目标不一致或复合包未展开，保留待核；不凭品牌、后缀、Skill/仓库包装复制软件身份，先明确具体模块、入口及版本。

| 原资源ID                                           | 名称                      | 原状态       | 原验证状态          | 原风险标记   |
|:---------------------------------------------------|:--------------------------|:-------------|:--------------------|:-------------|
| tools-platforms-local-history-2b05b2c1             | Local History             | needs-review | imported-unverified | missing-link |
| tools-platforms-partial-diff-4787875c              | Partial Diff              | needs-review | imported-unverified | missing-link |
| tools-platforms-zsh-d6d24951                       | zsh                       | active       | imported-unverified | 无           |
| tools-platforms-tabnine-0b2c09aa                   | Tabnine                   | active       | imported-unverified | 无           |
| tools-platforms-elevenlabs-5a58d635                | ElevenLabs                | active       | imported-unverified | 无           |
| tools-platforms-ideogram-efb6a3b8                  | Ideogram                  | active       | imported-unverified | 无           |
| tools-platforms-kling-253d44f3                     | Kling                     | active       | imported-unverified | 无           |
| tools-platforms-leonardo-ai-26816634               | Leonardo AI               | active       | imported-unverified | 无           |
| tools-platforms-meshy-549051bc                     | Meshy                     | active       | imported-unverified | 无           |
| tools-platforms-midjourney-976ad67d                | Midjourney                | active       | imported-unverified | 无           |
| tools-platforms-runway-6c8ab136                    | Runway                    | active       | imported-unverified | 无           |
| tools-platforms-sora-3b1d49f7                      | Sora                      | active       | imported-unverified | 无           |
| tools-platforms-suno-fb9344c5                      | Suno                      | active       | imported-unverified | 无           |
| tools-platforms-udio-0d39f909                      | Udio                      | active       | imported-unverified | 无           |
| tools-platforms-kiro-47d2b0fc                      | Kiro                      | active       | imported-unverified | 无           |
| tools-platforms-windsurf-fdd489a7                  | Windsurf                  | active       | imported-unverified | 无           |
| repo-rules-scaffolds-scientific-skills-0f3f6b96    | scientific-skills         | active       | imported-unverified | 无           |
| repo-rules-scaffolds-mcp-servers-5d60dee4          | mcp-servers               | active       | imported-unverified | 无           |
| repo-rules-scaffolds-ai-for-grant-writing-0a634380 | ai-for-grant-writing      | active       | imported-unverified | 无           |
| repo-rules-scaffolds-fastapi-template-c97cc061     | fastapi-template          | active       | imported-unverified | 无           |
| repo-rules-scaffolds-ai-coding-lab-6dc927c2        | luzhenqian/ai-coding-lab  | active       | imported-unverified | 无           |
| repo-rules-scaffolds-cs146s-cn-eaea3651            | ShouZhengAI/CS146S&#95;CN | active       | imported-unverified | 无           |

- `tools-platforms-local-history-2b05b2c1`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/9`。缺链接；同名插件可能有多个实现，需厂商/仓库和版本。
- `tools-platforms-partial-diff-4787875c`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/11`。缺链接；需补具体插件来源，保留missing-link与needs-review。
- `tools-platforms-zsh-d6d24951`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/29`。名称是zsh，但网址指ohmyz.sh；Shell程序与配置框架需消歧，不按标题选择软件身份。
- `tools-platforms-tabnine-0b2c09aa`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/44`。
- `tools-platforms-elevenlabs-5a58d635`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/49`。
- `tools-platforms-ideogram-efb6a3b8`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/50`。
- `tools-platforms-kling-253d44f3`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/51`。
- `tools-platforms-leonardo-ai-26816634`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/52`。
- `tools-platforms-meshy-549051bc`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/53`。
- `tools-platforms-midjourney-976ad67d`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/54`。
- `tools-platforms-runway-6c8ab136`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/55`。
- `tools-platforms-sora-3b1d49f7`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/56`。
- `tools-platforms-suno-fb9344c5`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/57`。
- `tools-platforms-udio-0d39f909`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/58`。
- `tools-platforms-kiro-47d2b0fc`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/60`。
- `tools-platforms-windsurf-fdd489a7`：[原始资源行](../assets/external-resources/tools-platforms.yml) `/resources/61`。
- `repo-rules-scaffolds-scientific-skills-0f3f6b96`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/1`。Skill集合可能包含方法与脚本，需逐实际内容选区；集合自身不直接注册成一件软件。
- `repo-rules-scaffolds-mcp-servers-5d60dee4`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/29`。服务器集合需按独立实现选区，不把MCP协议、多个示例、部署和整仓库作同一实例。
- `repo-rules-scaffolds-ai-for-grant-writing-0a634380`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/33`。
- `repo-rules-scaffolds-fastapi-template-c97cc061`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/67`。模板可能包含可执行应用或生成器，须分清模板内容、应用源码与新生成实例。
- `repo-rules-scaffolds-ai-coding-lab-6dc927c2`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/77`。项目实战复合仓库包含多种项目类型，不能把教程或整个仓库纳为一程序。
- `repo-rules-scaffolds-cs146s-cn-eaea3651`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/78`。课程、作业与工具混合，需明确具体程序选区。

### 关联已审本地来源

原仓库网址与已审本地submodule来源对应，仅建立来源参照，不新增重复法器；不把未版本化仓库入口等同本次固定源码版本。

| 原资源ID                             | 名称          | 原状态   | 原验证状态          | 原风险标记   |
|:-------------------------------------|:--------------|:---------|:--------------------|:-------------|
| repo-rules-scaffolds-skills-cd973130 | Skills 制作器 | active   | imported-unverified | 无           |
| repo-rules-scaffolds-tmux-9f36981a   | tmux          | active   | imported-unverified | 无           |

- `repo-rules-scaffolds-skills-cd973130`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/62`。 对应本地来源参照 faqi-skill-seekers；不把未版本化的仓库URL等同该固定源码版本。
- `repo-rules-scaffolds-tmux-9f36981a`：[原始资源行](../assets/external-resources/repo-rules-scaffolds.yml) `/resources/70`。 对应本地来源参照 faqi-tmux；不把未版本化的仓库URL等同该固定源码版本。

### 待核：受限服务所指

网络/金融服务品牌、推广入口或账号产品所指待核；保留全部风险与原状态，不批准交易、注册、权限、设备或运行实例。

| 原资源ID                                            | 名称         | 原状态   | 原验证状态          | 原风险标记                                          |
|:----------------------------------------------------|:-------------|:---------|:--------------------|:----------------------------------------------------|
| network-payment-services-www-bsmkweb-com-0960fe59   | 币安支付     | active   | imported-unverified | referral-or-tracking-link, financial-service-review |
| network-payment-services-xn-9kqz23b19z-com-a271e5a7 | 网络服务     | active   | imported-unverified | referral-or-tracking-link                           |
| network-payment-services-bybit-81d32c91             | Bybit 虚拟卡 | active   | imported-unverified | referral-or-tracking-link, financial-service-review |

- `network-payment-services-www-bsmkweb-com-0960fe59`：[原始资源行](../assets/external-resources/network-payment-services.yml) `/resources/0`。资源自称“币安支付”，网址为bsmkweb.com并带ref；品牌/网址所指一致性未核，不据名称认定官方服务。
- `network-payment-services-xn-9kqz23b19z-com-a271e5a7`：[原始资源行](../assets/external-resources/network-payment-services.yml) `/resources/2`。注册推广入口只有泛化云服务说明，实际服务、提供方与合规边界待核。
- `network-payment-services-bybit-81d32c91`：[原始资源行](../assets/external-resources/network-payment-services.yml) `/resources/3`。卡产品/账户/支付过程与网站或程序内容分开，不触发开户或支付。

## 来源与选区

选区是一基半开区间 `[start,end)`；SHA-256对应固定Git blob的完整字节与选区原字节，不归一化或复制源码。
校验还核当前文件字节及submodule指针；源码存在和指针匹配不等于完整仓库语义、许可证或能力已审。

### S01

[来源文件](../tools/prompts-library/README.md)：`tools/prompts-library/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`4c2d5f97a6cfa67e033e166676d12eeaab6a562fa83c39b0f2474ae2afbcdae2`。
- 选区：`[1,95)`；SHA-256：`4c2d5f97a6cfa67e033e166676d12eeaab6a562fa83c39b0f2474ae2afbcdae2`。

### S02

[来源文件](../tools/prompts-library/main.py)：`tools/prompts-library/main.py`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`ed0113d3ecbe9c9d4ca48ee7dde2c76c9a6fd1f54a1ae890fd3689d617347691`。
- 选区：`[625,689)`；SHA-256：`757b82c3bba30f1d62359c39f7c110d425463326e854acef2de085f14d90cf6d`。

### S03

[来源文件](../tools/chat-vault/README.md)：`tools/chat-vault/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`938ddcce3ba06fad18a05d072cfc47cb8427064c72745f557e4b782de8a2c753`。
- 选区：`[1,104)`；SHA-256：`deecf873b9392e27cbae073fd6f75fcb1865af9d6461232dd517ba945cafa3d1`。

### S04

[来源文件](../tools/chat-vault/services/chat-vault/src/main.py)：`tools/chat-vault/services/chat-vault/src/main.py`。
- 初审用途：`exclusion_evidence`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`561c611909714d358f9968c45078f037bd46cdb037969d598cfed27d94affd72`。
- 选区：`[65,107)`；SHA-256：`43279c5004b34ef3de79da4dd5c103e741f0a9ed47683e7c262a79bd35f8b551`。

### S05

[来源文件](../tools/config/.codex/README.md)：`tools/config/.codex/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`4cd23bbafa069d8bd651e9997951ac99252cf13310d1c9fda14dcf01de818a53`。
- 选区：`[1,78)`；SHA-256：`b290d2842b0290ee9701e41c046634d2cd90684c0c53d1e97e3781a05d695e87`。

### S06

[来源文件](../tools/config/.codex/install.sh)：`tools/config/.codex/install.sh`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`a2ba28d5a48d46aa7d508408519be117f8726c8d66e632d8736deab9175b04a4`。
- 选区：`[43,100)`；SHA-256：`99ccf88c8d5ec6f7b7eda53fc4fd3af29a0ca08d9eef74ad3283cdf649d6a7cf`。

### S07

[来源文件](../skills/auto-skill/README.md)：`skills/auto-skill/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`2fd869316c0469d9c4079cd9a19c41698b501bca6ddd2b6cc03617e3f96218f0`。
- 选区：`[1,21)`；SHA-256：`2fd869316c0469d9c4079cd9a19c41698b501bca6ddd2b6cc03617e3f96218f0`。

### S08

[来源文件](../skills/auto-skill/scripts/create-skill.sh)：`skills/auto-skill/scripts/create-skill.sh`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`3eb16d2f24cc2af3e7d7a0f4175e06b0258504795d079ba0920be9dd75f2f7fc`。
- 选区：`[80,182)`；SHA-256：`e769660515ada48debbd022fdfb85ec934b4d3413cf3501e06ef075b6d36b1a4`。

### S09

[来源文件](../skills/auto-skill/scripts/validate-skill.sh)：`skills/auto-skill/scripts/validate-skill.sh`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`deb5cf2529a93c87c8b7323b55ffc6d7798e6b59652351ba795340ac8c0061c9`。
- 选区：`[67,160)`；SHA-256：`dbd460af6a32307709a11281c7b90925b9fd9820128eb04881c80c020a99f0dc`。

### S10

[来源文件](../skills/auto-skill/scripts/skill-seekers.sh)：`skills/auto-skill/scripts/skill-seekers.sh`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`fdbf73b1faa1a0f445663b5c7c1c9792bbfb6dcdf5f5308198503e14ea0c64dc`。
- 选区：`[28,66)`；SHA-256：`f678142dddda161372feb5c5af96bbbf5e1b3e76b9e2c7dc905a4d1ba18070f2`。

### S11

[来源文件](../skills/auto-tmux/README.md)：`skills/auto-tmux/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`d21ca4f1c4adb6a799a76f7a7446b1ebca70d2402f73e80600cda1c2a6d24c25`。
- 选区：`[1,18)`；SHA-256：`0c0e46b950949789a6b85addd85f3a9ec0b2945e6a44134f82c7b46acc59b308`。

### S12

[来源文件](../skills/auto-tmux/scripts/auto-tmux.sh)：`skills/auto-tmux/scripts/auto-tmux.sh`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`f473fddada7a7f5fd85afe94deccd16e2aba26195423dc87afbac176315b6567`。
- 选区：`[701,725)`；SHA-256：`701db6430b20faa4bf2477001f584b15a1dea31e6c4a9d32747be343988dd3c2`。

### S13

[来源文件](../skills/auto-tmux/scripts/auto-tmux.sh)：`skills/auto-tmux/scripts/auto-tmux.sh`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`f473fddada7a7f5fd85afe94deccd16e2aba26195423dc87afbac176315b6567`。
- 选区：`[65,95)`；SHA-256：`a745cc41ed28208894954fccadc603a2f11e4e7888bd9df4f85d1dc0c84ca564`。

### S14

[来源文件](../tools/external/Skill_Seekers-development/pyproject.toml)：`tools/external/Skill_Seekers-development/pyproject.toml`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/Skill_Seekers-development`；Git修订：`26638b248279a3b001b651475e0f28975f5ff069`。
- 完整文件SHA-256：`40820d20d8f56c1dc24c8f432141fa438d54473acbfecfa716fc9d188cbc8294`。
- 选区：`[1,15)`；SHA-256：`8fc8e7df82f18edc826b13f63f097661c1f40b19d2e7ab576e25854b453919e3`。

### S15

[来源文件](../tools/external/Skill_Seekers-development/pyproject.toml)：`tools/external/Skill_Seekers-development/pyproject.toml`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/Skill_Seekers-development`；Git修订：`26638b248279a3b001b651475e0f28975f5ff069`。
- 完整文件SHA-256：`40820d20d8f56c1dc24c8f432141fa438d54473acbfecfa716fc9d188cbc8294`。
- 选区：`[301,327)`；SHA-256：`ac6771e334ffad6fe8cb4934797de797375c87d4c33a16afff72de8d1642893f`。

### S16

[来源文件](../tools/external/Skill_Seekers-development/src/skill_seekers/cli/main.py)：`tools/external/Skill_Seekers-development/src/skill_seekers/cli/main.py`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/Skill_Seekers-development`；Git修订：`26638b248279a3b001b651475e0f28975f5ff069`。
- 完整文件SHA-256：`8c02660dacd304f51fe8c4a9685d3f6d5324a7eef7779b6baa7325827bf01985`。
- 选区：`[39,116)`；SHA-256：`60fba27fbe444499a1e95b5dc69edc8b0d34d6c26a30039dcbf9d9205ffdfb14`。

### S17

[来源文件](../tools/external/.tmux/README.md)：`tools/external/.tmux/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/.tmux`；Git修订：`87dcd13a28aeb5f18baee630e24b3f5765ae3a4f`。
- 完整文件SHA-256：`10b0cca6bb2a4ab7af39d76d27f51b91ca1df4dead015315400041695c9471e7`。
- 选区：`[9,78)`；SHA-256：`243d5ab2936723c61f781dd6906e61de92cceea6069e570ca107b6c19236aeb7`。

### S18

[来源文件](../tools/external/.tmux/.tmux.conf)：`tools/external/.tmux/.tmux.conf`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/.tmux`；Git修订：`87dcd13a28aeb5f18baee630e24b3f5765ae3a4f`。
- 完整文件SHA-256：`6807d44735b7b11e64c4488a0c3fdcbd2809cc73efedcc349d098e80a690aeeb`。
- 选区：`[150,190)`；SHA-256：`e39dd4f98da410b88e110772d21d1eb14d3bfb6e2c6e8c36e2cb19129d9c98f8`。

### S19

[来源文件](../tools/external/.tmux/.tmux.conf)：`tools/external/.tmux/.tmux.conf`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/.tmux`；Git修订：`87dcd13a28aeb5f18baee630e24b3f5765ae3a4f`。
- 完整文件SHA-256：`6807d44735b7b11e64c4488a0c3fdcbd2809cc73efedcc349d098e80a690aeeb`。
- 选区：`[1829,1891)`；SHA-256：`3065f39bd62e8cb3bb4095dfaf9784840368d5760137ad01d3f96eb55ede68a1`。

### S20

[来源文件](../tools/external/tmux/README)：`tools/external/tmux/README`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/tmux`；Git修订：`615c27c11789948df2db09e113e882f82dfb3e1c`。
- 完整文件SHA-256：`9fb75e6c7f10c25b73e41b8214336d0dc2acfbe4c99984514ccaf7327192d53e`。
- 选区：`[1,20)`；SHA-256：`68e51dd5a0148fa1d22f5c7565d3da74dc6619207d1c5238658d5fd873c63e5b`。

### S21

[来源文件](../tools/external/tmux/tmux.c)：`tools/external/tmux/tmux.c`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/tmux`；Git修订：`615c27c11789948df2db09e113e882f82dfb3e1c`。
- 完整文件SHA-256：`58a9bef0d1d424fd2e2a79c6d998dab96aab81ee771b7c2653928451f3bf11a8`。
- 选区：`[350,492)`；SHA-256：`cd3c886c9a155f70dcddaeec88b4a86253c565b2e18753327f83446d92a7e8f4`。

### S22

[来源文件](../tools/external/claude-official-skills/README.md)：`tools/external/claude-official-skills/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/claude-official-skills`；Git修订：`1ed29a03dc852d30fa6ef2ca53a67dc2c2c2c563`。
- 完整文件SHA-256：`d7c5c2f9b248c7c0b31f093cf22b9a7407f5b093c8ca9ebe75a5b6845b02b76e`。
- 选区：`[1,28)`；SHA-256：`672c572d34a077a534754b7311d19db68a8402c86fe64e35be5e80da3ae7453a`。

### S23

[来源文件](../tools/external/claude-official-skills/skills/skill-creator/scripts/init_skill.py)：`tools/external/claude-official-skills/skills/skill-creator/scripts/init_skill.py`。
- 初审用途：`implementation`（人工标注，不是自动语义批准）。
- 仓库：`tools/external/claude-official-skills`；Git修订：`1ed29a03dc852d30fa6ef2ca53a67dc2c2c2c563`。
- 完整文件SHA-256：`cf12790f1d4958799281920d599f56aea38fb5c26e2812a61dd740bf3d4b6b99`。
- 选区：`[194,304)`；SHA-256：`f3ef6ff82946a9596d5cacfc1ed0405765187e5ffec5a4ede6c15f5e8dd248dd`。

### S24

[来源文件](../tools/external/html-tools-main/README.md)：`tools/external/html-tools-main/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`6aeb3fbdd0ad484f15b44b8c0e26caa7228cede0a659292893617d19d99b6df3`。
- 选区：`[1,18)`；SHA-256：`c58731ae7c6b900a386e03571782503c366959db1a623c21c7de2a08fc04442d`。

### S25

[来源文件](../tools/external/html-tools-main/clean_epub_css.html)：`tools/external/html-tools-main/clean_epub_css.html`。
- 初审用途：`exclusion_evidence`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`1716a7ea5f4bf4837bc044c9c164e58b3dbb04d492f677b7766b506edd1c0d2a`。
- 选区：`[317,405)`；SHA-256：`4d07dac2850cbf4860f628b5c26d52976aea9cc8dd981851da5141dc7b18a7cb`。

### S26

[来源文件](../tools/external/html-tools-main/markdown-bianjiqi.html)：`tools/external/html-tools-main/markdown-bianjiqi.html`。
- 初审用途：`exclusion_evidence`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`e4c76015749bf42e898412ec7b8e1229c847575ef740bcf6900311d7212dc61e`。
- 选区：`[181,260)`；SHA-256：`cbc5a64c27eefb0801c95a87cbf4ed0a149e25000a41e53e3387eb274ca40894`。

### S27

[来源文件](../tools/external/html-tools-main/task%20card%20generator.html)：`tools/external/html-tools-main/task card generator.html`。
- 初审用途：`exclusion_evidence`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`0eba89d2f674bb0bc26690c4e406f99b7a2bcd40ecd838c1c19e1f970f7b5670`。
- 选区：`[217,284)`；SHA-256：`8b710f5b6f6b1c1f0fcaafead15e6f63e5800684a1c8ae49dad6a7681659eb19`。

### S28

[来源文件](../tools/external/html-tools-main/xhs%20graphic%20production.html)：`tools/external/html-tools-main/xhs graphic production.html`。
- 初审用途：`exclusion_evidence`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`1835e29563d4cf7f01cb9cf837d3f57d1b2e48304cc202e1061240bccf6e7e0e`。
- 选区：`[96,147)`；SHA-256：`52b9c7a45cd3d5c8409ee1cde59c31296b608e35c0d668c2833bd7b35639a0f8`。

### S29

[来源文件](../tools/external/html-tools-main/xhs%20graphic%20production%20-%201.0.html)：`tools/external/html-tools-main/xhs graphic production - 1.0.html`。
- 初审用途：`exclusion_evidence`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`14a60fa5cc9fa3b7a8beac146277c1ef15729eb5e18cd7889fbcf498d5d1411a`。
- 选区：`[177,312)`；SHA-256：`abe37a7bfbc4b1035be0ff037decbc49b6f336a59e8b8e5501e810d721f45ab9`。

### S30

[来源文件](../tools/external/my-nvim/README.md)：`tools/external/my-nvim/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`905c3a248d5208f001f3eb6924beaf768454c70cdbc4c41cf67e906dba7ca8c0`。
- 选区：`[1,36)`；SHA-256：`5476e2380b6412a4d29ce37ad4ded76cd39bc5928e5cf716d98749f3ae8a31ea`。

### S31

[来源文件](../tools/external/my-nvim/nvim-config/init.lua)：`tools/external/my-nvim/nvim-config/init.lua`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`3b2d6e9976a515b7c8df08ed7c7f61a5751e9c08a6ff5579d621b87312c9e2c6`。
- 选区：`[1,3)`；SHA-256：`3b2d6e9976a515b7c8df08ed7c7f61a5751e9c08a6ff5579d621b87312c9e2c6`。

### S32

[来源文件](../tools/external/my-nvim/nvim-config/lua/config/lazy.lua)：`tools/external/my-nvim/nvim-config/lua/config/lazy.lua`。
- 初审用途：`exclusion_evidence`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`5fd03a47dc423a46b7c141149d35ba20cbbd96eb2c90f48f74dbff94c202802e`。
- 选区：`[1,56)`；SHA-256：`5fd03a47dc423a46b7c141149d35ba20cbbd96eb2c90f48f74dbff94c202802e`。

### S33

[来源文件](../tools/external/MCPlayerTransfer/README.md)：`tools/external/MCPlayerTransfer/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`f48b3081530011171ee6761115613c5eb7811a9ec3059cdec53e3b50c632f0e3`。
- 选区：`[1,47)`；SHA-256：`939c69119628dd9eea9c16461c41428db4e5faf6d7c9ab4024e7a2f8ffa0bce9`。

### S34

[来源文件](../tools/external/MCPlayerTransfer/main.py)：`tools/external/MCPlayerTransfer/main.py`。
- 初审用途：`exclusion_evidence`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`11bfdb47774247c32ad8cd0de441d56a13a17e9c12bcb3e2d9e81895958e1450`。
- 选区：`[1,51)`；SHA-256：`11bfdb47774247c32ad8cd0de441d56a13a17e9c12bcb3e2d9e81895958e1450`。

### S35

[来源文件](../tools/external/XHS-image-to-PDF-conversion/README.md)：`tools/external/XHS-image-to-PDF-conversion/README.md`。
- 初审用途：`support`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`19f65c7b6afe56c57789a30d1aed3c214051474fd21ea97f1ec10cc1ec774f13`。
- 选区：`[21,51)`；SHA-256：`271e08cdfc793b500025c6d2f7d8e768a1ba6f5a03fe86b86f1aee5c5a2517de`。

### S36

[来源文件](../tools/external/XHS-image-to-PDF-conversion/pdf.py)：`tools/external/XHS-image-to-PDF-conversion/pdf.py`。
- 初审用途：`exclusion_evidence`（人工标注，不是自动语义批准）。
- 仓库：`.`；Git修订：`0a7fdf4ca54d2bb327dcdfc13e816da57ee9c4c2`。
- 完整文件SHA-256：`ee045272a0ba361676c1ee908758e7316e96438774716c79472fb05cc5055539`。
- 选区：`[17,120)`；SHA-256：`4b4eb47d3545b5bcba80384c1aa81cee4d973d006736ea7a664f69ef9b759e70`。

## 维护与未完成事项

```bash
make sync-faqi-catalog
make check-faqi-catalog
make test-faqi-catalog
```

检查复用jsonschema/PyYAML；表格由tabulate生成原生Markdown语法，并转义单元格内容；依赖图、来源、ID、选区、范围或只读视图漂移均失败，不联网补证或静默升级。
本表未批准独立审查、完整运行/效果、许可、部署、账户或硬件身份。重要性分级与正式效能评价分轴；任务合同、阈值校准、运行版与源码身份桥接及通用图节点的落地实例仍待核。
