<a id="learning-map"></a>
<a id="1-学习地图"></a>

# Pi CLI 上手指南：从新电脑准备到安装后使用

## 字多不看

- 本文是 Pi CLI 入门的唯一完整指南：先看系统与网络，再安装、验证，最后区分模型授权和安装后使用。
- 联网是常规安装/更新和云端模型使用的必要条件：安装要访问所选官方分发与依赖源；本仓主路线 Pi + OpenAI GPT 还要从当前终端访问 OpenAI 登录及推理服务。只有已安装后的 `pi --version` 或已准备好的本地模型可能离线使用。
- Pi 官方 shell/PowerShell 安装器与 npm 路线要求 Node.js 22.19.0 或更高版本及 npm；官方安装器可协助安装 Node。安装器所选的自动安装路径可能修改用户 PATH，也可能调用系统包管理器。
- macOS/Linux 官方安装器：`curl -fsSL https://pi.dev/install.sh | sh`。Windows PowerShell 官方安装器：`powershell -c "irm https://pi.dev/install.ps1 | iex"`。两条命令都会下载并执行 Pi 官方安装脚本。
- `pi --version` 只证明 CLI 可运行；模型登录另用 Pi 内的 `/login`，之后再用 `/model` 选模型。凭据不发给网页 AI，也不提交到仓库。
- Windows 原生运行时，Git Bash 是 Pi 内置 Bash 工具所需的命令环境，不是安装 CLI 的通用前置条件；WSL 是可选路线。
- Pi 以启动它的操作系统账户权限运行，不是安全沙箱。不要以管理员/root 启动，并检查 AI 要执行的命令与修改。

## 快速导航

