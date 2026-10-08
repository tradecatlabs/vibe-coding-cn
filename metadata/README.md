# metadata

本目录存放机器可读索引及限定子域的数据协议，用于约束文档结构、AI 引用入口、历史路径映射和功法登记。
类型与语义仍以本体主文为准，不在此维护另一棵分类树。

## 文件

- `taxonomy.yml`：知识库分类、阅读路径和关键文档入口。
- `glossary.yml`：项目术语表。
- `redirects.yml`：已经不存在的历史路径到当前入口的映射，供维护和 AI 上下文使用。
- [gongfa/](gongfa/README.md)：功法JSON核心、限定内容、四阶十二级、人工分类/初评、冻结来源与正式评级历史。
- [功法总表](gongfa/catalog.md)／[Excel完整视图](gongfa/catalog.xlsx)：当前登记与已分类来源候选的同一总视图；聚合数量由生成器维护，不复制分批表。

## 使用

功法检查需要Python3.10+及`python3 -m pip install -r scripts/requirements-gongfa.txt`；其他脚本依赖不变。

修改目录、锚点、阅读路径或关键入口后，必须同步更新本目录，并运行：

```bash
make check-metadata
make check-gongfa
make test-gongfa
make sync-gongfa-catalog
make check-gongfa-catalog
make test-gongfa-catalog
make test
```
