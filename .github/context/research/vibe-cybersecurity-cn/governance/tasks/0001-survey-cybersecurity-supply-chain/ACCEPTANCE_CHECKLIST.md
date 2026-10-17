# Acceptance Checklist

## Global Standards

- [x] 只使用官方/原始来源支撑候选事实。
- [x] 上游事实、项目判断与未验证项分离。
- [x] 网络副作用和隔离要求是一等字段。
- [x] 安全工具自身供应链按高价值输入处理。
- [x] 没有执行安装、扫描、登录、部署或外部写入。

## Task Package Checklists

### TP-01

- [x] 八类范围、证据层级、评分和停止条件冻结。
- Verify: 人工审阅 `SEARCH_PROTOCOL.md`。
- Gate: 新候选必须填补真实缺口，不能只增加同类数量。

### TP-02

- [x] 关键来源覆盖官方仓库、文档、许可、advisory、标准和论文。
- [x] 来源账本明确每项证据天花板。
- Verify: `fact_sources` URL 结构检查与来源抽查。
- Gate: 搜索摘要不进入强结论。

### TP-03

- [x] 46 个候选具备完整机器字段。
- [x] MVP/pilot/reference/hold 状态和首个组合明确。
- Verify: `python3 validate_candidates.py`。
- Gate: 自动表由 JSON 确定性生成，`active-high` 不得进 MVP。

### TP-04

- [x] Python、JSON、任务文档和治理 strict/health 纳入校验。
- [x] 当前审查为 WARN，未把研究完成包装成系统就绪。
- [x] 复用采样已生成；复盘 requirement 已派生，canonical handoff 阻塞已如实记录而未伪造通过。
- Verify: 本任务 `REVIEW.md` 与最终验证命令。
- Gate: 所有命令新鲜通过或明确记录失败。