| 阶段 | 内容 |
|:---|:---|
| [准备](#准备与系统要求) | 分清 Pi 安装、模型授权和项目环境；核对系统与现有安装 |
| [网络与依赖](#network-and-dependencies) | 安装/更新与在线模型所需网络；具体目标随路线变化 |
| [安装 Pi CLI](#pi-cli-installation) | macOS/Linux、Windows、WSL、npm 与 Nix 的适用路线 |
| [验证与模型连接](#verify-and-connect-a-model) | `pi --version`、`/login`、`/model` 的不同验收 |
| [安装后使用](#post-install-use) | 让 Pi 按任务检查和配置环境，并保持权限边界 |
| [逐步引导提示词](#web-ai-walkthrough-prompt) | 可复制给网页 AI 的单步指导提示词 |
| [可选练习](first-project.md) | 用一个本地项目练习需求、运行、验收和 Git 保存 |

## 使用方式

- 新电脑先按本文准备并安装；已有 Pi 时先运行 `pi --version`，成功就不要重复安装。
- 安装后若要让 Pi 回答，再单独完成模型提供方授权；不需要模型登录即可确认 CLI 是否安装。
- 网页 AI 只能根据你反馈的结果指导，不能替你运行或验证本机命令。每次执行前阅读命令和安装器提示。
- [第一个项目](first-project.md)是可选练习；Git、Python、编辑器和项目依赖按具体任务需要，不是 Pi CLI 安装条件。

## 正文

### 准备与系统要求

先明确三个不同结果：

| 阶段 | 成功判断 | 不代表什么 |
|:---|:---|:---|
| CLI 已安装 | `pi --version` 输出版本号 | 不代表模型已授权或可用 |
| 模型已连接 | Pi 内 `/login` 完成，选定模型后能得到回答 | 不代表开发环境或项目依赖已配置 |
| 项目任务已完成 | 按具体任务完成并检查改动、运行结果和测试 | 不由安装成功自动推出 |

Pi 官方 Quickstart 支持 macOS、Linux，并为 Windows 提供独立说明；Windows 可原生运行，也可在 WSL 内运行。安装前按自己实际使用的终端选择同一环境：不要因为装 Pi 就默认安装 WSL。

| 项目 | 当前要求或选择 | 说明 |
|:---|:---|:---|
| macOS / Linux 安装 | 可运行 `curl` 和 POSIX shell | 使用 Pi 官方 shell 安装器。 |
| Windows 安装 | PowerShell | 使用 Pi 官方 PowerShell 安装器。原生 Windows 与 WSL 是两种独立环境。 |
| Node.js 与 npm | 官方安装器及 npm 路线要求 Node.js 22.19.0 或更高版本和 npm | 官方安装器可能提供 Node 安装选项；不要猜测或安装低于要求的版本。 |
| Windows 原生 Bash | 仅在需要 Pi 的内置 Bash 工具或 `!` 命令时需要 Git Bash | 可用 Git for Windows；官方安装器的版本也可能提供安装到 Pi 用户目录的 Portable Git，并写入 Pi 的 `settings.json`。不是 `pi --version` 的前置条件。 |
| Nix | 已经使用 Nix 的 macOS/Linux 用户可选 | 走官方 Nix 安装/更新路线；不需要为 Pi 专门安装 Nix。 |
| WSL、Git、Python、编辑器 | 按工作环境或具体项目选择 | 均不是安装 Pi CLI 的普遍前置条件。 |
| 网络 | 常规官方安装/更新以及云端模型调用都需要可用网络；本仓主路线需访问 OpenAI 提供方 | 安装源、包源与模型服务是不同目标；已安装后的本地版本检查和已准备好的本地模型可能离线。 |

开始前在普通用户终端检查 Pi 是否已安装：

```bash
pi --version
```

Windows PowerShell 中也运行同一条命令。若成功，跳过安装；若命令不存在，继续。不要以管理员/root 身份运行安装器。

### <a id="network-and-dependencies"></a>网络与依赖准备

联网是常规安装/更新与云端模型使用的必要环境条件，但目标不同：安装需访问 Pi 分发与依赖源；本仓默认的 Pi + OpenAI GPT 在线路线还需访问 OpenAI 认证与推理服务。安装脚本可访问，不等于模型提供方也可访问。

| 阶段 | 需要访问的服务（依安装路线） | 说明 |
|:---|:---|:---|
| 获取安装脚本和 Pi 发布信息 | Pi 官方 `pi.dev` 域名 | 使用下文列出的官方地址；不要从第三方脚本站下载。 |
| 获取 Pi 包及依赖 | npm 官方包分发服务（通常为 `registry.npmjs.org`） | 官方托管安装会安装锁定的依赖。 |
| 自动安装 Node 或系统依赖 | Node.js 官方分发服务，或当前系统选择的包管理器源 | 是否访问取决于系统、已有 Node/npm 和安装器选择；Linux/macOS 的系统包安装可能要求你在本机确认权限。 |
| Windows 可选安装 Git Bash | 选择 Portable Git 时可能访问 `api.github.com` 和 GitHub 发布资产；若明确选择 winget，则使用其配置的包源 | 只有选择安装 Git Bash 时才涉及；这不是 Pi CLI 安装本身的网络要求。具体下载地址以官方安装器当前输出为准。 |
| 已有 Nix 用户的可选路线 | GitHub 与本机 Nix 配置的缓存/包源 | 只有选择 Nix 路线时涉及。 |
| 登录和模型请求 | 用户选择的模型提供方及其认证服务 | 域名、账号权限、订阅/API 费用因提供方和登录方式而异。 |
| 网页 AI 协助 | 你所使用的网页 AI 服务 | 网页 AI 只读你提交的内容，不会自动看到本机终端。 |

可先在浏览器打开对应的 Pi 官方文档；这只能证明浏览器可访问，不能保证当前终端、包源或模型服务也可访问。安装命令和登录流程会分别给出实际网络结果。

Pi 官方资料没有给出覆盖所有平台、安装选项和模型提供方的固定网络白名单。公司/学校网络若拦截请求，应根据安装器报错和当前官方说明确认具体目标，并遵守网络管理员要求；不要默认购买代理、启用全局代理/TUN、关闭 TLS/安全软件或换用来历不明的镜像。不要把代理口令或含凭据的日志发给 AI。

### <a id="pi-cli-installation"></a>安装 Pi CLI

执行前确认地址来自 [Pi 官方 Quickstart](https://pi.dev/docs/latest/quickstart)、[Windows 说明](https://pi.dev/docs/latest/windows)或[官方仓库 README](https://github.com/earendil-works/pi)。下面的 `curl | sh` 和 `irm | iex` 会把下载的脚本直接交给 shell 执行；先看清域名、终端和安装器接下来的提示。使用交互式终端，不要用 `sudo` 或“以管理员身份运行”包装安装命令。

#### macOS / Linux

打开 Terminal，在普通用户 shell 中运行：

```bash
curl -fsSL https://pi.dev/install.sh | sh
```

官方安装器会安装并管理 Pi 的依赖，后续可用 `pi update` 更新。当前安装器要求 Node.js 22.19.0 或更高版本和 npm；如果缺少依赖，它会先说明拟采用的安装路线并询问是否继续。自动方案视系统而定：可能把 Node 放在用户目录、提示把 Pi/Node 的目录加入 shell 配置，也可能通过 Homebrew、apt 或 apk 等系统包管理器安装/更新依赖，后者可能请求 sudo。读清具体提示；不接受系统级修改时取消安装器，改用 Node.js 官方分发安装满足版本要求的 Node 和 npm，再重试。安装器也可能询问是否立即启动 Pi；可先选择暂不启动，完成 `pi --version` 验证后再手动打开。启动 CLI 不等于模型已登录。不要把安装器命令改成 `sudo curl ... | sh`。

#### Windows 原生 PowerShell

在普通用户 PowerShell 中运行：

```powershell
powershell -c "irm https://pi.dev/install.ps1 | iex"
```

PowerShell 安装器同样要求 Node.js 22.19.0 或更高版本和 npm；在缺少依赖时可能提出安装 Node 的选项，并把用户级安装位置加入 PATH。安装器显示更新、重装、卸载或迁移已有安装时，先确认现有版本和目标路径，不要盲目接受默认选项；若询问是否立即启动 Pi，可先选择暂不启动，完成 `pi --version` 验证后再手动打开。

若安装器询问 Git Bash：它只关系到 Pi 在 Windows 原生环境中运行 Bash 工具，不影响 `pi --version`。可选择安装在 Pi 用户目录中的 Portable Git；该选项会在 Pi 用户目录写入 Git Bash，并调整 `~/.pi/agent/settings.json` 中的 `shellPath`。也可稍后按[官方 Windows 说明](https://pi.dev/docs/latest/windows)安装 Git for Windows；如提供 winget 等全局安装选项，只有明确希望这样安装时才选。拒绝 Git Bash 不会阻止 CLI 安装，但 Pi 的 Bash 工具之后可能不可用。WSL 不是必选替代方案。

#### WSL（可选）

如果你本来就在 WSL 中开发，在目标发行版的 Linux shell 内按 macOS/Linux 路线安装，并在该发行版内运行 Pi。Windows 原生与 WSL 的安装目录、PATH 和工具环境相互独立；不要在两个终端之间混用安装结果。

#### 其他官方路线

- 已经使用 Nix 的 macOS/Linux 用户可按 [Pi Quickstart 的 Nix 说明](https://pi.dev/docs/latest/quickstart)安装。Nix 会按 Nix 路线更新，`pi update` 不负责更新 Nix 安装。
- 已有合格 Node.js 和 npm 的用户可使用官方 npm 备选命令：

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

官方说明指出 npm 安装不会锁定传递依赖，故新手通常优先使用平台安装器。全局 npm 权限报错时不要用 `sudo npm` 硬修；先停止并选择官方安装器或用户级 Node 环境。

### <a id="verify-and-connect-a-model"></a>验证安装并连接模型

在安装所用的同一个终端运行：

```bash
pi --version
```

出现版本号说明 CLI 已安装。若当前终端提示找不到命令，先关闭并重新打开终端，再核对安装器报告的 PATH 和安装位置；不要立刻重复安装。

需要 Pi 生成回答时，在终端启动 `pi`，然后在 Pi 界面内运行：

```text
/login
```

本仓主体路线是 Pi 加经用户授权的 OpenAI GPT；按这一路线时，选择你有权使用且当前可用的 OpenAI 认证方式。也可以按需要选择其他受支持的模型提供方。随后在 Pi 内用 `/model` 选择可用模型，并发送一条不要求修改文件的简单问题。Pi 支持订阅、API Key 或本地模型等不同提供方路线，前提、权限与费用不同。ChatGPT 订阅不应被自动当成 OpenAI API 额度。

若用 API Key，优先选择受信凭据管理器和 Pi 官方支持的安全读取方式；若通过 Pi 的 `/login` 交互录入，凭据可能保存在 `~/.pi/agent/auth.json`。该文件可能含 API Key 或 OAuth Token，必须保持私密，不得提交、上传或复制给网页 AI。不要把密钥、密码、Token、cookie、订阅链接或带凭据的截图贴进对话，也不要把凭据写进项目文件、脚本或 shell 配置。若选择本地模型，还需按提供方另行配置本地运行时与模型资源；这不是 Pi CLI 安装的一部分。

### <a id="post-install-use"></a>安装后的使用

1. 进入你有权让 Pi 访问的项目目录，再运行 `pi`。在本仓库中工作时，可从仓库根目录运行 `pi --skill .github/skills`，显式加载仓库 Skills；这不会把 `.github/extensions/` 整体作为 Pi 原生扩展加载。详见[根 README](../../../README.md)。不要以管理员/root 身份启动。
2. 用自然语言说明目标、当前状态、限制和验收标准。可以先要求 Pi 只检查现有环境和项目文件，给出所需工具、计划、风险与验证方式，暂不安装或修改。
3. 只配置当前任务确实需要的 Git、语言运行时、编辑器或项目依赖；Pi CLI 安装不意味着所有项目都要安装 Node.js、Python、Git 或某个编辑器。
4. 对系统级安装、外部服务、凭据、删除/覆盖等有副作用的动作，先看清对象和影响，再由你明确决定是否继续。Pi 的工具以启动账户权限运行，不保证每条命令都先征得确认；工作目录不是安全沙箱。
5. 检查实际命令、文件改动和测试输出。没有真实验证证据时，不把项目任务说成已完成。

可以把这段作为在本地 Pi 中开始某个任务时的开场要求：

```text
请先查看当前项目的说明文件和现有环境，围绕【我的目标】列出完成任务所必需的最小步骤、可能影响和验证方式。先检查并报告，不要安装依赖、修改系统、访问外部服务或改文件；等我确认后再逐项执行。不要读取或输出凭据；遇到系统权限、外部副作用或不可逆动作时先停下说明。完成后给出实际改动和验证结果。
```

旧 Codex 配置基线及其安装/恢复脚本已从仓库移除。保留历史链接锚点仅用于说明退役状态，不提供安装或恢复命令。

<a id="使用仓库配置基线"></a>

### 常见问题

| 现象 | 先区分什么 | 安全的下一步 |
|:---|:---|:---|
| `pi` 命令找不到 | 安装可能完成但当前终端没读到 PATH，或安装未成功 | 重开同一系统的终端，核对安装器结束信息和 PATH；先不要重复运行安装器。 |
| 安装器报告 Node/npm 缺失或版本过低 | 安装前置条件，不是模型登录问题 | 确认 Node.js 至少为 22.19.0 且有 npm；使用官方 Node 来源或安装器的明确选项。 |
| 官方安装源超时或被拒绝 | 访问安装源、包分发、Node 下载或系统包源中的哪一步 | 记录操作系统、执行的命令和脱敏报错；只排查实际失败的官方来源，不关闭 TLS 或改用未知脚本。 |
| Windows 上 `pi --version` 成功，但 Pi 报 Bash 不可用 | CLI 与 Bash 工具是不同问题 | 按 Windows 官方说明安装/定位 Git Bash，或检查 `~/.pi/agent/settings.json` 的 `shellPath`；无需因此默认迁移到 WSL。 |
| Pi 能启动但不能回答 | CLI 安装与模型授权/模型可用性是不同阶段 | 在 Pi 内检查 `/login`、`/model` 和提供方账号权限；不要重新安装 CLI，也不要向他人发送凭据。 |
| 网页 AI 让你粘贴密钥或运行来源不明的命令 | 凭据和下载来源风险 | 不提供密钥；回到 Pi 官方页面确认命令。错误信息先脱敏，再提供给 AI。 |

### 官方资料

- [Pi Quickstart：安装与启动](https://pi.dev/docs/latest/quickstart)
- [Pi Windows：原生 Windows、Git Bash 与 WSL](https://pi.dev/docs/latest/windows)
- [Pi Providers：认证与模型提供方](https://pi.dev/docs/latest/providers)
- [Pi Security：工具权限与安全边界](https://pi.dev/docs/latest/security)
- [Pi 官方安装脚本（macOS/Linux）](https://pi.dev/install.sh)
- [Pi 官方安装脚本（Windows PowerShell）](https://pi.dev/install.ps1)
- [Node.js 官方下载页](https://nodejs.org/en/download)
- [Git for Windows 官方下载页](https://git-scm.com/download/win)

### <a id="web-ai-walkthrough-prompt"></a>网页 AI 单步引导提示词

复制下面整段到你能使用的网页 AI。它会按你的系统逐步指导；命令仍由你在自己的电脑执行，网页 AI 不能替你运行或验证。

```text
你是我的 Pi CLI 安装和首次使用向导。请先查看并遵循 Pi 当前官方资料：
- Quickstart：https://pi.dev/docs/latest/quickstart
- Windows：https://pi.dev/docs/latest/windows
- Providers：https://pi.dev/docs/latest/providers
- Security：https://pi.dev/docs/latest/security
- 官方仓库：https://github.com/earendil-works/pi

请按以下规则逐步协助我，从确认电脑现状开始，直到 Pi CLI 安装完成；如果我愿意，再继续模型登录和第一次使用。每次只给我一个检查动作或一条命令，说明在哪个终端运行、目的、可能影响和成功信号，然后停下来等我的实际结果。不要一次列出后续命令，不要声称你已在我电脑上运行或验证任何内容。

1. 先问我使用的操作系统和终端；若不清楚，只给一个不会修改系统的检查方法。不要预设我必须用 WSL、管理员账户、Git、Python、编辑器、代理或项目依赖。
2. 先检查 `pi --version`。若已有版本号，跳过安装，不要重复安装；如果安装器识别到旧版本或提出更新、重装、卸载、迁移，先停下来让我核对现有安装和目标路径。安装器若询问是否立即启动 Pi，说明这只会打开 CLI，并建议先完成版本验证。
3. 只采用 Pi 官方当前安装方式。macOS/Linux 使用官方 shell 安装器；Windows 使用官方 PowerShell 安装器；只有我已在使用 Nix 时才推荐 Nix。先说明 `curl | sh` 或 `irm | iex` 会下载并执行脚本，并让我核对官方域名。
4. Pi 官方 shell/PowerShell 安装器与 npm 路线要求 Node.js 22.19.0 或更高版本和 npm。先检查现状；若安装器提出安装 Node、调用 apt/apk/Homebrew/winget、写入用户 PATH 或修改 shell 配置，解释精确动作、影响范围和是否需要管理员权限，等我选择后再继续。不要运行 `sudo npm`，不要以管理员/root 身份运行 Pi 安装器。
5. Windows 原生环境中，Git Bash 只关系到 Pi 的内置 Bash 工具，不是 CLI 安装本身的前置条件。若安装器提供用户目录内的 Portable Git（会修改 Pi 的 `settings.json`）、winget 全局安装或跳过选项，解释差异并等我选择；不要默认安装全局工具。WSL 只是可选环境。
6. 常规安装/更新和云端模型调用需要相应网络；安装源、包源与模型服务要分别核对。不猜固定网络白名单、镜像或代理设置。若网络失败，先判断失败在哪个官方来源或提供方；不建议购买代理、启用全局 TUN、关闭 TLS/安全软件或运行未知脚本。遵守我的组织网络政策。
7. 不向我索取、接收或复述密码、API Key、Token、cookie、订阅链接、私钥或授权码。我只会在 Pi 本机界面或可信凭据流程中自行处理凭据，不会贴给你。提示我在分享输出前脱敏。
8. CLI 安装后让我在同一终端运行 `pi --version`，只根据我实际反馈确认安装结果。之后再问我是否要连接模型；如继续，让我在本地 Pi 界面按 `/login` 操作，并用 `/model` 选择模型。说明订阅/API 权限和费用由提供方决定，`auth.json` 含敏感凭据，不可分享或提交。
9. 模型能回答后，如我有具体项目任务，先让我在目标项目目录启动 Pi。先检查现有项目和环境，只提出该任务必需的工具；涉及系统级安装、外部服务、改文件或不可逆操作时，先说明并等我决定。Pi 使用启动账户权限，不是安全沙箱；提醒我审阅命令和改动。
10. 遇到错误时，一次只排查一个最小问题。请先索取操作系统、终端、当前步骤、命令和已脱敏的完整报错；不要让我盲目重装、提高权限或关闭安全设置。若你无法访问官方资料，请明确说无法核对，不要编造。

现在只问我确认操作系统、终端，以及 `pi --version` 是否已经成功。不要先给安装命令。
```
