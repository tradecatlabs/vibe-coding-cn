<a id="learning-map"></a>
<a id="1-学习地图"></a>

# Pi CLI 上手指南：从新电脑准备到安装后使用

## 字多不看

- 按本文顺序完成：检查现状、准备网络、安装 CLI、验证安装；连接模型和开始项目是后续独立步骤。
- 常规安装/更新和云端模型使用需要联网。本仓主路线 Pi + OpenAI GPT 还需要当前终端能够访问 OpenAI 登录与推理服务；安装源和模型服务不是同一个网络目标。
- `pi --version` 只证明 CLI 可运行，不证明模型已经授权或项目任务已完成。已准备好的本地模型可能离线使用。
- 官方 shell/PowerShell 安装器和 npm 路线要求 Node.js 22.19.0 或更高版本及 npm；安装器可能协助安装 Node、修改用户 PATH 或调用系统包管理器。
- Windows 原生环境中的 Git Bash 只供 Pi 的内置 Bash 工具使用，不是 CLI 安装前提；WSL 是可选环境。
- Pi 以启动它的操作系统账户权限运行，不是安全沙箱。不要以管理员/root 启动；检查它执行的命令和改动，不要分享凭据。

## 快速导航

1. [第 1 步：确认系统与现有安装](#准备与系统要求)
2. [第 2 步：准备网络与依赖](#network-and-dependencies)
3. [第 3 步：安装 Pi CLI](#pi-cli-installation)
4. [第 4 步：验证 CLI，并选择是否连接模型](#verify-and-connect-a-model)
5. [第 5 步：在项目中使用](#post-install-use)
6. [常见问题](#常见问题)
7. [官方资料](#官方资料)
8. [网页 AI 单步引导提示词](#web-ai-walkthrough-prompt)
9. [可选练习：第一个项目](first-project.md)

<a id="准备与系统要求"></a>

## 第 1 步：确认系统与现有安装

先区分三个验收结果：

| 阶段 | 成功判断 | 不代表什么 |
|:---|:---|:---|
| CLI 已安装 | `pi --version` 输出版本号 | 不代表模型已授权或可用 |
| 模型已连接 | Pi 内完成 `/login`，选定模型后能得到回答 | 不代表开发环境或项目依赖已配置 |
| 项目任务已完成 | 按任务检查改动、运行结果和测试 | 不由安装成功或模型回答自动推出 |

Pi 官方 Quickstart 支持 macOS、Linux，并为 Windows 提供独立说明；Windows 可原生运行，也可在 WSL 内运行。选择你实际准备使用的终端；不要因为安装 Pi 就默认安装 WSL。

| 项目 | 要求或选择 | 说明 |
|:---|:---|:---|
| macOS | Terminal、`curl` 与 POSIX shell | 使用 Pi 官方 shell 安装器。 |
| Linux | 终端、`curl` 与 POSIX shell | 使用 Pi 官方 shell 安装器。 |
| Windows 原生 | PowerShell | 使用 Pi 官方 PowerShell 安装器；Windows 原生与 WSL 是两种独立环境。 |
| Node.js 与 npm | 官方主安装器及 npm 路线要求 Node.js 22.19.0 或更高版本和 npm | 缺少时，交互式安装器可提供安装路线；各系统区别见第 3 步。 |
| Windows 原生 Bash | 仅在需要 Pi 内置 Bash 工具或 `!` 命令时需要 Git Bash | 不是 `pi --version` 的前置条件；安装选项见第 3 步。 |
| Nix | 已经使用 Nix 的 macOS/Linux 用户可选 | 不需要为 Pi 专门安装 Nix。 |
| WSL、Git、Python、编辑器 | 按工作环境或具体项目选择 | 均不是安装 Pi CLI 的普遍前置条件。 |
| 网络 | 常规官方安装/更新与云端模型调用需要可用网络 | 安装源、包源和模型服务不同；本地版本检查及已准备好的本地模型可能离线。 |

在普通用户终端检查 Pi 是否已安装：

```bash
pi --version
```

Windows PowerShell 也运行同一条命令。若成功，跳过安装；若命令不存在，继续。不要以管理员/root 身份运行安装器。

<a id="network-and-dependencies"></a>

## 第 2 步：准备网络与依赖

联网是常规安装/更新和云端模型使用的必要环境条件，但不同阶段访问的目标不同。本仓主路线 Pi + OpenAI GPT 在线使用，需要从当前终端访问 OpenAI 认证与推理服务；安装脚本可访问，不代表模型提供方也可访问。

| 阶段 | 需要访问的服务（依安装路线） | 说明 |
|:---|:---|:---|
| 获取安装脚本和 Pi 发布信息 | Pi 官方 `pi.dev` 域名 | 使用下文列出的官方地址，不从第三方脚本站下载。 |
| 获取 Pi 包及依赖 | npm 官方包分发服务（通常为 `registry.npmjs.org`） | 官方托管安装会安装锁定的依赖。 |
| 自动安装 Node 或系统依赖 | Node.js 官方分发服务，或当前系统选择的包管理器源 | 是否访问取决于系统、已有 Node/npm 和安装器选择；系统包安装可能要求你确认权限。 |
| Windows 可选安装 Git Bash | 选择 Portable Git 时可能访问 `api.github.com` 和 GitHub 发布资产；若明确选择 winget，则使用其配置的包源 | 只有选择安装 Git Bash 时才涉及，不是 Pi CLI 安装本身的要求。具体下载地址以官方安装器当前输出为准。 |
| 已有 Nix 用户的可选路线 | GitHub 与本机 Nix 配置的缓存/包源 | 只有选择 Nix 路线时涉及。 |
| 登录和云端模型请求 | 用户选择的模型提供方及其认证服务 | 域名、账号权限、订阅/API 费用因提供方和登录方式而异。 |
| 网页 AI 协助 | 你所使用的网页 AI 服务 | 网页 AI 只读取你提交的内容，不会自动看到本机终端。 |

浏览器能够打开 Pi 官方文档，只能证明浏览器可访问；不能保证当前终端、包源或模型服务可访问。安装与模型登录要分别看实际结果。

Pi 官方资料没有覆盖所有平台、安装选项和模型提供方的通用网络白名单。公司/学校网络若拦截请求，根据安装器报错和当前官方说明确认具体目标，并遵守网络管理员要求；不要默认购买代理、启用全局代理/TUN、关闭 TLS/安全软件或换用来历不明的镜像。不要把代理口令或含凭据的日志发给 AI。

<a id="pi-cli-installation"></a>

## 第 3 步：安装 Pi CLI

先确认命令来自 [Pi 官方 Quickstart](https://pi.dev/docs/latest/quickstart)、[Windows 说明](https://pi.dev/docs/latest/windows)或[官方仓库 README](https://github.com/earendil-works/pi)。下面的 `curl | sh` 和 `irm | iex` 会把下载的脚本交给 shell 执行；核对域名和安装器提示。使用普通用户的交互式终端，不要用 `sudo` 或“以管理员身份运行”包装安装命令。

### macOS

在普通用户的 Terminal 中运行：

```bash
curl -fsSL https://pi.dev/install.sh | sh
```

安装器要求 Node.js 22.19.0 或更高版本和 npm；缺少时会询问是否安装。macOS 上若已有 Homebrew，安装器可能用它安装或更新 Node；否则会提供用户目录中的独立 Node 安装路线。不要为了 Pi 专门安装 Homebrew。读清安装器将执行的动作；不接受时取消，再从 [Node.js 官方下载页](https://nodejs.org/en/download)安装合格的 Node.js 和 npm 后重试。安装器若询问是否立即启动 Pi，可先选择暂不启动。官方安装器管理的 Pi 后续用 `pi update` 更新。

### Linux

在普通用户的 Linux 终端中运行：

```bash
curl -fsSL https://pi.dev/install.sh | sh
```

安装器要求 Node.js 22.19.0 或更高版本和 npm；缺少时会说明并询问是否安装。安装路线可能使用满足版本要求的 apt/apk 包，或用户目录中的独立 Node；系统包安装可能调用 `sudo`，读清提示后再决定。若不接受系统级动作，取消安装器，从 [Node.js 官方下载页](https://nodejs.org/en/download)安装合格的 Node.js 和 npm，再重试。不要用 `sudo curl ... | sh` 包装 Pi 安装命令。官方安装器管理的 Pi 后续用 `pi update` 更新。

### Windows 原生 PowerShell

在普通用户 PowerShell 中运行：

```powershell
powershell -c "irm https://pi.dev/install.ps1 | iex"
```

安装器要求 Node.js 22.19.0 或更高版本和 npm；若缺少，会询问是否安装独立 Node.js，并把它放在用户目录、加入当前用户 PATH。默认托管安装后可用 `pi update` 更新。若安装器显示更新、重装、卸载或迁移已有 Pi，先核对当前版本和目标路径，不要盲目接受。

Pi 在 Windows 原生环境中默认用 Git Bash 执行内置 Bash 工具和 `!` 命令；这不是安装 CLI 的前提。若找不到 Bash，安装器可提供 Portable Git（安装在 Pi 用户目录并修改 `~/.pi/agent/settings.json` 的 `shellPath`）、通过 winget 全局安装 Git for Windows（仅当 winget 可用），或跳过。也可自行安装[官方 Git for Windows](https://git-scm.com/download/win)。跳过不妨碍 CLI 安装，但 Bash 工具不可用。若询问是否立即启动 Pi，可先暂不启动，之后按第 4 步验证。

### WSL（可选）

如果你已经在 WSL 中开发，在目标发行版的 Linux 终端按上面的 Linux 路线安装。Windows 原生与 WSL 的安装目录和 PATH 相互独立；不要仅为安装 Pi 而配置 WSL，也不要在两个终端之间混用安装结果。

### 其他官方安装路线（可选）

- 已经使用 Nix 的 macOS/Linux 用户可按 [Pi Quickstart 的 Nix 说明](https://pi.dev/docs/latest/quickstart)安装。Nix 会按 Nix 路线更新，`pi update` 不负责更新 Nix 安装。
- 已有合格 Node.js 和 npm 的用户可使用官方 npm 备选命令：

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

官方 Quickstart 指出 npm 安装不会锁定传递依赖，新手通常优先使用平台安装器。全局 npm 权限报错时不要用 `sudo npm` 硬修；先停止，改选平台安装器或用户级 Node 环境。

<a id="verify-and-connect-a-model"></a>

## 第 4 步：验证 CLI，并选择是否连接模型

### 验证 CLI

在安装所用的同一个终端运行：

```bash
pi --version
```

出现版本号说明 CLI 已安装。若当前终端提示找不到命令，先关闭并重新打开终端，再核对安装器报告的 PATH 和安装位置；不要立刻重复安装。

### 连接模型（可选）

若需要 Pi 生成回答，在终端启动 `pi`，然后在 Pi 界面内运行：

```text
/login
```

本仓主体路线是 Pi 加经用户授权的 OpenAI GPT；选择你有权使用且当前可用的 OpenAI 认证方式。也可以选择其他受支持的模型提供方。随后用 `/model` 选择可用模型，并发送一条不要求修改文件的简单问题。云端模型需要相应的网络连接。ChatGPT 订阅不应被自动当成 OpenAI API 额度；不同路线的账号权限与费用不同。

若用 API Key，优先选择受信凭据管理器和 Pi 官方支持的安全读取方式；若通过 Pi 的 `/login` 交互录入，凭据可能保存在 `~/.pi/agent/auth.json`。该文件可能含 API Key 或 OAuth Token，必须保持私密，不得提交、上传或复制给网页 AI。不要把密钥、密码、Token、cookie、订阅链接或带凭据的截图贴进对话，也不要把凭据写进项目文件、脚本或 shell 配置。

若选择本地模型，还需按提供方另行准备本地运行时与模型资源；这不是 Pi CLI 安装的一部分。资源已经准备好后，本地模型可能离线使用。

<a id="post-install-use"></a>

## 第 5 步：在项目中使用

1. 进入你有权让 Pi 访问的项目目录，再运行 `pi`。在本仓库工作时，可从仓库根目录运行 `pi --skill .github/skills`，显式加载仓库 Skills；这不会把 `.github/extensions/` 整体作为 Pi 原生扩展加载。详见[根 README](../../../README.md)。不要以管理员/root 身份启动。
2. 用自然语言说明目标、当前状态、限制和验收标准。可以先要求 Pi 只检查现有环境和项目文件，报告所需工具、计划、风险与验证方式，暂不安装或修改。
3. 只配置当前任务确实需要的 Git、语言运行时、编辑器或项目依赖；Pi CLI 安装不意味着每个项目都要安装 Node.js、Python、Git 或某个编辑器。
4. 对系统级安装、外部服务、凭据、删除/覆盖等有副作用的动作，先看清对象和影响，再由你明确决定是否继续。Pi 的工具以启动账户权限运行，不保证每条命令都先征得确认；工作目录不是安全沙箱。
5. 检查实际命令、文件改动和测试输出。没有真实验证证据时，不把项目任务说成已完成。

可选练习：[第一个项目](first-project.md)用本地待办清单练习需求、运行、验收和 Git 保存；它不是 Pi CLI 安装条件。

可以把下面的开场要求交给本地 Pi：

```text
请先查看当前项目的说明文件和现有环境，围绕【我的目标】列出完成任务所必需的最小步骤、可能影响和验证方式。先检查并报告，不要安装依赖、修改系统、访问外部服务或改文件；等我确认后再逐项执行。不要读取或输出凭据；遇到系统权限、外部副作用或不可逆动作时先停下说明。完成后给出实际改动和验证结果。
```

## 常见问题

| 现象 | 先区分什么 | 安全的下一步 |
|:---|:---|:---|
| `pi` 命令找不到 | 安装可能完成但当前终端没读到 PATH，或安装未成功 | 重开同一系统的终端，核对安装器结束信息和 PATH；先不要重复运行安装器。 |
| 安装器报告 Node/npm 缺失或版本过低 | 安装前置条件，不是模型登录问题 | 确认 Node.js 至少为 22.19.0 且有 npm；使用官方 Node 来源或安装器的明确选项。 |
| 官方安装源超时或被拒绝 | 访问安装源、包分发、Node 下载或系统包源中的哪一步 | 记录操作系统、执行命令和脱敏报错；只排查实际失败的官方来源，不关闭 TLS 或改用未知脚本。 |
| CLI 能启动但模型不能回答 | CLI 安装与模型授权/可用性是不同阶段 | 在 Pi 内检查 `/login`、`/model` 和提供方账号权限；不要重新安装 CLI，也不要向他人发送凭据。 |
| Windows 上 `pi --version` 成功，但 Pi 报 Bash 不可用 | CLI 与 Bash 工具是不同问题 | 按 Windows 官方说明安装/定位 Git Bash，或检查 `~/.pi/agent/settings.json` 的 `shellPath`；无需因此默认迁移到 WSL。 |
| 网页 AI 让你粘贴密钥或运行来源不明的命令 | 凭据和下载来源风险 | 不提供密钥；回到 Pi 官方页面确认命令。错误信息先脱敏，再提供给 AI。 |

## 官方资料

- [Pi Quickstart：安装与启动](https://pi.dev/docs/latest/quickstart)
- [Pi Windows：原生 Windows、Git Bash 与 WSL](https://pi.dev/docs/latest/windows)
- [Pi Providers：认证与模型提供方](https://pi.dev/docs/latest/providers)
- [Pi Security：工具权限与安全边界](https://pi.dev/docs/latest/security)
- [Pi 官方安装脚本（macOS/Linux）](https://pi.dev/install.sh)
- [Pi 官方安装脚本（Windows PowerShell）](https://pi.dev/install.ps1)
- [Node.js 官方下载页](https://nodejs.org/en/download)
- [Git for Windows 官方下载页](https://git-scm.com/download/win)

<a id="web-ai-walkthrough-prompt"></a>

## 网页 AI 单步引导提示词

复制下面整段到你能使用的网页 AI。网页 AI 不能替你运行或验证本机命令。每次只做一个检查或执行动作，并根据你实际回报继续。

```text
你是我的 Pi CLI 安装和首次使用向导。先核对 Pi 当前官方资料：
- Quickstart：https://pi.dev/docs/latest/quickstart
- Windows：https://pi.dev/docs/latest/windows
- Providers：https://pi.dev/docs/latest/providers
- Security：https://pi.dev/docs/latest/security
- 官方仓库：https://github.com/earendil-works/pi

每次只给我一个检查动作或一条命令，说明在哪个终端运行、目的、可能影响和成功信号，然后停下来等我的实际结果。不要声称你已在我电脑上运行或验证任何内容。

先询问我的操作系统、终端，以及 `pi --version` 是否成功；若我不清楚，只给一个不会修改系统的检查方法。若已安装就不要重复安装。不要预设我必须使用 WSL、Git、Python、编辑器、代理或项目依赖。只用官方安装方式；常规安装/更新和云端模型需要网络，安装源、包源、模型服务要分别核对，不猜白名单或代理。`curl | sh` 或 `irm | iex` 会下载并执行脚本，先让我核对官方域名。

官方安装器与 npm 路线要求 Node.js 22.19.0 或更高版本和 npm。若安装器准备安装 Node、调用系统包管理器、改 PATH/shell 配置、更新/重装现有 Pi 或立即启动，先解释精确动作、范围和影响，等我决定。不要以管理员/root 运行，不用 `sudo npm`。Windows 原生 Git Bash 只用于 Pi 的 Bash 工具，WSL 可选；若选择 Portable Git，说明它会写入 Pi 用户目录并修改 `settings.json` 的 `shellPath`；若还有 winget 全局安装或跳过选项，解释差异后等我选择。只有我已在使用 Nix 时才推荐 Nix。

不要向我索取或复述密码、API Key、Token、cookie、订阅链接、私钥或授权码；我只在本地 Pi 的可信流程里自行处理凭据，并在分享结果前脱敏。CLI 安装、模型 `/login` 与 `/model`、项目任务是不同验收。ChatGPT 订阅不自动代表 OpenAI API 额度。Pi 使用启动账户权限，不是安全沙箱；项目中只配置当前任务必需的工具，涉及系统修改、外部服务或不可逆操作时先停下让我决定。

遇到错误时一次只排查一个问题，先根据操作系统、终端、当前步骤、命令和已脱敏报错诊断；不要盲目重装、提高权限、关闭 TLS/安全软件或使用未知脚本。无法核对官方资料时明确说明，不要编造。

现在只询问操作系统、终端和 `pi --version` 的实际结果，然后停下来等我回复。
```

## 历史链接说明

<a id="使用仓库配置基线"></a>

旧 Codex 配置基线及其安装/恢复脚本已从仓库移除。此历史锚点仅用于旧链接跳转，不提供安装或恢复命令。
