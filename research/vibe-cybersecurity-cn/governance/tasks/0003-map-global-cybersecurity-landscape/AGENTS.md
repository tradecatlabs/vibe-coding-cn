# Global Landscape Task Guidelines

本目录保存网络安全全局景观的来源、覆盖映射、任务契约和验证证据；长期坐标系位于
`governance/context/CYBERSECURITY_LANDSCAPE.md`，产品边界位于 ADR-0001。

## 文件地图

```text
0003-map-global-cybersecurity-landscape/
├── README.md                 # 任务目标、范围和阅读入口
├── CONTEXT.md                # 仓库证据、约束、风险和推翻条件
├── PLAN.md                   # 生命周期、最短路径和回滚
├── ACCEPTANCE*.md            # 可执行验收与检查表
├── TODO.md / STATUS.md       # 当前执行和 closeout 状态
├── TASK_INTENT*.json         # 任务意图输入与编译结果
├── SOURCE_LEDGER.md          # 权威框架与标准来源账本
├── LANDSCAPE_COVERAGE.md     # 46 项候选到全局能力的映射
├── REVIEW.md                 # 专项审查和剩余风险
└── REUSE_SAMPLING.json       # 主要任务复用采样决策
```

## 边界

- 不在本目录复制 0001 的逐工具事实或 0002 的准入状态。
- 不把市场类别、框架映射、候选覆盖写成运行能力或实证漏洞。
- 动态版本必须记录观察日期和官方来源。
- 不保存扫描响应、payload、凭据或目标信息。

## 验证

使用 `validate_task_docs.py --phase closeout` 和项目治理 strict/health；候选总数从 0001 JSON 读取核对。

