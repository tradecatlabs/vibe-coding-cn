# Task Lessons Candidate Pool

本文件是任务级候选教训整理池，只记录尚未拆分、晋升或拒绝的原始经验材料。

## 使用规则

- 任务执行中发现的纠偏、失败复盘、可复用验收标准或防复发经验，可以先追加到这里。
- 写入后必须拆成原子事实：事实、来源、影响、通用规则、建议目标位置。
- 通用规则最终应晋升到 `governance/evidence/lessons/`、`governance/architecture-gates/rules/`、`governance/standards/`、`governance/processes/`、`governance/decisions/adr/` 或 `governance/context/module-contexts/`。
- 已晋升或拒绝晋升的条目，应保留简短处理记录，避免同一教训长期堆积在候选池。

## Candidate Lessons

- 工具接入前必须先收敛前置条件（PATH、版本管理器的编译器安装），再进证据链；
  否则会出现"工具存在但运行失败"的假阴性。来源：0004 TP-02/TP-04。
  建议晋升位置：`governance/processes/本地工具与验证入口.md`。
- 新工具的输出契约（如 Echidna `--format json` 实际混合文本日志与 JSON）必须
  以真实运行样例确认，不依赖旧版行为假设。来源：0004 TP-04。
  建议晋升位置：`governance/standards/工程质量标准.md`。
- Echidna 2.3.3 的 `balanceContract` 配置会导致部署失败；应先用最小配置
  验证部署契约，再用 `balanceAddr` + wrapper 提供资金。来源：0005 TP-03。
  建议晋升位置：`governance/processes/本地工具与验证入口.md`。
- 属性模型必须先做守恒推演（买卖对净投入的影响）再编码，否则反例是
  属性缺陷而非真实漏洞。来源：0005 TP-03。
  建议晋升位置：`governance/standards/工程质量标准.md`。
- 供应链静态审计的高危模式命中（curl|bash、私钥、注入指令）绝大多数是
  教学示例/检测规则，必须逐条人工核对内容而非只看正则命中。来源：0006 TP-02。
  建议晋升位置：`governance/processes/本地工具与验证入口.md`。
- 攻击工具库（如 FuzzDB nc.exe）是真实二进制，审计须单独标记并隔离存储，
  禁止执行。来源：0006 TP-02。
  建议晋升位置：`governance/architecture-gates/rules/`。
