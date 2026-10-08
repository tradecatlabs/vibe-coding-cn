# metadata/ Agent 指南

本目录维护机器可读索引与限定子域数据协议，是 README、docs 和 AI 引用资产之间的结构桥。

## 约束

- 新增、删除、移动或重命名 docs 入口时，必须同步 `taxonomy.yml`。
- 历史路径仍需被 AI 或外部说明理解时，维护 `redirects.yml`。
- 术语口径变化时，同步 `glossary.yml`。
- 不确定的映射不要猜；先查当前文件和锚点，再修改。
- `redirects.yml` 只记录已经不存在的历史路径到当前入口的映射；禁止添加指向自身的自映射。
- `redirects.yml` 的 `from` 必须唯一，且不能仍然存在于仓库中。

## 功法子域

- `gongfa/registry.json`是功法品级与条目数据的唯一可编辑源，Schema和冻结来源同目录维护。
- 本体主文仍是类型与语义入口；JSON只引用已有主类并附人工判定理由，不复制主父树或推广为全仓IR。
- 修改来源、内容版本或规则时遵守`gongfa/AGENTS.md`；不凭原文宣传、篇幅或候选收录状态赋级。
- 人工初评批次保存于`grade_proposals`，不能冒称实测评级或放松草案`rated`检查；表格由JSON只读输出。
- README品级块由JSON生成，运行`make check-gongfa`和`make test-gongfa`，保留真实退出码及产物。
- 功法总表`gongfa/catalog.md`与`catalog.xlsx`由同一脚本生成，输入为当前登记和仓内冻结候选历史材料。
- `catalog-sources.json`只索引不可变候选来源的路径/SHA/范围，不持有活跃登记或新评级，不是第二可编辑登记。
- 候选来源保留旧编者意见并明确未登记；不同限定内容和同名条目不自动合并或继承品级。
- 更新后运行`make sync-gongfa-catalog`、`make check-gongfa-catalog`及`make test-gongfa-catalog`，不手改生成视图。

## 验证

```bash
make check-metadata
make check-gongfa
make test-gongfa
make test
```
