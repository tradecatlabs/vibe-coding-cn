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

`ISSUE_TEMPLATE/`、`CODEOWNERS`、`FUNDING.yml`、`PULL_REQUEST_TEMPLATE.md`、`SECURITY.md`、`WIKI.md`、`labeler.yml`、`lint_config.json`保留现有位置；用户本次点名workflows，不扩改其他协作入口。

- `workflows/`已退役，不再作为平台例外；禁止重建目录、符号链接或兼容壳。原3个定义以`github-actions-*.yml`在Extensions平铺，说明见`extensions/github-actions.md`。
- 自动CI、Labeler和Welcome不再触发；本地命令仍由根Makefile调用Extensions中的脚本，不把空远端检查当CI成功。
- CODEOWNERS仍由`@tukuaiai`、`@tradecatlabs`覆盖，仅迁移路径，不改变审批或豁免资格。
- 原自动化定义逐字节保全，不执行或读取其secret表达式；恢复自动化须显式授权，不能只搬回路径而忽略权限、输入及检查生产者。
- 审批Ruleset25244224的`tradecatlabs`豁免只用于其自己的PR；其他PR仍须有效批准。仅退役两套保护中已停用的`markdown-lint`/`link-checker`；签名、PR、线性历史及其它保护不变，不伪造审核。
- Issue/PR模板保持协作职责，长期规则写根AGENTS或资源域AGENTS，不塞入模板与CI。
- 固定来源使用Extensions下四个Gitlink；不得提交缓存、私有模板、真实会话、数据库或凭据。

## 验证

从仓库根运行相关`make lint`、`make check-links`、`make check-directory-docs`及受影响协议检查，最终完整测试以根AGENTS为准。
