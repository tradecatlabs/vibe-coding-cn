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

## 法器总分类登记

- `faqi.json`是法器总分类登记的唯一可编辑源：包含固定来源实现初审、Vibe Coding依赖图具名对象/实例、用户确认纳入的依赖类别、暂定品级记录及外部资源逐ID分流；字段契约由`faqi.schema.json`约束。
- 类型只引用唯一本体；原资源ID、名称、地址、状态、验证状态和风险仍归`assets/external-resources/`分类YAML，不复制为第二资源登记。
- 程序内容、运行实例、模型、服务、硬件、信息内容、过程、地址及账号按真实所指分离；用户可确认依赖类别纳入范围，但该确认不自动补出具体产品身份、版本或任务效果等级。
- 来源用途是人工初审标注，Schema/后缀/SHA不能证明语义正确；`exclusion_evidence`不能作为纳入对象实现来源。每个空纳入入口至少有一条显式排除记录；同一入口可列多项排除对象，按入口路径与名称去重，排除来源分别唯一绑定，不能静默复入。
- `faqi-grade-vocabulary-v1`仍为draft且效能结果带阈值未校准；正式效能评级与当前`provisional_grade_assignments`的重要性分级是不同轴。用户要求暂按Vibe Coding核心模型/Agent、代码执行与变更基础、质量/上下文/产品交付增强、可替代专用支路分层；各阶初中高表示阶内重要性，不表示效果或实现质量。运行时对象正式`grade_id`仍为null，效能验证仍为false。
- 固定来源修订、原字节SHA与一基半开选区；新内容/版本重新核身份，不继承旧能力，不覆盖旧Git来源事实。依赖图文本SHA与观测时间分别绑定，不冒称固定源码来源。
- `tools/faqi-catalog.md`只读生成；运行`make sync-faqi-catalog`、`make check-faqi-catalog`、`make test-faqi-catalog`，保留真实工件。

## 验证

```bash
make check-metadata
make check-faqi-catalog
make test-faqi-catalog
make check-gongfa
make test-gongfa
make test
```

<!-- 用户授权审计：门禁=metadata/AGENTS.md#法器来源初审、docs/gongfa/AGENTS.md#唯一维护边界；用户原话摘要=“从完整依赖图提取工具、平台等对象，更新法器总分类评级表并打印”；时间=2026-10-10T13:32:28Z；绕过范围=将法器登记/只读视图扩展为总分类与依赖图观察表；不绕过分级证据门槛，等级保持待核；结果=登记v2列入13个具名对象/运行观察、9个仓内图节点关联及8个未具体化节点，原10项来源实现与外部资源分流保留。 -->
<!-- 用户授权审计：门禁=metadata/AGENTS.md#法器总分类登记中的依赖类别待核边界；用户原话摘要=“待核的我全部核查过了，开始执行分类，全部进入”“全部纳入”；时间=2026-10-10T14:28:10Z；绕过范围=将8个依赖图类别由待核身份改为用户确认纳入评估范围；不推断具体实现、版本或品级，不绕过效能分级证据门槛；结果=8类均标记user_confirmed_in_scope并纳入生成视图，正式等级仍未赋值。 -->
<!-- 用户授权审计：门禁=docs/gongfa/cultivation-ontology-taxonomy.md#法器品级规约（draft阈值未校准、不得默认最低档）；用户原话摘要=“给全部NULL／未赋级赋予品级”；时间=2026-10-10T17:10:19Z；绕过范围=为原25条未赋级记录暂列黄阶初级，其中8条依赖类别按用户确认纳入，已有6条烟测记录保留具体任务范围；这是可撤销的用户授权分组，不声称效能已验证或正式评级；结果=31条登记均有暂定品级记录，生成视图按天、地、玄、黄分组，正式效能验证仍为false。 -->
<!-- 用户授权审计：门禁=docs/gongfa/cultivation-ontology-taxonomy.md#法器品级规约（品级按任务效果定义）与metadata/AGENTS.md#法器总分类登记（暂定品级边界）；用户原话摘要=“按照对于vibecoding重要性排序作为品级分类”；时间=2026-10-11T06:19:20Z；范围=全部31条法器/依赖对象及类别的暂定品级，从统一黄阶初级改为按核心闭环重要性、执行关键性、上下文/质量/交付作用及可替代性排序；结果=天5、地12、玄9、黄5，仍不代表效能验证、实现质量或正式评级，正式效能grade_id保持null；此前烟测未用于重要性排序：Skill Seekers创建因缺PyMuPDF未运行成功、auto-tmux doctor因脚本Git mode为100644失败，其他高副作用路径未运行，记录仍见/tmp/faqi-rating.WdWHPQ/rating-report.md。 -->
