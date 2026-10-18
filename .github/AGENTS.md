# `.github/`目录规则

根`README.md`是唯一主页，本目录禁止新增`README.md`。

## 三个资源域

| 目录 | 职责 | 入口 |
|---|---|---|
| `context/` | 既有资料、规则、文档、研究及数据 | `context/README.md`、`context/AGENTS.md` |
| `skills/` | 所有既有Skill指令和流程，统一治理 | `skills/README.md`、`skills/AGENTS.md` |
| `extensions/` | 既有小工具、程序、脚本和适配实现 | `extensions/README.md`、`extensions/AGENTS.md` |

对象在各域平铺；资料集合和原生程序内部结构不拆散。旧docs/assets/metadata/prompts/research/scripts/tools不再作为并行活动根目录。

## 维护脚本与共享库

校验和测试是仓库维护基础设施，不属于用户侧Extensions资源；本次直接平铺到`.github/`，不另建scripts目录或旧路径兼容壳。

| 类别 | 当前入口 |
|---|---|
| Markdown校验 | `check-local-links.py`、`check-markdown-details.py`、`check-doc-structure.py` |
| 目录与导航 | `check-directory-docs.py`、`check-metadata.py`、`check-ai-citation.py` |
| 数据与来源 | `check-gongfa.py`、`check-external-resources.py`、`check-research-raw.py`、`check-source-facts.py` |
| Wiki | `check-wiki.py`；仍只校验明确给定的本地checkout |
| 测试 | `test-gongfa.py`、`test-gongfa-catalog.py`、`test-faqi-catalog.py`、`test-markdown-details.py`、`test-source-archive.py` |
| 共享实现 | `lib/`；供同级入口与原资料生成器共同使用，不重复复制 |
| 依赖 | `requirements-gongfa.txt`、`requirements-faqi.txt` |

3个sync与1个fetch入口仍在Extensions，本次没有迁移它们。保持原校验范围和断言，同步Makefile、真实ROOT、导入与隔离夹具；从其他cwd调用不能误判仓库根。
归档Actions定义保持历史字节，不能当作仍有效的新路径调用；迁移Python脚本不恢复自动CI。

## 平台入口

`ISSUE_TEMPLATE/`、`CODEOWNERS`、`FUNDING.yml`、`PULL_REQUEST_TEMPLATE.md`、`SECURITY.md`、`WIKI.md`、`labeler.yml`、`lint_config.json`保留现有位置；用户本次点名workflows，不扩改其他协作入口。

- `workflows/`已退役，不再作为平台例外；禁止重建目录、符号链接或兼容壳。原3个定义以`github-actions-*.yml`在Extensions平铺，说明见`extensions/github-actions.md`。
- 自动CI、Labeler和Welcome不再触发；本地校验/测试由根Makefile调用同级维护脚本，资料维护仍调用Extensions入口，不把空远端检查当CI成功。
- CODEOWNERS仍由`@tukuaiai`、`@tradecatlabs`覆盖，仅迁移路径，不改变审批或豁免资格。
- 原自动化定义逐字节保全，不执行或读取其secret表达式；恢复自动化须显式授权，不能只搬回路径而忽略权限、输入及检查生产者。
- 审批Ruleset25244224的`tradecatlabs`豁免只用于其自己的PR；其他PR仍须有效批准。仅退役两套保护中已停用的`markdown-lint`/`link-checker`；签名、PR、线性历史及其它保护不变，不伪造审核。
- Issue/PR模板保持协作职责，长期规则写根AGENTS或资源域AGENTS，不塞入模板与CI。
- 固定来源使用Extensions下四个Gitlink；不得提交缓存、私有模板、真实会话、数据库或凭据。

## 验证

从仓库根运行相关`make lint`、`make check-links`、`make check-directory-docs`及受影响协议检查，最终完整测试以根AGENTS为准。
