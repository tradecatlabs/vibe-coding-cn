<!-- generated: sync-faqi-catalog.py -->
# Vibe Coding法器重要性总表

## 字多不看

目录登记30个对象的Vibe Coding重要性；部分软件工件已退役但保留历史重要性记录，不表示当前可运行。各对象使用v1的18项说明表；Vibe Coding 重要性暂定不代表效能验证。
原始登记、来源及历史见[data.json](data.json)；来源初审与当前迁移位置分开，视图不产生运行、许可或效果批准。

## 快速导航

- [天阶（4项）](tian.md)
- [地阶（12项）](di.md)
- [玄阶（9项）](xuan.md)
- [黄阶（5项）](huang.md)
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

按重要性阶打开对应文档；原始数据只在data.json维护，运行make sync-faqi-catalog更新README.md及四阶文档。

## 正文

## 法器总表

### 天阶

<a id="v0-faqi-dep-category-cloud-model-api-1a52191c"></a>
- [2.2 云端模型服务/API与固定模型版本](tian.md#v0-faqi-dep-category-cloud-model-api-1a52191c)
<a id="v0-faqi-dep-pi-cli-7a8190bb"></a>
- [Pi Agent CLI（当前 PATH 实例）](tian.md#v0-faqi-dep-pi-cli-7a8190bb)
<a id="v0-faqi-dep-category-local-model-stack-7430e743"></a>
- [2.2 本地模型权重、Tokenizer与推理引擎](tian.md#v0-faqi-dep-category-local-model-stack-7430e743)
<a id="v0-faqi-dep-codex-cli-89544cbf"></a>
- [Codex CLI（依赖图替代项）](tian.md#v0-faqi-dep-codex-cli-89544cbf)

### 地阶

<a id="v0-faqi-dep-bash-9e17a7e4"></a>
- [GNU Bash](di.md#v0-faqi-dep-bash-9e17a7e4)
<a id="v0-faqi-dep-category-terminal-pty-3d912d9d"></a>
- [3.2 Terminal Emulator / PTY](di.md#v0-faqi-dep-category-terminal-pty-3d912d9d)
<a id="v0-faqi-dep-git-client-817eaef2"></a>
- [Git 本地客户端](di.md#v0-faqi-dep-git-client-817eaef2)
<a id="v0-faqi-dep-category-infrastructure-92099635"></a>
- [8 CPU/GPU、内存、存储、网络、电力与数据中心](di.md#v0-faqi-dep-category-infrastructure-92099635)
<a id="v0-faqi-dep-category-package-sources-de4ecd15"></a>
- [4.2 包注册表、Git源与可信缓存](di.md#v0-faqi-dep-category-package-sources-de4ecd15)
<a id="v0-faqi-dep-nodejs-runtime-154fe616"></a>
- [Node.js 运行时](di.md#v0-faqi-dep-nodejs-runtime-154fe616)
<a id="v0-faqi-dep-npm-npx-99c5e69b"></a>
- [npm / npx 工具](di.md#v0-faqi-dep-npm-npx-99c5e69b)
<a id="v0-faqi-dep-python-runtime-c49ee719"></a>
- [Python 运行时](di.md#v0-faqi-dep-python-runtime-c49ee719)
<a id="v0-faqi-dep-gnu-make-a64dde37"></a>
- [GNU Make](di.md#v0-faqi-dep-gnu-make-a64dde37)
<a id="v0-faqi-dep-ubuntu-userland-27a7ecd2"></a>
- [Ubuntu 用户空间发行版](di.md#v0-faqi-dep-ubuntu-userland-27a7ecd2)
<a id="v0-faqi-dep-wsl2-kernel-dc978cb1"></a>
- [WSL2 Linux 内核](di.md#v0-faqi-dep-wsl2-kernel-dc978cb1)
<a id="v0-faqi-dep-wsl2-platform-116a484c"></a>
- [WSL 2 承载平台](di.md#v0-faqi-dep-wsl2-platform-116a484c)

### 玄阶

<a id="v0-faqi-dep-category-ci-platform-e3564493"></a>
- [7.1 Git托管、CI Runner与CI/CD平台](xuan.md#v0-faqi-dep-category-ci-platform-e3564493)
<a id="v0-faqi-dep-category-retrieval-memory-da201109"></a>
- [2.3 检索/索引/记忆与向量库](xuan.md#v0-faqi-dep-category-retrieval-memory-da201109)
<a id="v0-faqi-dep-category-deployment-data-35c30956"></a>
- [7.2-7.3 制品注册表、部署目标、产品运行时、数据库与外部API](xuan.md#v0-faqi-dep-category-deployment-data-35c30956)
<a id="v0-faqi-faqi-auto-skill-create-ffe7ec4d"></a>
- [auto-skill模板生成脚本](xuan.md#v0-faqi-faqi-auto-skill-create-ffe7ec4d)
<a id="v0-faqi-faqi-auto-skill-validate-5244b18f"></a>
- [auto-skill结构校验脚本](xuan.md#v0-faqi-faqi-auto-skill-validate-5244b18f)
<a id="v0-faqi-faqi-skill-seekers-cc1f7ed8"></a>
- [Skill Seekers程序](xuan.md#v0-faqi-faqi-skill-seekers-cc1f7ed8)
<a id="v0-faqi-faqi-claude-skill-init-3a642a5d"></a>
- [官方Skill初始化脚本](xuan.md#v0-faqi-faqi-claude-skill-init-3a642a5d)
<a id="v0-faqi-faqi-codex-config-installer-2dcddf43"></a>
- [Codex配置安装与恢复脚本](xuan.md#v0-faqi-faqi-codex-config-installer-2dcddf43)
<a id="v0-faqi-faqi-skill-seekers-adapter-eb5e7e6f"></a>
- [Skill Seekers本地运行适配脚本](xuan.md#v0-faqi-faqi-skill-seekers-adapter-eb5e7e6f)

### 黄阶

<a id="v0-faqi-dep-tmux-runtime-8bd62e08"></a>
- [tmux 当前运行实例](huang.md#v0-faqi-dep-tmux-runtime-8bd62e08)
<a id="v0-faqi-faqi-auto-tmux-09bb1add"></a>
- [auto-tmux命令封装程序](huang.md#v0-faqi-faqi-auto-tmux-09bb1add)
<a id="v0-faqi-faqi-tmux-fbe1a81c"></a>
- [tmux终端复用程序](huang.md#v0-faqi-faqi-tmux-fbe1a81c)
<a id="v0-faqi-faqi-oh-my-tmux-3ab56947"></a>
- [oh-my-tmux可执行配置程序](huang.md#v0-faqi-faqi-oh-my-tmux-3ab56947)
<a id="v0-faqi-faqi-prompt-converter-43a9d077"></a>
- [提示词格式转换程序](huang.md#v0-faqi-faqi-prompt-converter-43a9d077)

## 原始说明

冻结说明原文、字节摘要和选择器保存在唯一资料源[data.json](data.json)的`documents`中；本页只保留历史入口，不重复展开原文。

### 原始文档

<a id="doc-faqi-system"></a>
- `.github/docs/gongfa/faqi-system.md`：原始字节与摘要见[data.json](data.json)

<!-- 兼容已发布阅读视图中的章节锚点 -->
<a id="doc-faqi-system-vibe-coding-法器体系说明"></a>
<a id="doc-faqi-system-一句话"></a>
<a id="doc-faqi-system-字多不看"></a>
<a id="doc-faqi-system-对象边界"></a>
<a id="doc-faqi-system-重要性分级"></a>
<a id="doc-faqi-system-重要性与效能评级"></a>
<a id="doc-faqi-system-选用流程"></a>
<a id="doc-faqi-system-skill-seekers-mcp-static-review"></a>
<a id="doc-faqi-system-固定源码复核skill-seekers-mcp"></a>
<a id="doc-faqi-system-登记与维护"></a>
