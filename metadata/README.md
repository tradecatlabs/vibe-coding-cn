# metadata

本目录存放机器可读索引，用于约束文档结构、AI 引用入口和历史路径映射。

## 文件

- `taxonomy.yml`：知识库分类、阅读路径和关键文档入口。
- `glossary.yml`：项目术语表。
- `redirects.yml`：历史路径到当前入口的映射，供维护和 AI 上下文使用。

## 使用

修改目录、锚点、阅读路径或关键入口后，必须同步更新本目录，并运行：

```bash
make check-metadata
make test
```
