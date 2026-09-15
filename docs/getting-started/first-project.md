<a id="first-project"></a>

# 第一个项目：完成一次可验证闭环

> 用一个不依赖框架、不需要账号、可以在本地打开的待办清单，把“想法 → 需求 → 计划 → AI 执行 → 本地运行 → 验收 → Git 保存”完整走一遍。

## 核心摘要

- 本教程的目标不是做出生产级产品，而是亲手完成第一次可验证的状态转移。
- 项目使用原生 HTML、CSS 和 JavaScript，不安装 npm 包，不接入数据库，不调用外部 API。
- AI 负责读取上下文、提出计划和修改文件；你负责确认范围、观察结果和判断是否通过。
- 每一步都有成功判断；没有通过验收时，不进入下一步，也不提交 Git。

## 你将完成什么

### 项目范围

制作一个离线待办清单，包含：

1. 新增一条非空任务。
2. 显示任务列表和空状态。
3. 标记任务已完成或恢复未完成。
4. 删除任务。
5. 使用浏览器 `localStorage` 保存任务，刷新页面后数据仍然存在。
6. 为输入框、按钮和任务状态提供清晰的文字或无障碍标签。
7. 在窄屏幕下仍然可以操作。

### 明确不做

- 不做登录、注册、用户权限和云同步。
- 不做后端、数据库、支付和部署。
- 不引入 React、Vue、Tailwind、构建工具或第三方 CDN。
- 不把任何 Token、密码、个人信息或真实服务地址写入项目。

### 预期文件

```text
first-todo/
├── index.html
├── style.css
├── app.js
└── README.md
```

`README.md` 由 Agent 补充运行方式、功能说明和已知限制。文件数量不是目的；如果 Agent 提出新增依赖或额外目录，先要求它说明理由，不要默认接受。

## 开始前检查

### 前置条件

| 条件 | 成功判断 |
|:---|:---|
| 已完成 [CLI 配置](cli-setup.md)，或手边有可读写当前目录的 AI 工具 | 能在当前目录启动 Agent，或能把文件保存到当前目录 |
| 已安装 Git | 执行 `git --version` 能看到版本号 |
| 已安装 Python 3 | 执行对应系统的 Python 版本命令能看到版本号 |
| 已有浏览器 | 能打开 `http://127.0.0.1:8000/` |

本项目不要求 Node.js 或 npm。若 `codex` 命令不存在，先回到 [CLI 配置](cli-setup.md)；若 Git 或 Python 不可用，先阅读 [开发环境搭建](development-environment.md)。

### 创建独立工作目录

不要在已有重要项目中练习。选择一个你有权限写入的位置。

**Linux、macOS 或 WSL：**

```bash
mkdir -p "$HOME/vibe-projects/first-todo"
cd "$HOME/vibe-projects/first-todo"
pwd
```

**Windows PowerShell：**

```powershell
New-Item -ItemType Directory -Force "$HOME\vibe-projects\first-todo" | Out-Null
Set-Location "$HOME\vibe-projects\first-todo"
Get-Location
```

成功判断：终端当前路径的最后一段是 `first-todo`，且这是一个专门用于本教程的空目录。

<a id="first-project-define"></a>

## 第 1 步：先写清目标和验收标准

不要一开始就说“帮我做一个好看的待办应用”。把目标、边界和证据写成 Agent 可以执行的要求。

将下面提示词粘贴到当前目录中的 Agent 会话：

```text
我在当前目录创建一个用于学习的本地待办清单，请先不要修改文件，只阅读当前目录并输出实现计划。

目标：
- 创建一个不依赖框架、不依赖 npm、不调用外部网络的静态网页。
- 用户可以新增非空任务、标记完成、恢复未完成和删除任务。
- 任务通过浏览器 localStorage 持久化，刷新页面后仍然存在。
- 输入框、按钮、任务状态和空状态要让第一次使用的人看得懂；键盘可以完成基本操作。
- 页面在桌面和窄屏宽度下都能使用。

必须创建或修改的文件只有：
- index.html
- style.css
- app.js
- README.md

明确不做：登录、注册、后端、数据库、云同步、支付、第三方 CDN、第三方依赖和构建工具。

请先输出：
1. 文件职责；
2. 数据结构和状态变化；
3. 交互流程；
4. 验收清单；
5. 可能的风险和最小测试方式。

在我确认计划前，不要创建、删除或修改任何文件。
```

