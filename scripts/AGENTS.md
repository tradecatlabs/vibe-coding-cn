# scripts/ Agent 指南

本目录维护仓库级自动化脚本，主要用于 Markdown、链接、锚点、metadata、功法JSON、AI 引用资产及仓库身份、外部资源注册表校验、研究域 raw 原始事实层与 Git 工作树检查和拉取。

## 约束

- 脚本默认从仓库根目录运行，路径解析必须稳定。
- 新增检查脚本时，同步更新 `scripts/README.md`、`Makefile` 和根目录 `AGENTS.md` 的命令清单；只有 CI 环境稳定具备所需输入时才纳入 CI。
- `fetch-research-raw.py` 访问 GitHub 网络 API，只作为手动刷新命令，不纳入 `make test` 或 CI 硬门禁。
- `check-research-raw.py` 只检查本地文件结构和 JSON 形态，可以纳入 `make test`。
- `check-directory-docs.py` 对根 `.github/` 只要求 `AGENTS.md`，不要重新补 `.github/README.md`。
- 修改 docs README 或主题正文的主章节、锚点、索引后，优先运行 `python3 scripts/sync-doc-toc.py`，再运行 `make test`。
- 修改 GitHub Wiki 独立仓库后，运行 `make check-wiki WIKI_DIR=/path/to/wiki`；不要把 Wiki checkout 提交进主仓。
- 检查失败输出应包含文件路径、行号或可定位的错误信息。
- 跳过目录必须明确，至少跳过 `.git`、`.history`、`build`、`node_modules` 和外部源码快照。

## 功法协议脚本

- `check-gongfa.py`复用jsonschema和BeautifulSoup4，不自研Schema/HTML解释器；只检查冻结本地来源，不联网或执行原文。
- 依赖由`requirements-gongfa.txt`隔离声明，检查需Python3.10+；CI未安装这些依赖时不得顺手修改或假称远端覆盖。
- `test-gongfa.py`固定时间及独立清单，CLI输入/输出是真实协议消费，不mock核心；每次保存隔离工件，不能把合成评级当业务效果证明。
- 数据、选择器、只读视图及规则变化先修改契约/测试；未知条件不补零、补正式评级或静默放行。
- 人工初评与正式评级分开校验；初评记录必须有内容摘要、任务族、理由、置信标签及反证，多批次输出显式选范围。
  `--render-catalog`仅输出登记意见，不计算等级或提供效果证明；草案规约不能产生`rated`的约束不放松。

## 功法总表维护

- `sync-gongfa-catalog.py`复用登记校验器与openpyxl，消费当前登记和仓内候选来源快照，不依赖`/tmp`或个人目录。
- 默认/`--check`只读；`--write`只维护`metadata/gongfa/catalog.md`与`catalog.xlsx`，不改主登记、来源快照或初评。
- 先完整校验文字上限、目标归属与摘要，再单文件原子替换；输出软链接、越界路径、非本工具文件或并行修改均拒绝覆盖。
- 内容新版本不继承旧初评；纠正链按显式`supersedes`，不同活动情境保留原意见集合，不按时间或最高等级选一条。
- `test-gongfa-catalog.py`保留输入、命令/日志和结果；检查来源绑定/表示一致性，不证明效果或独立语义批准。
- 注册库仍唯一拥有活跃登记/正式评级；候选历史快照只作来源事实，迁移入库后才考虑退役该来源视图。

## 法器初审维护

- `sync-faqi-catalog.py`复用jsonschema/PyYAML/tabulate，读取初审JSON与原资源YAML，只维护`tools/faqi-catalog.md`；不自动分类、联网、执行工具或写原登记。
- 字段、来源用途、入口/身份与输出边界变化先补真实行为测试；初审不是独立语义、许可证、部署/运行或效果证明，不套功法品级。
- 用户范围排除保留独立证据与重审条件，不进入`objects`；`exclusion_evidence`不可作为实现来源，不能清空排除后静默复入。
- 固定Git/submodule修订、完整字节SHA与一基半开选区；来源/输入/输出软链接、未知字段、漏/重资源、越界/超限与并行漂移非零失败。
- 生成标记、输入/目标前后复核与单文件原子替换只保护本工具输出，不声称多文件事务或跨写者强CAS；失败保留工件，不清理别人文件。
- `test-faqi-catalog.py`复用MarkdownIt消费真实Markdown，独立字面量和失败输入核原样文字、安全隔离与所有权；不mock核心或运行被审工具。
- 依赖独立声明于`requirements-faqi.txt`；本地`make test`纳入维护验证，CI选定目标未改，不冒称远端覆盖。

## 验证

```bash
make test
```
