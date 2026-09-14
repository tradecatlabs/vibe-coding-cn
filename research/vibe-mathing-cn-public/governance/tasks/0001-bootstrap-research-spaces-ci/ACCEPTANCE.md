# Task-Level Acceptance

- [x] Problem、Attempt、Result 契约和空真相源存在。
- [x] Solution 是 Result 的派生视图，不是第二写入面。
- [x] 有限证据、自我审查、陈述失真、失效证据和同生成者验证负例被拒绝。
- [x] research/result-library/governance/CI 目录均有职责文档。
- [x] `make check` 和 `make check-full` 本地通过。
- [x] 干净公开克隆等价副本安装依赖并运行 `make check`。
- [x] 初始提交 `33dd5de` 已推送到 `vibemathing/vibe-mathing-cn`。
- [x] GitHub Actions run `31703110676` 绑定实现提交并 PASS。

# Validation Plan

- `python3 -m py_compile scripts/*.py governance/tools/*.py`
- `make check`
- `make check-full`
- 复制 Git index 到无 ignored 材料的临时目录，安装依赖并运行 `make check`。
- staged secrets/path/large-file/ignore 审计。
- `gh run watch` 和 `gh run view` 绑定最终 SHA。

# Review Gate

correctness、contract、security/repo-hygiene、architecture、build-release、performance、document-drift 不得有 BLOCK。外部独立 reviewer provenance 当前不存在，结论只称同一执行主体的确定性审查。

# Runtime Verification Gate

- [x] 负例对晋升规则具有反事实敏感性。
- [x] governance 首次 RED 已按根因修复并同源 GREEN。
- [x] GitHub-hosted Python 3.12 环境完成实现提交验证。

# Ship Readiness

只有公开文件清单、提交、远端 SHA 和 GitHub Actions 全部核验后才将任务状态改为 Done。

# Task Package Acceptance

- TP-01：Schema 与负例能够表达并守住解库边界。
- TP-02：空间与治理真相源没有模板占位或文档漂移。
- TP-03：同一入口覆盖本地和 CI，ignored 资产不成为隐式依赖。
- TP-04：无敏感/大文件/许可边界错误，远端与 CI 绑定当前 HEAD。

# Anti-Goals

- 不产生数学成果。
- 不引入没有当前消费者的抽象和基础设施。
- 不通过放宽测试、删除 Gate 或伪造日志获得绿色结果。