### 计划审查

看到计划后，逐项检查：

- 是否仍然是本地静态页面，而不是偷偷引入后端或依赖安装？
- 是否覆盖新增、完成、恢复、删除、刷新持久化和空输入？
- 是否说明了如何验证，而不是只描述“看起来正常”？
- 是否只触及约定的四个文件？
- 是否把不确定的产品决策列出来，而不是替你猜测？

计划超出范围时，先回复：`请缩回到最小范围，不增加依赖和后端，并重新列出计划。` 计划清晰且符合边界后，再确认执行。

<a id="first-project-implement"></a>

## 第 2 步：让 Agent 实现最小版本

确认计划后，发送下面的执行指令：

```text
按刚才确认的计划实现最小可用版本。

执行约束：
1. 只在当前目录工作，只创建或修改 index.html、style.css、app.js、README.md。
2. 不安装依赖，不调用网络，不使用外部 CDN，不写入 Token、密码或个人信息。
3. 先实现可用功能，再做有限的样式整理；不要顺手重构或增加未确认功能。
4. 对空输入、重复点击、任务不存在和 localStorage 数据损坏等边界情况给出稳定行为。
5. README.md 必须写清本地运行命令、功能、验收步骤和已知限制。
6. 完成后列出实际修改的文件、未完成事项和建议的验证命令；不要声称“已通过”而不提供证据。

现在开始修改。完成后先停止，等待我检查结果。
```

成功判断：Agent 报告的修改文件没有超出范围；四个文件存在；没有出现依赖清单、外部脚本链接或敏感信息。

可以用下列命令查看文件。Linux、macOS 或 WSL：

```bash
find . -maxdepth 1 -type f -print
```

Windows PowerShell：

```powershell
Get-ChildItem -File
```

<a id="first-project-run"></a>

## 第 3 步：在本地运行

在项目目录启动一个本地静态服务器。保持这个终端运行，再打开浏览器。

**Linux、macOS 或 WSL：**

```bash
python3 -m http.server 8000
```

**Windows PowerShell：**

```powershell
py -m http.server 8000
```

打开：`http://127.0.0.1:8000/`

成功判断：浏览器能显示待办清单页面，终端没有立即退出或打印 Python 异常。停止服务器时，在运行服务器的终端按 `Ctrl+C`。

如果 8000 端口已被占用，换成 8080：

**Linux、macOS 或 WSL：**

```bash
python3 -m http.server 8080
```

**Windows PowerShell：**

```powershell
py -m http.server 8080
```

然后打开 `http://127.0.0.1:8080/`。不要为了释放端口而结束你不认识的进程。

<a id="first-project-accept"></a>

## 第 4 步：按证据验收

不要只看页面是否“漂亮”。按下面顺序操作，并记录每项是否通过：

| 验收项 | 操作 | 通过标准 |
|:---|:---|:---|
| 初始状态 | 第一次打开页面 | 有清晰标题、输入入口和空状态；控制台没有明显错误 |
| 新增任务 | 输入“学习 Git”，提交一次 | 列表出现对应任务，输入框恢复可用 |
| 空输入 | 不输入内容直接提交，或只输入空格 | 不新增空任务，并给出可理解的提示 |
| 完成与恢复 | 点击任务完成控制，再点击一次 | 状态可在已完成与未完成之间切换，视觉和文字状态一致 |
| 持久化 | 刷新页面 | “学习 Git”仍然存在且状态正确 |
| 删除 | 删除该任务 | 任务从列表消失；页面回到正确的空状态 |
| 键盘操作 | 只用键盘聚焦输入框并提交 | 基本流程不依赖鼠标；焦点位置可辨认 |
| 窄屏 | 缩窄浏览器窗口或使用移动设备模拟 | 文本、按钮和输入框不重叠，仍可完成新增和删除 |
| 范围与隐私 | 查看源文件和浏览器网络面板 | 没有外部请求、凭据、个人信息或未确认功能 |

如果某项失败，不要直接让 Agent “全部重写”。先记录：操作、预期、实际结果、浏览器控制台错误和涉及文件。

<a id="first-project-review"></a>

## 第 5 步：进行一次隔离复核

同一个 Agent 既生成又宣布通过，证据强度较弱。重要任务应开启新的会话，或至少明确要求 Agent 暂时不相信上一轮结论。

把项目目录和下面的复核要求交给新的 AI 会话：

