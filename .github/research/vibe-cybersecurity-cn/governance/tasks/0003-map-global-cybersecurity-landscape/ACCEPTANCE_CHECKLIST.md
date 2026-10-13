# Acceptance Checklist

## Global Standards

- [x] 未来终态、真实约束、惯性约束、proof point 和 falsifier 已记录。
- [x] 新增长期对象已通过存在性检查；没有引入运行时抽象。
- [x] 成熟框架和现有候选优先，自研仅为项目特有文档组织。
- [x] 网络、凭据和外部系统副作用为零。

## Task Package Checklists

### TP-01

- [x] 权威来源和证据上限已落盘。
- Verify: `TASK_INTENT.json`、`SOURCE_LEDGER.md`。
- Gate: 动态版本必须有观察日期和官方来源。

### TP-02

- [x] 四轴景观和产品边界 ADR 已落盘。
- Verify: `CYBERSECURITY_LANDSCAPE.md`、ADR-0001。
- Gate: 不把六个 Function 写成一次性流程，不把集成对象写成自研范围。

### TP-03

- [x] 46 项候选按八类映射，覆盖空白已列出。
- Verify: `jq '[.candidates | group_by(.category)[] | length] | add' ...` 输出 46。
- Gate: research coverage 不得表述为 admitted、verified 或 production capability。

### TP-04

- [x] 专项 review、复用采样和所有 closeout 命令通过。
- Verify: task docs、governance strict/health 与 principle gate。
- Gate: 文档或状态在最终验证后改变必须重跑。
