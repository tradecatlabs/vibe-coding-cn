# scripts

本目录存放仓库级自动化脚本，例如链接检查、索引生成、taxonomy 校验和文档结构校验脚本。

当前已有：

- `check-local-links.py`：仓库内 Markdown 相对链接与锚点检查脚本。
- `check-markdown-details.py`：仓库内 Markdown `<details>/<summary>` 折叠块结构检查脚本。
- `check-doc-structure.py`：`docs/` README 的标准块顺序、目录入口、重复锚点与细粒度目录入口检查脚本。
- `check-directory-docs.py`：仓库自有目录 `README.md` / `AGENTS.md` 覆盖检查脚本；根 `.github/` 仅要求 `AGENTS.md`，避免 GitHub 首页误展示平台配置说明。
- `check-metadata.py`：`metadata/taxonomy.yml` 与 `metadata/redirects.yml` 路径和锚点检查脚本。
- `check-gongfa.py`：功法JSON、十二级、冻结来源/原文、初评与正式评级的引用/历史离线检查；`--render-grades`输出词表，`--render-catalog`输出分类初评表。
- `test-gongfa.py`：功法协议的隔离CLI集成测试，保留输入、命令、退出码、日志、result.json与JUnit工件。
- `sync-gongfa-catalog.py`：当前登记＋仓内冻结候选的单一总表生成与只读检查，不改品级、主登记或功法身份。
- `test-gongfa-catalog.py`：总表覆盖、版本/纠正范围、离线可移植性、Excel文本安全与陈旧视图的行为测试。
- `requirements-gongfa.txt`：功法检查和总表脚本的独立依赖清单，Python3.10+，不影响其他脚本。
- `check-ai-citation.py`：`llms.txt` 与 AI 引用语料的路径、锚点和规范仓库身份检查脚本。
- `check-external-resources.py`：本地外部资源注册表字段、分类统计、ID 与链接形态检查脚本。
- `check-research-raw.py`：研究域 raw 原始事实层、Git 工作树、来源清单和核心材料文件检查脚本。
- `check-source-facts.py`：外部源事实镜像、文件数、边界和隐私登记检查脚本。
- `fetch-research-raw.py`：按 `research/*/domain.yml` 拉取 GitHub 研究对象的 raw 原始事实层和 `repository/` 工作树。

`research/vibe-cybersecurity-cn/`、`research/vibe-harness-cn/` 和 `research/vibe-mathing-cn-public/` 是外部源事实镜像，不是父仓库研究域；事实登记位于 `research/facts/sources.yml`。仓库级 lint、相对链接、`details` 和目录覆盖检查会跳过这些源内容，镜像边界由 `check-source-facts.py` 验证。
- `check-wiki.py`：GitHub Wiki 独立仓库本地 checkout 的页面覆盖、内链和旧口径检查脚本。
- `sync-doc-toc.py`：兼容旧线性 README 的细粒度目录生成脚本；当前拆分结构下通常无变更。

## 功法JSON检查

```bash
python3 -m pip install -r scripts/requirements-gongfa.txt
make check-gongfa
make test-gongfa
python3 scripts/check-gongfa.py --render-catalog --proposal-batch gongfa-author-repo-expansion-20261007
```

分类/暂定品级表只读自JSON，多批次用`--proposal-batch`显式选取；不按最新时间自动裁决跨范围结论。
原批次标识为`gongfa-author-initial-20261007`；输出标明所选批次，“本批未初评”不代表其他批次没有意见。
检查不联网、不执行来源中的代码/提示词，也不计算真实品级；数据入口见[功法JSON核心](../metadata/gongfa/README.md)。
`test-gongfa.py --artifacts /tmp/新的目录`可指定证据目录；已存在目录拒绝覆盖。
登记检查、总表检查和相关测试纳入本地`make test`；GitHub Actions选定目标未改，不宣称新增远端覆盖。

## 项目内功法总表

```bash
make sync-gongfa-catalog
make check-gongfa-catalog
make test-gongfa-catalog
```

总表入口：[仓内浏览](../metadata/gongfa/catalog.md)／[Excel完整视图](../metadata/gongfa/catalog.xlsx)，两者来自同一消费链。
只读输入是当前登记和`catalog-sources.json`所指仓内快照，不再读取个人目录、原HTML、完整Solve或临时分析工件。
默认运行只检查；`--write`只重建带本工具生成标记的两个视图，先检查文字上限和目标摘要，再单文件原子替换。
中途失败不会改源数据；两种呈现若不一致，检查非零，重跑生成即可恢复，不静默跳过错误。

依赖沿用[openpyxl](https://openpyxl.readthedocs.io/)（最低及固定版本3.1.2），与Schema/HTML检查依赖共同声明。
`test-gongfa-catalog.py --artifacts /tmp/新的目录`保留隔离输入、CLI命令/日志及结果，拒绝覆盖已有证据目录。
候选快照记录之前的编者意见，不作为第二可编辑登记；正文、分类、品级或选区更新必须另存来源版本。
内容新版本不继承旧初评；显式纠正链选有效意见，不同情境仍并列保留，不按最新时间或最高档裁决。