```text
请把当前项目当作一个不可信的候选实现，重新阅读 index.html、style.css、app.js 和 README.md，不沿用任何“已完成”结论。

按以下标准逐项检查：
- 只能离线运行，不依赖 npm、构建工具、外部 CDN 或外部 API。
- 可以新增非空任务、拒绝空输入、完成/恢复、删除。
- 刷新页面后 localStorage 数据仍然存在；异常数据不会让页面崩溃。
- 交互文字、键盘操作、焦点和窄屏布局基本可用。
- README 的运行命令和实际文件一致。

先输出“通过项、失败项、证据和风险”，不要修改文件。
```

把失败项与实际操作结果对照后，再让 Agent 只修复已确认的问题：

```text
只修复刚才列出的失败项，不增加新功能，不改变已通过行为。
修复后重新说明修改文件，并给出可以复现的验证步骤。
如果没有可靠证据，请明确写“未验证”。
```

修复后重复 [第 3 步](#first-project-run) 的运行和 [第 4 步](#first-project-accept) 的验收；不要用 Agent 的一句“应该可以”替代浏览器验证。

<a id="first-project-git"></a>

## 第 6 步：保存 Git 检查点

确认验收通过后再初始化 Git。先检查状态，避免把不认识的文件一并提交。

```bash
git init
git status --short
git add index.html style.css app.js README.md
git diff --cached --check
git commit -m "feat: create first todo project"
git status --short
git rev-parse --short HEAD
```

成功判断：

- `git diff --cached --check` 没有输出错误。
- commit 成功并返回短提交号。
- 最后的 `git status --short` 没有未提交的四个项目文件。

如果 commit 报“无法识别作者”，不要关闭检查；回到 [开发环境搭建](development-environment.md) 配置 Git 用户信息后，重新检查 `git status` 再提交。不要把 Token、密码或临时配置文件加入 Git。

## 完成证据

完成后至少保留以下信息：

```text
项目目录：first-todo
本地地址：http://127.0.0.1:8000/
验收结果：新增 / 空输入 / 完成恢复 / 刷新持久化 / 删除 / 键盘 / 窄屏
提交号：<git rev-parse --short HEAD 的输出>
已知限制：仅本地保存，无登录、后端和云同步
```

这份记录就是本次状态转移的证据：它说明了从哪个目录、经过哪些动作、以什么标准、到达了什么结果。失败项也应记录，不要为了“看起来完成”而删除。

## 常见失败与最小处理

| 现象 | 先检查 | 最小处理 |
|:---|:---|:---|
| `codex` 找不到 | 是否完成 CLI 配置、当前终端是否重启 | 回到 [CLI 配置](cli-setup.md)，不要手动猜安装路径 |
| `python3` 或 `py` 找不到 | 版本命令是否可用、PATH 是否更新 | 回到 [开发环境搭建](development-environment.md)，完成 Python 配置后重开终端 |
| 浏览器显示目录列表 | `index.html` 是否存在且文件名大小写正确 | 让 Agent 只检查文件名和当前目录，不要先重写全部代码 |
| 页面空白 | 浏览器控制台第一条错误、脚本路径和 HTML 元素 ID | 把完整错误和相关文件交给 Agent，要求最小修复 |
| 刷新后任务消失 | `localStorage` 的 key、序列化格式和浏览器站点地址是否变化 | 先检查实现和控制台，再补持久化测试 |
| 端口被占用 | 是否只是已有本地服务在使用 | 改用 8080；不要结束不认识的进程 |
| Agent 添加了依赖或外部链接 | `git status`、文件中的 `<script src>` 和 `package.json` | 停止执行，要求回到本教程的范围并解释偏离原因 |
| Git 提交包含陌生文件 | `git status --short` | 撤销暂存的陌生文件：`git restore --staged <文件路径>`，然后重新检查 |

## 下一步

- 想理解为什么要先定义目标、现状和标准：阅读 [问题求解](../concepts/problem-solving.md)。
- 想把目标、约束、行动、证据和版本串起来：阅读 [Vibe Coding 状态转移闭环](../concepts/vibe-coding-state-transition.md)。
- 想学习更完整的人机分工、机器门禁和复盘：阅读 [Vibe Coding 经验](vibe-coding-experience.md)。
- 想把一次练习升级为可维护项目：阅读 [项目架构模板](../references/project-architecture-template.md) 和 [开发流程](../workflow/development-process.md)。
