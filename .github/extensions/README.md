# Extensions：既有程序与小工具

## 字多不看

这里统一放原有程序、脚本、检查器及适配代码；每个既有程序或独立脚本在本域平铺，程序内部源码结构不拆散。
这里的Extensions不是Pi原生扩展的同义词；不能把整个目录交给Pi的`-e`加载。

## 快速导航

| 既有对象 | 入口与用途 |
|---|---|
| [Skill Seekers](Skill_Seekers-development/README.md) | 固定上游源码；原本地适配脚本已退役，按上游说明与具体授权选择使用 |
| [Claude官方Skills源](claude-official-skills/README.md) | 保留单一固定源码及独立初始化脚本；Skills域的16个官方入口已移除 |
| [tmux](tmux/README)、[oh-my-tmux](oh-my-tmux/README.md) | 原固定源码与配置仓库；不是自动安装或启用 |
| [提示词转换](prompts-library/README.md) | 原Excel、Markdown、JSONL转换程序 |
| [Codex配置](codex-config/README.md) | 原配置与安装/恢复脚本；使用前核对副作用与凭据边界 |
| [chat-vault](chat-vault/README.md) | 原聊天保存程序；不得随仓保存真实会话和数据库 |
| [my-nvim](my-nvim/README.md)、[MCPlayerTransfer](MCPlayerTransfer/README.md)、[图片转PDF](XHS-image-to-PDF-conversion/README.md) | 保留原程序；文件归类不解除法器原有范围排除 |
| [HTML工具原说明](html-tools-main.md) | `clean_epub_css.html`、`markdown-bianjiqi.html`、`task card generator.html`、`xhs graphic production - 1.0.html`、`xhs graphic production.html` |
| [原GitHub Actions定义](github-actions.md) | `github-actions-ci.yml`、`github-actions-labeler.yml`、`github-actions-welcome.yml`；已停用，仅保全原定义 |

来自两个自有Skill的33个封装脚本已退役，不保留兼容壳；两个Skill改用原生工具与指令检查。
引用原上游的`init_skill.py`独立入口继续保留；固定上游、公共检查/生成/测试脚本及共享库不在本批删除范围。

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

- [使用方式](#使用方式)
- [正文](#正文)
- [检查与维护入口](#检查与维护入口)
- [依赖与执行边界](#依赖与执行边界)

</details>

## 使用方式

先读具体程序的README和来源，再按任务显式调用。Python脚本从仓库根运行；现有Shell脚本可用`bash .github/extensions/<脚本名>`调用。
程序只存一份；Skill中的指令引用这里，不复制执行实现。Pi Agent使用原生工具和模型选择，不新增运行器或模型HTTP客户端。

## 正文

### 检查与维护入口

| 范围 | 既有脚本与入口 |
|---|---|
| Markdown | `check-local-links.py`、`check-markdown-details.py`、`test-markdown-details.py`；`make lint/check-links/check-details/test-details` |
| 结构与索引 | `check-doc-structure.py`、`check-directory-docs.py`、`check-metadata.py`、`sync-doc-toc.py` |
| 功法 | `check-gongfa.py`、`sync-gongfa-catalog.py`、`test-gongfa.py`、`test-gongfa-catalog.py` |
| 法器 | `sync-faqi-catalog.py`、`test-faqi-catalog.py` |
| 引用与资源 | `check-ai-citation.py`、`check-external-resources.py` |
| 研究与来源 | `check-research-raw.py`、`check-source-facts.py`、`fetch-research-raw.py` |
| Wiki | `check-wiki.py`；`make check-wiki WIKI_DIR=<本地checkout>` |
| 迁移数据契约 | `test-source-archive.py`；`lib/source_archive.py`读取原始载荷，`lib/book_views.py`生成阅读导航 |

迁移新增的资料读取与测试是上述既有总表的必要维护支撑，不是新业务工具。
共享库职责见[lib](lib/README.md)。完整本地检查为`make test`；它不执行被审第三方程序，也不证明运行、效果或许可。

### 依赖与执行边界

检查器使用Python3；功法、法器和资料档案维护使用Python3.10+，依赖分别见[requirements-gongfa.txt](requirements-gongfa.txt)、[requirements-faqi.txt](requirements-faqi.txt)。
复用jsonschema、PyYAML、tabulate、markdown-it-py；转换程序另用其原有requirements。Markdown lint使用Node22+及固定的markdownlint-cli0.48.0。

来源树保持原Git修订。安装、抓取、上传、发布、修改配置和终端注入均有独立副作用，不因移入本域得到授权。
凭据仅从受信来源在运行时注入，不提交真实会话、数据库、API密钥、环境文件或私有模板。
