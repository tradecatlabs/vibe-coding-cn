# Supply Chain Admission Guidelines

本目录把 0001 的研究候选编译成正式供应链准入队列；它不安装、不启用任何工具。

## 文件地图

```text
.
├── README.md                       # 任务边界和入口
├── AGENTS.md                       # 本目录维护规则
├── ADMISSION_POLICY.md             # 生命周期、门禁、波次和硬边界
├── admission-candidates.json       # 准入决策机器真相源
├── validate_admission_candidates.py# 跨目录校验与表格生成器
├── test_validate_admission_candidates.py # 状态机负例回归测试
├── DEBUG.md                        # 临时目录血缘解析 bug 的 RED/GREEN 证据
├── REVIEW.md                       # 自审 findings、未知项与准入阻塞
├── REUSE_SAMPLING.json             # 主要任务复用价值采样
├── ADMISSION_CANDIDATE_TABLE.md    # 自动生成的可读视图
├── CONTEXT.md                      # 证据、约束和风险
├── PLAN.md                         # 执行路径
├── ACCEPTANCE.md                   # 完成定义
├── ACCEPTANCE_CHECKLIST.md         # 验收清单
├── TODO.md                         # 叶子任务
└── STATUS.md                       # 当前事实和下一步
```

## 真相源与边界

- 工具名称、上游、许可初筛和网络副作用来自 0001 的 `supply-chain-candidates.json`。
- 波次、计划职责、准入状态、固定版本和门禁状态只写入 `admission-candidates.json`。
- `ADMISSION_CANDIDATE_TABLE.md` 只能由校验器生成。
- `admission-candidate` 不等于 `admitted`；`admitted` 也不等于 `enabled`。
- 未固定版本、摘要和全部门禁的候选不得进入执行面。

## 验证

```bash
python3 validate_admission_candidates.py
python3 -m py_compile validate_admission_candidates.py
python3 -m unittest test_validate_admission_candidates.py
```
