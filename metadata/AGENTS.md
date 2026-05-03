# metadata/ Agent 指南

本目录维护机器可读索引，是 README、docs 和 AI 引用资产之间的结构桥。

## 约束

- 新增、删除、移动或重命名 docs 入口时，必须同步 `taxonomy.yml`。
- 历史路径仍需被 AI 或外部说明理解时，维护 `redirects.yml`。
- 术语口径变化时，同步 `glossary.yml`。
- 不确定的映射不要猜；先查当前文件和锚点，再修改。

## 验证

```bash
make check-metadata
make test
```
