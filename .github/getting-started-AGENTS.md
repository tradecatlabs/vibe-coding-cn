# 入门文件组维护指南

## 职责

入门文件平铺在`.github/`根；原名不冲突的文件保留原名，README和AGENTS指南因重名分别命名为`getting-started-README.md`与`getting-started-AGENTS.md`。本组提供给网页版 AI 使用的 Pi CLI 安装配置提示词，以及一个独立的可选项目练习。

## 文件地图

| 文件 | 职责 |
|---|---|
| `getting-started-README.md` | 入门索引 |
| `god.md` | 《道成了肉身》：以经文题名组织、可全文复制给网页版 AI 的 Pi CLI 安装配置提示词 |
| `first-project.md` | 可选的本地项目闭环练习 |
| `getting-started-AGENTS.md` | 本组维护规则 |

## 修改规则

- 根`README.md`是唯一主页；`getting-started-README.md`只做导航，不复制完整教程。
- `god.md` 本身就是给网页版 AI 的完整提示词：指导用户从现状检查到 CLI 安装、模型配置和安全的本机工具验证；用户复制全文后由 AI 一轮一步引导，并在 Agent 能力验收后停止。不另维护重复的提示词区块或项目开发步骤。
- `god.md` 的叙事题名与经文引文仅用已核验的《圣经》和合本简体（CUVS）原句，注明书卷、章节、版本与原页；连续节录须注明，不拼接或改写经文。保留原语境，技术对应另作说明，不以引用或比喻增加执行授权、权限或效果承诺。标题变化保留必要旧锚点，并同步读者入口。
- 安装方式、Node.js 版本要求、系统支持和 provider 流程以 Pi 当前官方文档与安装入口为准；链接及命令须明确系统、终端、影响和成功判断。官方资料未说明的内容标为未知，不猜测。
- 区分 `pi --version`、模型授权/可用和项目任务完成；不把 CLI 安装说成模型已接通或项目环境已就绪。
- 不把 WSL、Git、Python、编辑器、代理或项目依赖设为 Pi CLI 安装的通用前置条件。Windows 原生 Git Bash 是内置 Bash 工具的命令环境，不是 CLI 安装本身的要求。
- 联网是常规 Pi 安装/更新和云端模型路线的必要条件；仅在官方分发/依赖源或所选模型服务确实不可达时才处理网络配置。不默认推荐购买代理、全局代理/TUN、关闭安全机制或使用非官方源。
- 不要求用户把密码、API Key、Token、cookie、订阅链接或私钥贴给网页 AI。Pi 以启动账户权限运行，不是安全沙箱；提醒用户不要用管理员/root 启动并审阅实际命令与改动。
- 第一个项目保持可选且独立；只同步其真实前置条件和指向提示词的链接，不在练习中复制 Pi 安装说明。
- 入口变化时同步`.github/context/README.md`、根`README.md`、`llms.txt`、`.github/llms-full.txt`和`.github/taxonomy.yml`；删除或迁移入口时核对`.github/redirects.yml`与活动链接。
- 修改后运行 `make sync-doc-toc` 和 `make test`；本地文档检查不证明用户机器安装成功、认证有效或模型效果。
