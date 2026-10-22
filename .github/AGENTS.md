# `.github/`目录规则

根`README.md`是唯一主页，本目录禁止新增`README.md`。原首页贡献者名单与鸣谢集中保存在`.github/CONTRIBUTORS.md`，不在根README重复维护。

## 三个资源域

| 目录 | 职责 | 入口 |
|---|---|---|
| `context/`及同级平铺的Context资料、`tool-explanation-template-v*.md` | 公开资料、规则、文档及数据；研究档案仅留已有本机副本 | `context/README.md`、`context/AGENTS.md` |
| `skills/` | 所有既有Skill指令和流程，统一治理 | `skills/README.md`、`skills/AGENTS.md` |
| `extensions/` | 既有小工具、程序、脚本和适配实现 | `extensions/README.md`、`extensions/AGENTS.md` |

对象在各域平铺；资料集合和原生程序内部结构不拆散。旧docs/assets/metadata/prompts/research/scripts/tools不再作为并行活动根目录。

### Context平铺文件

原`ai-citation`、`metadata`、`prompts`、`getting-started`目录中的文件已平铺到`.github/`根；无重名的文件保留原名，冲突的`README.md`、`AGENTS.md`仅加集合名区分。两个说明模板为`.github/tool-explanation-template-v0.md`与`.github/tool-explanation-template-v1.md`。导航见`context/README.md`。

| 文件组 | 用途 | 编辑前阅读 |
|---|---|---|
| AI引用文件；指南为`ai-citation-AGENTS.md` | AI引用语料 | `ai-citation-AGENTS.md` |
| metadata文件；指南为`metadata-AGENTS.md` | 分类、术语与历史路径映射 | `metadata-AGENTS.md` |
| 提示词文件；指南为`prompts-AGENTS.md` | 提示词入口 | `prompts-AGENTS.md` |
| 入门文件；指南为`getting-started-AGENTS.md` | 新手入门与项目练习 | `getting-started-AGENTS.md` |

这些带集合名的指南保留分组规则，但不再是按目录自动发现的`AGENTS.md`；本文件负责路由，改动对应文件前须显式阅读。

## 维护脚本与共享库

校验和测试是仓库维护基础设施，不属于用户侧Extensions资源；本次直接平铺到`.github/`，不另建scripts目录或旧路径兼容壳。

| 类别 | 当前入口 |
|---|---|
| Markdown校验 | `check-local-links.py`、`check-markdown-details.py`、`check-doc-structure.py` |
| 目录与导航 | `check-directory-docs.py`、`check-metadata.py`、`check-ai-citation.py` |
| 数据与来源 | `check-gongfa.py`；本机研究副本另用`check-research-raw.py`、`check-source-facts.py` |
| Wiki | `check-wiki.py`；仍只校验明确给定的本地checkout |
| 测试 | `test-gongfa.py`、`test-gongfa-catalog.py`、`test-faqi-catalog.py`、`test-markdown-details.py`、`test-source-archive.py`、`test-research-distribution.py` |
| 共享实现 | `source_boundaries.py`、`taxonomy.py`、`source_archive.py`、`book_views.py`、`tool_explanations.py`直接平铺；供同级入口与原资料生成器共用，不保留lib包 |
| 依赖 | `requirements-gongfa.txt`、`requirements-faqi.txt` |

### 平铺共享模块

| 模块 | 职责 |
|---|---|
| [source_boundaries.py](source_boundaries.py) | 原lib/__init__中的第三方、镜像与研究缓存边界；保留各检查器范围差异 |
| [taxonomy.py](taxonomy.py) | 读取原轻量YAML子集中的分类与文档导航 |
| [source_archive.py](source_archive.py) | 严格读取JSON载荷，核对字节、模式、SHA、当前位置、当前绑定与隔离复原 |
| [book_views.py](book_views.py) | 复用既有链接规则及markdown-it-py，生成文集锚点、历史导航及目录，代码示例不改写 |
| [tool_explanations.py](tool_explanations.py) | 绑定登记v1模板SHA，校验对象覆盖与18项顺序，安全渲染每对象独立三列表格 |

- 5个模块只保存一份，直接导入；不保留`.github/lib/`目录、软链接、__init__兼容包或新的运行框架。
- 公共函数小而稳定，历史来源/选区与当前实现绑定不能混同；不增加模型客户端或独立注册框架。
- 导入阶段不写文件、不联网、不执行目标程序；book_views只加载本仓链接检查器的规则函数。
- source_archive在显式调用时读取资料；`explanations_v1`与冻结的`documents`分层保存，模板版本和完整对象集合由tool_explanations校验；v0不作为活动或兼容载荷。export_documents只向调用方指定的新隔离目录复原，拒绝越界、软链接及敏感路径，不恢复旧运行目录。
- 复用标准库、原YAML子集、既有slug规则及markdown-it-py，不自研解析器；原字节、控制字符、读取预算、归属和并行变化保护不变。
- 修改后先运行相关协议及`make test-source-archive`；最终完整`make test`按根AGENTS执行，不因路径调整削弱断言。

研究档案不属于公开仓库；默认`make test`不运行本机研究事实检查，已有完整本机副本时可显式运行`make test-local-research`。`test-research-distribution.py`防止研究路径重新进入Git索引，并确认整目录被忽略。

3个sync与1个fetch入口仍在Extensions，本次没有迁移它们。保持原校验范围和断言，同步Makefile、真实ROOT、导入与隔离夹具；从其他cwd调用不能误判仓库根。
原3份Actions定义已从当前文件树移除，原始字节仍保留在Git历史中；迁移Python脚本不恢复自动CI。

## 平台入口

`ISSUE_TEMPLATE/`、`CODEOWNERS`、`FUNDING.yml`、`PULL_REQUEST_TEMPLATE.md`、`SECURITY.md`、`WIKI.md`、`labeler.yml`、`lint_config.json`保留现有位置；用户本次点名workflows，不扩改其他协作入口。

- `workflows/`已退役，不再作为平台例外；禁止重建目录、符号链接或兼容壳。原3个定义已从当前文件树移除，原始提交仍在Git历史中。
- 自动CI、Labeler和Welcome不再触发；本地校验/测试由根Makefile调用同级维护脚本，资料维护仍调用Extensions入口，不把空远端检查当CI成功。
- CODEOWNERS仍由`@tukuaiai`、`@tradecatlabs`覆盖，仅迁移路径，不改变审批或豁免资格。
- Actions定义只在历史提交中保留，不复制或执行；恢复自动化须显式授权，不能只重建路径而忽略权限、输入及检查生产者。
- 审批Ruleset25244224的`tradecatlabs`豁免只用于其自己的PR；其他PR仍须有效批准。仅退役两套保护中已停用的`markdown-lint`/`link-checker`；签名、PR、线性历史及其它保护不变，不伪造审核。
- Issue/PR模板保持协作职责，长期规则写根AGENTS或资源域AGENTS，不塞入模板与CI。
- 固定来源使用Extensions下四个Gitlink；不得提交缓存、私有模板、真实会话、数据库或凭据。

## 验证

从仓库根运行相关`make lint`、`make check-links`、`make check-directory-docs`及受影响协议检查，最终完整测试以根AGENTS为准。
