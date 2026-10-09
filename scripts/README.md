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
- `sync-faqi-catalog.py`：法器来源初审JSON、固定Git/SHA/选区、身份/入口及资源覆盖校验与只读清单生成，不推断类型或执行被审工具。
- `test-faqi-catalog.py`：真实CLI消费与拒绝行为、代码表保真/注入隔离、重复生成及输出所有权验证；保留输入、退出码和JUnit。
- `requirements-faqi.txt`：法器维护与测试的固定依赖，复用已安装成熟库，不安装被审工具依赖。
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

## 法器来源初审清单

```bash
python3 -m pip install -r scripts/requirements-faqi.txt
make sync-faqi-catalog
make check-faqi-catalog
make test-faqi-catalog
```

维护需Python3.10+、Git及按当前父仓库固定指针初始化的submodule；集成测试使用Linux/WSL的`resource`限制异常宽表内存。
字段判定只编辑[metadata/faqi.json](../metadata/faqi.json)，原名称、ID、风险和验证状态只读自原资源YAML；
类型只引用本体，输出[tools/faqi-catalog.md](../tools/faqi-catalog.md)不承接正文或第二本体树。

依赖来源及最低/固定版本：

- [jsonschema 4.26.0](https://pypi.org/project/jsonschema/4.26.0/)：复用Draft2020-12字段校验，不自研Schema解释器。
- [PyYAML 6.0.3](https://pypi.org/project/PyYAML/6.0.3/)：安全读取原资源YAML，拒重复键和别名展开。
- [tabulate 0.9.0](https://pypi.org/project/tabulate/0.9.0/)：生成可复制的psql原样代码表。
- [markdown-it-py 3.0.0](https://pypi.org/project/markdown-it-py/3.0.0/)：测试用真实Markdown解析验证转义边界，不mock维护核心。

默认/`--check`只读；`--write`仅写带生成标记的视图，先校验全部来源、上限与输入/目标摘要，再单文件原子替换。
文件/生成视图输入上限2 MiB，最多128来源、512实现、每分类4096资源行；固定Git命令预算20秒。
格式化前保守核代码表列宽×行数预算，不让一条长名称扩大整表、耗尽内存后才拒绝；不截断原文。
原文选区按一基半开区间和原UTF-8字节SHA核，不清洗或执行HTML/代码/提示词。
首批父仓库修订绑定已发布主线的历史提交，不依赖本地未推送提交；历史Git对象须可读，浅克隆不保证来源可回放。
重复内容身份、入口错配、缺失资源ID、越界/凭据/日志/数据库来源、未知字段与NaN均非零失败。
路径/来源/指针变更先重新核证；并行修改采用前后摘要及指针复核，不声称多文件事务或跨写者强CAS。

`test-faqi-catalog.py --artifacts /tmp/新的目录`保存真实输入、命令/退出码、日志、result.json和JUnit，拒绝覆盖已有证据目录。
仅此初审与维护测试纳入本地`make test`；GitHub Actions选定目标未改，不声称远端运行了法器测试。
程序源码存在、Schema及消费通过不证明语义真、效果、安全、许可证或独立审查；不按功法十二级给法器赋级。
