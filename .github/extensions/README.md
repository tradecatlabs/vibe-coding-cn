# Extensions：既有程序与小工具

## 字多不看

这里保存现存程序、资料维护脚本与固定上游；当前13个一级对象在本域平铺，程序内部源码结构不拆散。
这里的Extensions不是Pi原生扩展的同义词；不能把整个目录交给Pi的`-e`加载。

## 快速导航

| 既有对象 | 入口与用途 |
|---|---|
| [Skill Seekers](Skill_Seekers-development/README.md) | 固定上游源码；原本地适配脚本已退役，按上游说明与具体授权选择使用 |
| [Claude官方Skills源](claude-official-skills/README.md) | 固定上游源码，不属于当前Skills发现集合 |
| [Skill初始化入口](init_skill.py) | 引用上游初始化脚本；不是Pi Skill入口或自动安装器 |
| [tmux](tmux/README)、[oh-my-tmux](oh-my-tmux/README.md) | 原固定源码与配置仓库；不是自动安装或启用 |
| [提示词转换](prompts-library/README.md) | 原Excel、Markdown、JSONL转换程序 |
| [EPUB CSS清理](clean_epub_css.html) | 保留的HTML工具文件 |
| [Markdown编辑](markdown-bianjiqi.html) | 保留的HTML工具文件 |
| [任务卡生成](task%20card%20generator.html) | 保留的HTML工具文件 |

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

仓库级校验和测试入口由仓库根`.github/`维护，不属于本域工具；入口与职责见[维护规则](../AGENTS.md#维护脚本与共享库)。
本域保留以下资料维护入口；本次没有扩大迁移范围：

| 范围 | 本域保留入口 |
|---|---|
| 文档目录 | [sync-doc-toc.py](sync-doc-toc.py) |
| 功法视图 | [sync-gongfa-catalog.py](sync-gongfa-catalog.py) |
| 法器视图 | [sync-faqi-catalog.py](sync-faqi-catalog.py) |
| 研究事实获取 | [fetch-research-raw.py](fetch-research-raw.py)；需要明确联网授权 |

共享实现只有一份；职责与原库规则见[维护说明](../AGENTS.md#维护脚本与共享库)，资料生成器直接使用仓库根层平铺模块，不保留lib目录。两个目录生成器从原始JSON中的`explanations_v1`读取唯一活动说明载荷，输出轻量README导航页及天、地、玄、黄四阶正文；每个对象仍单独使用一张18项严格三列表格。v0仅保留为历史模板，不接受旧载荷兼容。未定级功法在黄阶文档中单列并标明“不归黄阶”。完整本地检查仍为`make test`，不执行被审第三方程序，也不证明运行、效果或许可。

### 依赖与执行边界

检查器使用Python3；功法、法器和资料档案维护使用Python3.10+，共享依赖在`.github/`，见[requirements-gongfa.txt](../requirements-gongfa.txt)、[requirements-faqi.txt](../requirements-faqi.txt)。
复用jsonschema、PyYAML和markdown-it-py；v1的18项表格由共享模块按固定三列表格契约安全渲染。转换程序另用其原有requirements。Markdown lint使用Node22+及固定的markdownlint-cli0.48.0。

来源树保持原Git修订。安装、抓取、上传、发布、修改配置和终端注入均有独立副作用，不因移入本域得到授权。
凭据仅从受信来源在运行时注入，不提交真实会话、数据库、API密钥、环境文件或私有模板。
