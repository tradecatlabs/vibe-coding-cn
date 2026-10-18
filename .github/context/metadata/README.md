# metadata

本目录只存放三域资源导航、术语和历史路径映射；功法、法器的原始登记及协议已归各自单一JSON资料集合。
类型与语义仍以本体主文为准，不在此维护另一棵分类树。

## 文件

- `taxonomy.yml`：知识库分类、阅读路径和关键文档入口。
- `glossary.yml`：项目术语表。
- `redirects.yml`：已经不存在的历史路径到当前入口的映射，供维护和 AI 上下文使用。
- [法器原始资料](../faqi/data.json)：原总分类JSON、Schema、来源及历史引用的单一资料源；重要性、正式效能、排除与未验证状态不因迁移改变。
- [法器体系说明](../faqi/README.md#doc-faqi-system)：解释工具/依赖边界、重要性分级及正式效能评价边界；不复制登记或生成总表。
- [法器总表](../faqi/README.md#法器总表)：总登记与原资源事实的生成视图；包括本地实现、图中现实对象、用户确认纳入的依赖类别和重要性分级；正式效能评级仍未赋值，不手改。
- [gongfa/](../gongfa/README.md)：功法JSON核心、限定内容、四阶十二级、人工分类/初评、冻结来源与正式评级历史。
- [功法总表与完整文集](../gongfa/README.md)／[原始JSON资料](../gongfa/data.json)：JSON保存原字节、登记、协议与历史，Markdown生成阅读视图；历史Excel仅作原始载荷保存，不再维护活动Excel。

## 使用

功法检查需要Python3.10+及`python3 -m pip install -r .github/requirements-gongfa.txt`。
法器维护需要Python3.10+、Git与`.github/requirements-faqi.txt`；submodule须按父仓库固定指针初始化。
更新法器来源或实现内容须核身份/版本，保留旧Git修订及旧记录，不把同名、副本、声明版本或源码变化自动当能力升级。
当前固定来源实现10项；依赖图另列12项具名对象/运行观察及8项由用户确认纳入的依赖类别，不与固定来源实现数相加冒称独立产品数。30项按对Vibe Coding的重要性分布于天4、地12、玄9、黄5；此轴表示依赖角色重要性，不表示效能。正式法器效果量表仍为draft且阈值未校准，正式效能评级仍为空。Chat Vault、MC Player Transfer、XHS ZIP→PDF、HTML工具五项及my-nvim共9项仍为明确范围排除；复入前须按各自记录重新核验。
2026-10-15补充oh-my-tmux固定submodule pin `87dcd13a28aeb5f18baee630e24b3f5765ae3a4f`的S65 `.logo/LICENSE`支持来源，选区SHA与文件SHA相同；许可证文本引用可变的tmux `master/logo`路径。该仓内`.logo/logomark.svg`、`.logo/logomark+wordmark.svg`与固定tmux pin的`logo/tmux-logomark.svg`、`logo/tmux-logo.svg`字节不相同；这不排除衍生或其他来源关系，许可覆盖范围及整体再分发兼容性仍未核实。S65只记录线索，不代表许可批准或独立法律审查，`license_approved`仍为false。

2026-10-16补充Skill Seekers固定pin的S66–S73 MCP支持选区：兼容入口、FastMCP监听、打包/上传/安装及抓取调用链。仍是同一程序身份，父仓库`source_revision`与旧来源不变；通配CORS、进程参数密钥、环境继承及独立发布支路只作静态风险线索，不当运行证明。详见[MCP静态复核](../faqi/README.md#doc-faqi-system-skill-seekers-mcp-static-review)及登记中的待核事项。功法本批补审机器学习entries[9..11]与[17]，完整冻结和各索引审阅位置归[gongfa入口](../gongfa/README.md)，不新增登记或评级。

独立语义、运行、效果和许可批准不在此初审格式内；未经相应证据，不修改声明边界。

修改目录、锚点、阅读路径或关键入口后，必须同步更新本目录，并运行：

```bash
make check-metadata
make sync-faqi-catalog
make check-faqi-catalog
make test-faqi-catalog
make check-gongfa
make test-gongfa
make sync-gongfa-catalog
make check-gongfa-catalog
make test-gongfa-catalog
make test
```
