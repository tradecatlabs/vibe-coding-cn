# metadata

本目录存放机器可读索引及限定子域的数据协议，用于约束文档结构、AI 引用入口、历史路径映射和功法登记。
类型与语义仍以本体主文为准，不在此维护另一棵分类树。

## 文件

- `taxonomy.yml`：知识库分类、阅读路径和关键文档入口。
- `glossary.yml`：项目术语表。
- `redirects.yml`：已经不存在的历史路径到当前入口的映射，供维护和 AI 上下文使用。
- [faqi.json](faqi.json)：来源限定的法器实现初审及外部资源逐ID分流的唯一可编辑判定；原资源事实仍归分类YAML。
- [faqi.schema.json](faqi.schema.json)：首批程序内容初审的字段与声明边界，不复制本体父链或维护能力、许可、品级。
- [法器清单](../tools/faqi-catalog.md)：上述初审与原资源事实的生成视图；不手改，不把候选自动晋升为已核程序。
- [gongfa/](gongfa/README.md)：功法JSON核心、限定内容、四阶十二级、人工分类/初评、冻结来源与正式评级历史。
- [功法总表](gongfa/catalog.md)／[Excel完整视图](gongfa/catalog.xlsx)：当前登记与已分类来源候选的同一总视图；聚合数量由生成器维护，不复制分批表。

## 使用

功法检查需要Python3.10+及`python3 -m pip install -r scripts/requirements-gongfa.txt`。
法器维护需要Python3.10+、Git与`scripts/requirements-faqi.txt`；submodule须按父仓库固定指针初始化。
更新法器来源或实现内容须核身份/版本，保留旧Git修订及旧记录，不把同名、副本、声明版本或源码变化自动当能力升级。
本轮16项纳入，Chat Vault、MC Player Transfer、XHS ZIP→PDF 3项保留为明确范围排除和源码证据，不作为faqi对象；复入前须满足各自隔离数据/副作用复核条件。
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
