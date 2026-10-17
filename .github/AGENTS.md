# `.github/`目录规则

根`README.md`是唯一主页，本目录禁止新增`README.md`。

## 三个资源域

| 目录 | 职责 | 入口 |
|---|---|---|
| `context/` | 既有资料、规则、文档、研究及数据 | `context/README.md`、`context/AGENTS.md` |
| `skills/` | 所有既有Skill指令和流程，统一治理 | `skills/README.md`、`skills/AGENTS.md` |
| `extensions/` | 既有小工具、程序、脚本和适配实现 | `extensions/README.md`、`extensions/AGENTS.md` |

对象在各域平铺；资料集合和原生程序内部结构不拆散。旧docs/assets/metadata/prompts/research/scripts/tools不再作为并行活动根目录。

## 平台入口

`workflows/`、`ISSUE_TEMPLATE/`、`CODEOWNERS`、`FUNDING.yml`、`PULL_REQUEST_TEMPLATE.md`、`SECURITY.md`、`WIKI.md`、`labeler.yml`、`lint_config.json`保留GitHub原生位置，不算第四种资源。

- 工作流只做本次必要路径同步，不改变触发、权限、原检查范围或分支保护；本地命令仍由根Makefile调用Extensions中的脚本。
- CODEOWNERS仍由`@tukuaiai`、`@tradecatlabs`覆盖，仅迁移路径，不改变审批或豁免资格。
- 原欢迎Action仍使用`actions/first-interaction@v3`的`repo_token`、`issue_message`、`pr_message`，保留原平台secret、事件、权限及不checkout外部PR边界。
- 审批Ruleset25244224的`tradecatlabs`豁免只用于其自己的PR；其他PR仍须有效批准。主Ruleset17185792及必需CI/签名保持不变，不伪造独立审核。
- Issue/PR模板保持协作职责，长期规则写根AGENTS或资源域AGENTS，不塞入模板与CI。
- 固定来源使用Extensions下四个Gitlink；不得提交缓存、私有模板、真实会话、数据库或凭据。

## 验证

从仓库根运行相关`make lint`、`make check-links`、`make check-directory-docs`及受影响协议检查，最终完整测试以根AGENTS为准。
