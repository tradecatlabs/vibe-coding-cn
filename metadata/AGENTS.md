# metadata/ Agent 指南

本目录维护机器可读索引，是 README、docs 和 AI 引用资产之间的结构桥。

## 约束

- 新增、删除、移动或重命名 docs 入口时，必须同步 `taxonomy.yml`。
- 历史路径仍需被 AI 或外部说明理解时，维护 `redirects.yml`。
- 术语口径变化时，同步 `glossary.yml`。
- 不确定的映射不要猜；先查当前文件和锚点，再修改。
- `redirects.yml` 只记录已经不存在的历史路径到当前入口的映射；禁止添加指向自身的自映射。
- `redirects.yml` 的 `from` 必须唯一，且不能仍然存在于仓库中。

## 验证

```bash
make check-metadata
make test
```
