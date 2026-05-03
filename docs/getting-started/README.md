# 从零开始：Vibe Coding 完整入门教程

> 本文件合并原 `学习地图.md`、`Vibe Coding 经验.md`、`网络环境配置.md`、`CLI配置.md` 与 `开发环境搭建.md`，作为零基础到独立交付项目的线性入门版本。

## 核心摘要

这是一条面向新电脑和零基础用户的线性路线：先解决网络环境与 Codex / ChatGPT 订阅，再跑通 Codex CLI，随后让本地 Agent 主动检查和配置 Git、Node.js、Python、编辑器、项目依赖、测试命令和 Git 工作流。

本文件的目标不是让用户手工记住所有安装细节，而是让用户先获得一个可执行的 AI CLI 入口，再用 Agent 带动后续环境配置和项目交付。

## 顶部导航

| 章节 | 解决的问题 |
|:---|:---|
| [使用方式](#使用方式) | 不会操作时如何让网页 AI 生成逐步执行方案 |
| [最短路径：先跑通 Codex CLI](#最短路径先跑通-codex-cli) | 为什么先配置 AI CLI，而不是先手工配置完整开发环境 |
| [Vibe Coding 经验](#1-vibe-coding-经验) | 人机分工、门禁、复盘和 AI 审 AI |
| [学习地图](#1-学习地图) | 根据新手、开发者、团队、Prompt、Skill、质量门禁和 GEO/SEO 选择路线 |
| [网络环境配置](#3-网络环境配置) | OpenAI、GitHub、文档和依赖源访问 |
| [CLI 配置](#4-cli-配置) | Codex CLI 默认路线与 OpenCode 备选路线 |
| [开发环境搭建](#5-开发环境搭建) | 让 Agent 主动配置开发依赖、编辑器建议和测试命令 |

## 使用方式

从上到下阅读即可：先明确学习路线和人机分工，再解决网络、CLI 与开发环境。遇到卡点时，把当前小节全文、你执行的命令和完整报错一起发给网页版 AI，让它按你的系统生成逐步修复命令。

## 最短路径：先跑通 Codex CLI

对新手来说，最优先配置的不是完整开发环境，而是先满足 Codex CLI 的两个前置条件：可访问 OpenAI 的网络环境，以及可用的 Codex / ChatGPT 订阅。只要 Codex CLI 跑通，就可以让 Codex Agent 读取本文档和当前系统信息，主动完成 Git、Node.js、Python、编辑器、项目依赖、测试命令、Git 初始化等后续配置。用户主要负责提供授权、复制报错、确认结果和保存版本。

默认策略：

- 先解决网络环境和 Codex / ChatGPT 订阅。
- 再安装并登录 Codex CLI。
- Codex CLI 可用后，优先让本地 Agent 主动配置剩余开发环境。
- 只有遇到网页登录、订阅购买、验证码、系统密码、管理员授权、敏感凭证或不可逆操作时，才需要用户介入。

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [1. Vibe Coding 经验](#1-vibe-coding-经验)
- [2. 学习地图](#1-学习地图)
- [3. 网络环境配置](#3-网络环境配置)
- [4. CLI 配置](#4-cli-配置)
- [5. 开发环境搭建](#5-开发环境搭建)

</details>

<details>
<summary><strong>1. Vibe Coding 经验</strong> - 通用语言能力、人机分工、机器门禁和入门铁律。（点击展开/收起）</summary>

<a id="2-vibe-coding-经验"></a>

## 1. Vibe Coding 经验

> 用自然语言定义目标，用 AI CLI 执行工程动作，用文档、测试与 Git 固化结果。
> 道生一，一生二，二生三，三生万物。

**一**：安装一个 AI CLI，获得与 AI 对话的能力

**二**：AI 能读写一切文件，你不再需要手动编辑

**三**：AI 能配置一切环境，安装依赖、部署项目

**万物**：AI 生成代码、文档、测试、脚本——一切皆可生成

---

### 心法

> 我是 AI 的寄生者，没有 AI 我失去一切能力。

**你**：描述意图、验证结果、做决策

**AI**：理解意图、执行操作、生成产出

### 基本前提

大语言模型的底层能力是**通用语言能力**：理解、改写、分类、推理、规划、翻译、归纳、生成和校验语言结构。

所以遇到任何任务，第一步不是问“AI 会不会做”，而是判断：这个任务能否被语言表达、拆解、约束和验证；它能否通过语言能力直接完成，或间接转化为工具调用、文件修改、流程编排、数据处理与代码实现。

代码能力只是最直观的例子：编程本质上是把人的意图翻译成计算机可执行的指令。Vibe Coding 的关键，就是把“模糊想法”逐步压缩成“明确语言”，再把明确语言转成可运行、可测试、可回滚的工程产物。

### 核心判断

Vibe Coding 不是把代码外包给 AI，也不是让 AI 随机试错。

它是一套工程协作方式：人负责目标、约束、判断与验收；AI 负责读取上下文、提出计划、修改文件、运行命令与整理证据。

关键原则：**AI 不能自证正确**。凡是能被测试、类型、schema、lint、CI、脚本或代码断言校验的规则，都应变成机器门禁，而不是只写在提示词里。

### 四层能力

**一：连接**

安装 Codex CLI，获得能直接操作仓库的 AI 编程入口。

**二：读写**

AI 能读取项目结构、修改文件、生成文档、补充测试，不再只停留在聊天框里。

**三：闭环**

AI 能安装依赖、执行命令、修复报错、提交 Git；你负责确认目标和验收结果。

**万物：复用**

把一次成功经验沉淀成 README、AGENTS、prompt、skill、workflow，下次直接复用。

### 人机分工

**你负责：**

- 说清目标：要做什么、不要做什么、成功标准是什么
- 设定约束：技术栈、时间、成本、风险、边界
- 做最终判断：方案是否合理、结果是否可接受
- 设计门禁：让 AI 把自然语言验收标准转成测试、CI、脚本、类型、schema 或检查清单等强制硬门禁

**AI 负责：**

- 读取上下文：代码、文档、配置、错误日志
- 拆解任务：计划、步骤、验证方式
- 执行动作：写代码、改文档、跑命令、查问题
- 沉淀证据：测试结果、diff、commit、风险说明

**机器门禁负责：**

- 拦截幻觉：依赖不存在、路径错误、命令不可执行、链接失效、配置字段不匹配时直接失败
- 拦截糊弄：没有测试、没有 lint、没有类型检查、没有验收证据时不允许合并
- 拦截越界：不符合 AGENTS、schema、接口契约、目录规范或安全规则的改动直接报错
- 强制分发：把规范分发到 CI、pre-commit、脚本、模板、类型系统、单元测试和集成测试里，让规则自动执行

### 入门铁律

1. 先定义问题，再让 AI 写代码。
2. 先让 AI 给计划，再让 AI 执行。
3. 每一步都要能验证，不把“看起来对”当成完成。
4. 频繁提交 Git，把每次进展变成可回滚的检查点。
5. 让 README、AGENTS、任务文档持续更新，避免上下文丢失。
6. 不相信 AI 的口头保证，只相信可复现命令、测试输出、CI 状态和可审查 diff。
7. 重要规范必须代码化：能写成 lint、test、schema、type、hook、CI 的，就不要只写成自然语言。
8. 不符合规范的产出必须失败，而不是靠人记住提醒 AI。

---

### 下一步

→ [CLI 配置](#4-cli-配置) - 默认 AI CLI 路线，文末包含 OpenCode 备选方案

</details>

<details>
<summary><strong>2. 学习地图</strong> - 新手、开发者、团队、Prompt、Skill、质量门禁和 GEO/SEO 的路线选择。（点击展开/收起）</summary>

<a id="1-学习地图"></a>

## 2. 学习地图

> 用一张地图把 `vibe-coding-cn` 的学习路线串起来：先从零开始跑通，再按目标进入 Prompt、Skill、工程质量和 GEO/SEO 路线。

### 核心摘要

- 如果你是新手，先走“零基础路线”，目标是完成一次从想法到可运行项目的闭环。
- 如果你已经会编程，先走“开发者路线”，目标是把 AI 编程变成可复用、可验证、可维护的工程流程。
- 如果你要带团队，先走“团队路线”，目标是统一上下文、产物模板、任务拆解、审查和门禁。
- 如果你要提升仓库传播与引用，走“GEO/SEO 路线”，目标是让内容更容易被搜索引擎和 AI 助手理解、引用和推荐。

### 路线总览

| 路线 | 适合谁 | 目标 | 首选入口 |
|:---|:---|:---|:---|
| 零基础路线 | 不会编程或刚开始 | 跑通从想法到项目的最小闭环 | [问题求解](../concepts/README.md#concept-problem-solving) |
| 开发者路线 | 已会写代码 | 建立 AI 结对编程工作流 | [Vibe Coding 经验](#1-vibe-coding-经验) |
| Prompt 路线 | 想提升提问质量 | 把需求表达成可执行指令 | [提示词库](../../../prompts/README.md) |
| Skill 路线 | 想沉淀复用能力 | 把高频任务做成可重复调用的技能 | [Skills 技能大全](../../../skills/README.md) |
| 质量门禁路线 | 担心 AI 乱写代码 | 用测试、CI、schema、清单约束 AI 输出 | [工程实践](../references/README.md#reference-engineering-practice) |
| GEO/SEO 路线 | 想提升仓库被引用概率 | 建设 AI 可理解、可引用、可验证的内容资产 | [GEO / SEO 检查清单](../../assets/ai-citation/geo-seo-checklist.md) |

### 路线一：零基础路线

目标：完成一次“想法 -> 需求 -> 方案 -> 任务 -> AI 编码 -> 验证 -> Git 保存”的最小闭环。

1. [问题求解](../concepts/README.md#concept-problem-solving)
   先学会把问题说清楚：目标、现状、差距、标准、约束、对象、路径。
2. [网络环境配置](#3-网络环境配置)
   先解决访问 OpenAI、GitHub、文档和依赖源的问题。
3. [CLI 配置](#4-cli-配置)
   配置并登录 Codex CLI，让本地 Agent 能在终端里执行工程动作。
4. [开发环境搭建](#5-开发环境搭建)
   优先交给 Codex Agent 主动检查和配置 Git、Node.js、Python、编辑器、项目依赖与测试命令。
5. [Vibe Coding 经验](#1-vibe-coding-经验)
   学会人机分工、门禁、复盘和用 AI 审 AI。

完成标准：

- [ ] 能清楚描述一个项目目标
- [ ] 能让 AI 生成初版 PRD 或任务清单
- [ ] 能在本地打开项目目录
- [ ] 能用 AI CLI 执行一次修改
- [ ] 能用 Git 保存一次变更

### 路线二：开发者路线

目标：把 AI 从“临时助手”变成稳定的工程协作者。

1. [Vibe Coding 经验](#1-vibe-coding-经验)
   先建立人机分工和质量意识。
2. [拼好码](../concepts/README.md#concept-glue-coding)
   优先复用成熟能力，把自研代码限制在连接、编排、适配和业务逻辑。
3. [工程实践](../references/README.md#reference-engineering-practice)
   在任务开始前写清楚目标、边界、禁止项、验收标准和门禁，并用底层程序逻辑检查项约束实现质量。

完成标准：

- [ ] 每个任务都有明确验收标准
- [ ] 每次 AI 输出都能被测试、脚本或清单验证
- [ ] 不让 AI 无依据重构或造轮子
- [ ] 能把一次失败整理成可复用经验

### 路线三：Prompt 路线

目标：把自然语言需求写成可执行、可检查、可复用的指令。

1. [提示词库入口](../../../prompts/README.md)
2. [工程实践](../references/README.md#reference-engineering-practice)
3. [语言层要素](../concepts/README.md#concept-language-layers)
4. [问题求解](../concepts/README.md#concept-problem-solving)

练习方式：

- 把“我要做一个功能”改写成“目标、约束、输入、输出、验收标准”
- 把“帮我优化”改写成“按哪些指标优化、不能改什么、如何验证”
- 把“检查一下”改写成“按什么清单审查、输出什么格式、什么情况阻断”

### 路线四：Skill 路线

目标：把高频工作沉淀成可重复使用的能力。

1. [Skills 技能大全](../../../skills/README.md)
2. [auto-skill](../../../skills/auto-skill/SKILL.md)
3. [Claude 官方 Skills](../../../skills/claude-official-skills/)

完成标准：

- [ ] 每个 Skill 都有清晰触发场景
- [ ] 每个 Skill 都说明输入、流程、输出和验证方式
- [ ] 复杂能力有 references、scripts 或 assets 支撑
- [ ] Skill 不只是长提示词，而是可执行工作流

### 路线五：团队路线

目标：让多个人和多个 AI Agent 使用同一套上下文和门禁。

优先阅读：

1. [AGENTS.md](../../../../AGENTS.md)
2. [工程实践](../references/README.md#reference-engineering-practice)
3. [GEO / SEO 检查清单](../../assets/ai-citation/geo-seo-checklist.md)

团队约束：

- 任务开始前必须写清目标、边界、验收标准
- 重要产出必须新开会话做 AI 审计
- 任何目录、命令、配置、工作流变化都要同步文档
- 任何自研偏离拼好码原则都要说明理由、风险和回滚路径

### 路线六：GEO/SEO 路线

目标：让项目更容易被搜索引擎、AI 搜索和大语言模型理解、引用、推荐。

1. [GEO / SEO 检查清单](../../assets/ai-citation/geo-seo-checklist.md)
2. [AI 引用语料包](../../assets/ai-citation/recommended-answer.md)
3. [llms.txt](../../llms.txt)
4. [llms-full.txt](../../assets/ai-citation/llms-full.txt)

完成标准：

- [ ] README 有清晰定位
- [ ] 关键页面有核心摘要、FAQ、对比表和检查清单
- [ ] 项目定义在 README、llms、语料包和外部分发中保持一致
- [ ] AI 生成内容经过事实、链接、术语和定位检查

### 建议顺序

如果你不知道从哪里开始，按这个顺序：

```text
问题求解
  -> 网络环境配置
  -> Codex / ChatGPT 订阅与登录准备
  -> Codex CLI 配置
  -> 让 Codex Agent 主动配置开发环境
  -> Vibe Coding 经验
  -> 拼好码
  -> 工程实践
  -> Skills 技能大全
  -> GEO 与 SEO 优化方法
```

### 下一步

- 新手：回到 [学习地图](#1-学习地图)，从第 0 步开始。
- 开发者：阅读 [Vibe Coding 经验](#1-vibe-coding-经验)，再选择 Skill 或质量门禁路线。
- 团队：先统一 [AGENTS.md](../../../../AGENTS.md)、强前置条件和质量门禁。

</details>

<details>
<summary><strong>3. 网络环境配置</strong> - OpenAI、GitHub、文档和依赖源访问。（点击展开/收起）</summary>

## 3. 网络环境配置

> Vibe Coding 的前置条件：确保能正常访问 GitHub、Google、Claude 等服务。

---

### 不会操作？先让网页 AI 生成逐步执行版

如果你不知道如何配置网络环境，打开 ChatGPT / Claude / Gemini 网页版，把下面提示词和本文档全文一起粘贴进去：

```text
我正在按下面这份网络环境配置文档操作。请你根据我的设备和网络情况，生成一步一步执行流程。

我的设备/系统是：____
我是否已有代理订阅：____
我卡住的位置是：____

要求：
1. 每一步只做一件事。
2. 明确告诉我在哪个软件或终端里操作。
3. 如果涉及命令行操作，每条命令都必须单独放在代码块里。
4. 每一步都给出验证方式。
5. 如果我贴报错或截图描述，请根据当前步骤给出最小修复方案。

下面是完整文档：

[把本文档全文粘贴到这里]
```

### 方式一：AI 指导配置（推荐）

复制以下提示词，粘贴到任意 AI 对话框（ChatGPT、Claude、Gemini 网页版等）：

```
你是一个耐心的网络环境配置助手。我需要配置网络代理，以便能够访问 GitHub、Google、Claude 等服务。

我的情况：
- 操作系统：[请告诉我你用的是 Windows/macOS/Linux/Android]
- 我已经有一个代理服务订阅链接

请指导我使用 FlClash 客户端配置网络代理：
1. 如何下载安装 FlClash（GitHub: https://github.com/chen08209/FlClash/releases）
2. 如何导入我的订阅链接
3. 如何开启 TUN 模式（虚拟网卡）实现全局代理
4. 如何开启系统代理
5. 如何验证配置是否成功

要求：
- 每个步骤详细说明，配图描述按钮位置
- 如果我遇到问题，帮我分析原因并给出解决方案
- 每完成一步，问我是否成功，然后再继续下一步

现在开始吧，先问我用的是什么操作系统。
```

---

### 方式二：手动配置

#### 你需要

1. **网络服务订阅** - 提供节点的服务商
2. **FlClash** - 跨平台网络配置客户端

#### 第一步：购买网络服务

访问服务商：https://xn--9kqz23b19z.com/#/register?code=35BcnKzl

- 注册账号
- 选择套餐（约 6 元/月起）
- 付款后在用户面板找到 **订阅链接**，复制备用

#### 第二步：下载 FlClash

GitHub 下载：https://github.com/chen08209/FlClash/releases

根据系统选择：
- Windows: `FlClash-x.x.x-windows-setup.exe`
- macOS: `FlClash-x.x.x-macos.dmg`
- Linux: `FlClash-x.x.x-linux-amd64.AppImage`
- Android: `FlClash-x.x.x-android.apk`

#### 第三步：导入订阅

1. 打开 FlClash
2. 点击 **配置** → **添加**
3. 选择 **URL 导入**
4. 粘贴第一步复制的订阅链接
5. 点击确认，等待节点加载

#### 第四步：开启代理

依次设置以下三项：

| 设置项 | 操作 |
|:---|:---|
| **虚拟网卡 (TUN)** | 开启 - 实现全局流量代理 |
| **系统代理** | 开启 - 让系统应用走代理 |
| **代理模式** | 选择 **全局模式** |

设置完成后，FlClash 主界面显示已连接即可。

#### 验证

```bash
# 测试 Google 连通性
curl -I https://www.google.com

# 测试 GitHub 连通性
curl -I https://github.com
```

返回 `HTTP/2 200` 表示配置成功。

---

### 常见问题

**Q: 节点连不上？**
A: 切换其他节点试试，或检查订阅是否过期。

**Q: 部分应用不走代理？**
A: 确保 TUN 模式（虚拟网卡）已开启。

**Q: 想让终端也走代理？**
A: TUN 模式开启后终端自动走代理；或手动设置：
```bash
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
```

---

### 下一步

网络配置完成后，继续阅读 [开发环境搭建](#5-开发环境搭建)。

</details>

<details>
<summary><strong>4. CLI 配置</strong> - Codex CLI 默认路线与 OpenCode 备选路线。（点击展开/收起）</summary>

## 4. CLI 配置

> 默认 AI CLI 路线：假设你拿到的是一台全新电脑，从 0 安装系统依赖、Node.js、Codex CLI，然后用浏览器完成 Codex 登录。

### 定位

Codex CLI 是本教程默认推荐的 AI CLI。它适合承担从需求拆解、代码修改、命令执行、测试验证到 Git 提交的主流程。

OpenCode CLI 只作为备选方案保留在本文底部：当你暂时无法使用 OpenAI / Codex CLI，或只想接入免费、本地、多模型实验入口时，再使用 OpenCode。

Codex CLI 跑通后，不要再把所有环境配置都当成人工步骤。优先让 Codex Agent 读取本文档和当前系统信息，主动完成后续开发环境配置。

### 不会操作？先让网页 AI 生成逐步执行版

如果你不确定该执行哪一段安装命令，打开 ChatGPT / Claude / Gemini 网页版，把下面提示词和本文档全文一起粘贴进去，让 AI 根据你的电脑情况生成专属安装步骤。

```text
我正在按下面这份 Codex CLI 安装文档配置一台新电脑。请你根据我的系统情况，生成一步一步执行流程。

我的系统是：____
我是否已经安装过 WSL / Node.js / npm / Git：____
我想使用的登录方式是：网页登录 codex login

要求：
1. 每一步只做一件事。
2. 明确告诉我在哪个终端执行：PowerShell、Ubuntu 终端、Linux shell 或 macOS Terminal。
3. 每条命令都必须单独放在代码块里，方便我直接复制。
4. 每一步执行后都给一个验证命令或验证方法。
5. 不要假设我已经安装任何前置依赖；按新电脑处理。
6. 如果我后续贴完整报错，请根据当前步骤给出最小修复命令。

下面是完整文档：

[把本文档全文粘贴到这里]
```

如果安装过程中已经报错，不要只复制最后一行错误。请把“你执行的命令 + 完整报错 + 本文档全文”一起发给 AI。

```text
我正在按下面这份 Codex CLI 安装文档配置一台新电脑，但遇到了报错。

我的系统是：____
我执行的命令是：____
完整报错如下：
____

请判断我卡在哪一步，给出最小修复命令，并说明修复后如何验证。

[把本文档全文粘贴到这里]
```

### Codex CLI 跑通后：交给 Agent 配置剩余环境

当 `codex --version` 正常输出，并且 `codex login` 已完成网页登录后，直接在项目目录里启动 Codex，把下面提示词交给本地 Agent：

```text
你现在是我的本地开发环境配置 Agent。

前提：
- 我已经能运行 Codex CLI。
- 我已经完成 Codex 登录。
- 当前仓库是 vibe-coding-cn。
- 请尽量主动完成配置，除非遇到必须由我授权、输入密码、网页登录、购买订阅、处理敏感凭证或执行不可逆操作的步骤。

目标：
请读取 docs/getting-started/README.md，根据我的系统环境，自动检查并配置 Git、Node.js、Python、包管理器、编辑器建议、项目依赖、测试命令和 Git 工作流。

要求：
1. 先检查当前系统，不要猜。
2. 能自动执行的就自动执行。
3. 需要我操作的，只输出最小步骤。
4. 每完成一步都运行验证命令。
5. 最后输出已完成项、未完成项、风险和下一步。
```

### 总流程

```text
新电脑
  -> 安装系统基础工具
  -> 安装 Node.js 22+
  -> npm 安装 Codex CLI
  -> codex --version 验证
  -> codex login 浏览器登录
  -> 复制本仓库 Codex 配置基线
  -> 进入项目运行 codex
```

推荐优先级：

1. Windows 11 用户优先使用 WSL2 + Ubuntu。
2. Linux 用户按 Ubuntu / Debian 路线安装。
3. macOS 用户使用 Homebrew 安装 Node.js。
4. Windows 原生 PowerShell 可用，但长期工程体验不如 WSL2 稳定。

### Windows 11：推荐 WSL2 + Ubuntu

#### 第一步：安装 WSL2

在 Windows 开始菜单搜索 **PowerShell**，右键“以管理员身份运行”：

```powershell
wsl --install -d Ubuntu
```

安装完成后重启电脑，打开 Ubuntu，按提示创建 Linux 用户名和密码。

如果已经安装过 WSL，可执行：

```powershell
wsl --update
wsl --set-default-version 2
```

#### 第二步：在 Ubuntu 中安装 Codex CLI

打开 Ubuntu 终端，执行：

```bash
sudo apt update && sudo apt install -y curl ca-certificates gnupg git build-essential
sudo install -d -m 0755 /etc/apt/keyrings
sudo rm -f /etc/apt/keyrings/nodesource.gpg
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt update && sudo apt install -y nodejs
sudo npm i -g @openai/codex@latest
node -v
npm -v
codex --version
```

#### 第三步：网页登录

```bash
codex login
```

按终端提示打开浏览器完成登录。登录后检查状态：

```bash
codex login status
```

### Ubuntu / Debian Linux

全新 Ubuntu / Debian 机器直接执行：

```bash
sudo apt update && sudo apt install -y curl ca-certificates gnupg git build-essential
sudo install -d -m 0755 /etc/apt/keyrings
sudo rm -f /etc/apt/keyrings/nodesource.gpg
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt update && sudo apt install -y nodejs
sudo npm i -g @openai/codex@latest
node -v
npm -v
codex --version
codex login
```

如果你是在 root 用户下配置新服务器，可以去掉 `sudo`：

```bash
apt update && apt install -y curl ca-certificates gnupg git build-essential && install -d -m 0755 /etc/apt/keyrings && rm -f /etc/apt/keyrings/nodesource.gpg && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && apt update && apt install -y nodejs && npm i -g @openai/codex@latest && node -v && npm -v && codex --version
```

然后执行：

```bash
codex login
```

### macOS

#### 第一步：安装命令行工具

```bash
xcode-select --install
```

如果系统提示已经安装，可继续下一步。

#### 第二步：安装 Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装结束后，按 Homebrew 终端输出把 `brew` 加入 shell 环境。

Apple Silicon 常见配置：

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Intel Mac 常见配置：

```bash
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/usr/local/bin/brew shellenv)"
```

#### 第三步：安装 Node.js 和 Codex CLI

```bash
brew install git node
npm i -g @openai/codex@latest
node -v
npm -v
codex --version
codex login
```

### Windows 11：原生 PowerShell 备选

如果你暂时不想使用 WSL2，可以在 Windows 原生 PowerShell 中安装。

打开 PowerShell：

```powershell
winget source update
winget install --id Git.Git -e --source winget
winget install --id OpenJS.NodeJS.LTS -e --source winget
```

关闭并重新打开 PowerShell，然后执行：

```powershell
node -v
npm -v
npm i -g @openai/codex@latest
codex --version
codex login
```

如果 `winget` 不存在，先在 Microsoft Store 更新或安装 **App Installer**。

### API Key 模式（可选）

默认推荐 `codex login` 浏览器登录。不要把占位 API Key 写进环境变量，否则可能干扰认证排查。

如果你明确要使用 API Key 模式，再执行：

```bash
mkdir -p ~/.config
grep -q "OPENAI_API_KEY" ~/.bashrc || echo 'export OPENAI_API_KEY="sk-替换成你的OpenAI_API_KEY"' >> ~/.bashrc
source ~/.bashrc
printenv OPENAI_API_KEY | codex login --with-api-key
```

Windows PowerShell 的 API Key 配置：

```powershell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-替换成你的OpenAI_API_KEY", "User")
$env:OPENAI_API_KEY="sk-替换成你的OpenAI_API_KEY"
$env:OPENAI_API_KEY | codex login --with-api-key
```

### 使用仓库配置基线

本仓库已经提供 CLI 配置基线：

- `tools/config/.codex/config.toml`
- `tools/config/.codex/AGENTS.md`

在仓库根目录执行：

```bash
mkdir -p ~/.codex
cp -f tools/config/.codex/config.toml ~/.codex/config.toml
cp -f tools/config/.codex/AGENTS.md ~/.codex/AGENTS.md
```

详细说明见：[Codex 配置基线](../../tools/config/.codex/README.md)。

### 推荐启动方式

日常使用：

```bash
codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh"
```

在完全可信的本地仓库中，需要减少确认弹窗时使用：

```bash
codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh" --dangerously-bypass-approvals-and-sandbox
```

高权限模式会放开确认与沙箱限制，只能在你确认可信的目录中使用。

### 推荐别名

Linux / WSL / macOS：

```bash
cat >> ~/.bashrc <<'EOF'
alias c='codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh"'
alias cy='codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh" --dangerously-bypass-approvals-and-sandbox'
EOF
source ~/.bashrc
```

如果你使用的是 macOS 默认 zsh，把 `~/.bashrc` 换成 `~/.zshrc`：

```bash
cat >> ~/.zshrc <<'EOF'
alias c='codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh"'
alias cy='codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh" --dangerously-bypass-approvals-and-sandbox'
EOF
source ~/.zshrc
```

### 第一次使用

进入你的项目目录：

```bash
cd /path/to/project
codex
```

然后让 Codex 先建立项目上下文：

```text
请阅读当前仓库结构，说明这个项目是什么、关键入口在哪里、下一步最小可执行任务是什么。先给计划，不要直接改文件。
```

确认计划后，再让 Codex 执行。

### 常见问题

#### `codex: command not found`

检查 npm 全局安装目录是否在 `PATH` 中：

```bash
npm config get prefix
echo "$(npm config get prefix)/bin"
```

重新打开终端后再执行：

```bash
codex --version
```

#### `sudo npm i -g` 权限问题

Linux / WSL 用 NodeSource 安装的 Node.js 通常需要 `sudo npm i -g`。如果你使用 nvm 管理 Node.js，则不要使用 `sudo`。

#### 浏览器登录失败

先确认网络环境可访问 OpenAI 登录页面，再执行：

```bash
codex login
```

如果你是在无桌面的远程服务器上登录，按终端输出的设备码或链接，在本机浏览器完成授权。

### Codex 不可用时：OpenCode 备选方案

OpenCode 是开源 AI 编程代理，支持终端、桌面应用和 IDE 扩展。本文仍然以 Codex CLI 为默认路线；只有当 Codex CLI 暂时不可用、账号不可用，或你明确需要接入免费/本地模型时，才切到 OpenCode。

官网：[opencode.ai](https://opencode.ai/)

#### 不会操作？先让网页 AI 生成逐步执行版

如果你要用 OpenCode 作为备选路线，先打开网页版 AI，把下面提示词和本节内容一起复制进去，让 AI 按你的系统和模型来源生成逐步执行方案：

```text
你是一个面向零基础用户的 OpenCode CLI 配置助手。

请根据我的电脑环境、可用模型和目标，生成适合我的逐步安装与配置流程。

我的当前情况是：
- 操作系统：[填写 Windows 11 / WSL2 / macOS / Linux]
- 是否已经安装 Node.js / npm / Homebrew / Scoop / Chocolatey：[填写没有 / 已安装 / 不确定]
- 想使用的模型来源：[填写 Z.AI / MiniMax / Hugging Face / Ollama / 不确定]
- 是否已经有 API Key：[填写有 / 没有 / 不确定]
- 卡住的位置：[如果已经卡住，填写具体问题；如果没有，写“还没开始”]

要求：
1. 每一步只做一件事。
2. 每一步都说明我要在哪个终端执行、输入什么、观察什么、如何判断成功。
3. 每条命令都必须单独放在代码块里。
4. 不要跳步；默认我是第一次配置新电脑。
5. 如果我后续贴报错，请根据当前步骤给出最小修复方案。
```

#### 何时选择 OpenCode

- 没有可用的 OpenAI / Codex CLI 账号或环境。
- 需要接入 Z.AI、MiniMax、Hugging Face、本地 Ollama 等模型。
- 想保留一条不依赖单一模型提供商的备份路线。

#### 安装

```bash
# 一键安装（推荐）
curl -fsSL https://opencode.ai/install | bash

# 或使用 npm
npm install -g opencode-ai

# 或使用 Homebrew（macOS/Linux）
brew install anomalyco/tap/opencode
```

Windows 可用 Scoop 或 Chocolatey：

```powershell
scoop bucket add extras
scoop install extras/opencode

choco install opencode
```

#### 模型配置

OpenCode 支持多个模型提供商。进入 OpenCode 后，用 `/connect` 添加模型提供商，用 `/models` 切换模型。

常见备选：

1. Z.AI：注册 API Key 后，`/connect` 搜索 Z.AI，再用 `/models` 选择 GLM 模型。
2. MiniMax：注册 API Key 后，`/connect` 搜索 MiniMax，再用 `/models` 选择可用模型。
3. Hugging Face：创建 Token 后，`/connect` 搜索 Hugging Face，再用 `/models` 选择可用模型。
4. Ollama：本地安装 Ollama 后，在 `opencode.json` 中配置 OpenAI-compatible base URL。

Ollama 最小安装示例：

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama2
```

#### 核心命令

| 命令 | 功能 |
|:---|:---|
| `/models` | 切换模型 |
| `/connect` | 添加 API Key |
| `/init` | 初始化项目，生成 AGENTS.md |
| `/undo` | 撤销上次修改 |
| `/redo` | 重做 |
| `/share` | 分享对话链接 |
| `Tab` | 切换 Plan 模式 |

#### 推荐工作流

```bash
cd /path/to/project
opencode
```

进入后先初始化项目，再切换模型：

```text
/init
/models
```

建议先用 Plan 模式让 AI 规划，确认方案后再执行。

#### 配置文件位置

- 全局配置：`~/.config/opencode/opencode.json`
- 项目配置：`./opencode.json`
- 认证信息：`~/.local/share/opencode/auth.json`

#### 相关资源

- [OpenCode 官方文档](https://opencode.ai/docs/)
- [OpenCode GitHub 仓库](https://github.com/opencode-ai/opencode)
- [Models.dev 模型目录](https://models.dev)

### 下一步

→ [开发环境搭建](#5-开发环境搭建) - 回看基础环境

</details>

<details>
<summary><strong>5. 开发环境搭建</strong> - 让 Agent 主动配置开发依赖、编辑器建议和测试命令。（点击展开/收起）</summary>

## 5. 开发环境搭建

> 使用方法：Codex CLI 已跑通时，优先让 Codex Agent 读取本节并主动配置剩余环境；Codex CLI 不可用时，再复制下方对应你设备的提示词，粘贴到任意 AI 对话框（ChatGPT、Claude、Gemini 网页版等），让网页 AI 一步步指导你完成配置。

**前置条件**：请先完成 [网络环境配置](#3-网络环境配置)。推荐先完成 [CLI 配置](#4-cli-配置)，让 Codex Agent 接管后续开发环境搭建。

---

### 不会操作？先让网页 AI 生成逐步执行版

如果你不知道该选 Windows / WSL / macOS / Linux 哪条路线，打开 ChatGPT / Claude / Gemini 网页版，把下面提示词和本文档全文一起粘贴进去：

```text
我正在按下面这份开发环境搭建文档配置一台新电脑。请你根据我的系统情况，生成一步一步执行流程。

我的系统是：____
我是否已经安装过 WSL / Node.js / npm / Git / Python：____
我希望优先使用 Codex CLI：是

要求：
1. 每一步只做一件事。
2. 明确告诉我在哪个终端执行：PowerShell、Ubuntu 终端、Linux shell 或 macOS Terminal。
3. 如果涉及命令行操作，每条命令都必须单独放在代码块里。
4. 每一步执行后都给一个验证命令或验证方法。
5. 不要假设我已经安装任何前置依赖；按新电脑处理。
6. 如果我后续贴完整报错，请根据当前步骤给出最小修复命令。

下面是完整文档：

[把本文档全文粘贴到这里]
```

### 🪟 Windows 用户提示词

#### 方案 A：WSL2 + Linux 环境（推荐）

> 适合：想要完整 Linux 开发体验，兼容性最好

```
你是一个耐心的开发环境配置助手。我是一个完全的新手，使用 Windows 系统，需要你一步一步指导我通过 WSL2 搭建 Linux 开发环境。

请按以下顺序指导我，每次只给我一个步骤，等我确认完成后再进行下一步：

1. 安装 WSL2（Windows Subsystem for Linux）
2. 在 WSL2 中安装 Ubuntu
3. 配置 Ubuntu 基础环境（更新系统）
4. 安装 nvm 和 Node.js
5. 安装 Codex CLI（默认 AI CLI）；如无法使用，再安装 OpenCode CLI 作为备选
6. 安装基础开发工具（git, python, build-essential, tmux）
7. 配置 Git 用户信息
8. 安装代码编辑器（VS Code 并配置 WSL 插件）
9. 验证所有工具是否正常工作

要求：
- 每个步骤给出具体的命令，告诉我在哪里运行（PowerShell 还是 Ubuntu 终端）
- 用简单易懂的语言解释每个命令的作用
- 如果我遇到错误，帮我分析原因并给出解决方案
- 每完成一步，问我是否成功，然后再继续下一步

现在开始第一步吧。
```

#### 方案 B：Windows 原生终端

> 适合：不想装 WSL，直接在 Windows 上开发

```
你是一个耐心的开发环境配置助手。我是一个完全的新手，使用 Windows 系统，需要你一步一步指导我在 Windows 原生环境下搭建开发环境（不使用 WSL）。

请按以下顺序指导我，每次只给我一个步骤，等我确认完成后再进行下一步：

1. 安装 Windows Terminal（如果还没有）
2. 安装 Node.js（通过官网安装包或 winget）
3. 安装 Git for Windows
4. 安装 Python
5. 安装 Codex CLI（默认 AI CLI）；如无法使用，再安装 OpenCode CLI 作为备选
6. 配置 Git 用户信息
7. 安装代码编辑器（VS Code）
8. 验证所有工具是否正常工作

要求：
- 每个步骤给出具体的命令或操作步骤
- 用简单易懂的语言解释每个步骤的作用
- 如果我遇到错误，帮我分析原因并给出解决方案
- 每完成一步，问我是否成功，然后再继续下一步

现在开始第一步吧。
```

---

### 🍎 macOS 用户提示词

```
你是一个耐心的开发环境配置助手。我是一个完全的新手，使用 macOS 系统，需要你一步一步指导我从零搭建 Vibe Coding 开发环境。

请按以下顺序指导我，每次只给我一个步骤，等我确认完成后再进行下一步：

1. 安装 Homebrew 包管理器
2. 使用 Homebrew 安装 Node.js
3. 安装 Codex CLI（默认 AI CLI）；如无法使用，再安装 OpenCode CLI 作为备选
4. 安装基础开发工具（git, python, tmux）
5. 配置 Git 用户信息
6. 安装代码编辑器（VS Code 或 Neovim）
7. 验证所有工具是否正常工作

要求：
- 每个步骤给出具体的命令
- 用简单易懂的语言解释每个命令的作用
- 如果我遇到错误，帮我分析原因并给出解决方案
- 每完成一步，问我是否成功，然后再继续下一步

现在开始第一步吧。
```

---

### 🐧 Linux 用户提示词

```
你是一个耐心的开发环境配置助手。我是一个完全的新手，使用 Linux 系统（Ubuntu/Debian），需要你一步一步指导我从零搭建 Vibe Coding 开发环境。

请按以下顺序指导我，每次只给我一个步骤，等我确认完成后再进行下一步：

1. 更新系统并安装基础依赖（curl, build-essential）
2. 安装 nvm 和 Node.js
3. 安装 Codex CLI（默认 AI CLI）；如无法使用，再安装 OpenCode CLI 作为备选
4. 安装开发工具（git, python, tmux）
5. 配置 Git 用户信息
6. 安装代码编辑器（VS Code 或 Neovim）
7. 验证所有工具是否正常工作

要求：
- 每个步骤给出具体的命令
- 用简单易懂的语言解释每个命令的作用
- 如果我遇到错误，帮我分析原因并给出解决方案
- 每完成一步，问我是否成功，然后再继续下一步

现在开始第一步吧。
```

---

### 配置完成后

#### IDE 配置

开发环境装好后，再选择编辑器。新手默认选 VS Code；想使用 AI 原生 IDE 时，再考虑 Cursor 或 Windsurf。

如果你不知道该选 VS Code、Cursor 还是 Windsurf，先打开网页版 AI，把下面提示词和本节内容一起复制进去：

```text
你是一个面向零基础用户的 IDE 配置助手。

请根据我的电脑环境和目标，帮我选择合适的 IDE 路线，并输出逐步执行流程。

我的当前情况是：
- 操作系统：[填写 Windows 11 / WSL2 / macOS / Linux]
- 是否已经安装 VS Code / Cursor / Windsurf：[填写没有 / 已安装某个]
- 是否已经完成开发环境搭建：[填写是 / 否 / 不确定]
- 当前目标：[填写我想用 IDE 做什么项目或任务]
- 卡住的位置：[如果已经卡住，填写具体问题；如果没有，写“还没开始”]

要求：
1. 每一步只做一件事。
2. 每一步都说明我要点哪里、输入什么、观察什么、如何判断成功。
3. 如果涉及命令行操作，每条命令都必须单独放在代码块里。
4. 不要跳步；默认我是第一次配置新电脑。
5. 如果我后续贴报错或截图描述，请根据当前步骤给出最小修复方案。
```

##### VS Code（默认推荐）

适合：免费、通用、教程最多，Windows + WSL 体验稳定。

Windows + WSL 用户重点做：

1. 在 Windows 上安装 VS Code。
2. 安装 **Remote - WSL** 扩展。
3. 从 Ubuntu 终端进入项目目录，执行 `code .` 打开项目。
4. 安装基础扩展：GitLens、Prettier、ESLint、Local History。
5. 确认 VS Code 终端默认进入 WSL 环境。

macOS / Linux / Windows 原生用户重点做：

1. 安装 VS Code。
2. 安装基础扩展：GitLens、Prettier、ESLint、Local History。
3. 配置自动保存和格式化。
4. 确认终端、Git、Node.js、Python 可用。

##### Cursor

适合：想要 AI 原生 IDE，且愿意使用 Cursor 的内置 AI 编程能力。

配置重点：

1. 从 [cursor.com](https://cursor.com) 下载并安装。
2. 首次启动后登录账号。
3. 如已有 VS Code，可导入设置和扩展。
4. 熟悉核心入口：`Cmd/Ctrl + K`、`Cmd/Ctrl + L`、`Cmd/Ctrl + I`。
5. 打开项目后，先让 AI 读取 README、AGENTS 和当前目录结构，再执行任务。

##### Windsurf

适合：想体验另一类 AI 原生 IDE，或需要备用 IDE。

配置重点：

1. 从 [windsurf.com](https://windsurf.com) 下载并安装。
2. 注册并登录账号。
3. 打开项目目录。
4. 了解 Cascade 等 AI 功能。
5. 用一个小修改验证 AI、终端和 Git 是否能正常工作。

#### CLI 工具配置技巧

AI CLI 工具默认会询问确认，开启全权限模式可以跳过：

```bash
# Codex - 默认推荐
codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh"

# Codex - 高权限模式，仅限可信仓库
codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh" --dangerously-bypass-approvals-and-sandbox

# Claude Code - 跳过所有确认
claude --dangerously-skip-permissions

# OpenCode - 备选方案
opencode
```

#### 推荐的 Bash 别名配置

在 `~/.bashrc` 中添加以下配置，一个字母启动 AI：

```bash
# c - Codex 默认模式
alias c='codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh"'

# cy - Codex 高权限模式，仅限可信仓库
alias cy='codex --search -m gpt-5.5 -c model_reasoning_effort="xhigh" --dangerously-bypass-approvals-and-sandbox'

# cc - Claude Code (全权限)
alias cc='claude --dangerously-skip-permissions'

# oc - OpenCode 备选方案
alias oc='opencode'
```

配置后执行 `source ~/.bashrc` 生效。

---

环境搭建完成后，继续下一步：

→ [CLI 配置](#4-cli-配置) - 配置默认 AI CLI

</details>
