# Supply Chain Survey Guidelines

本目录是开源网络安全供应链第一轮调研的可追溯证据包。

## 文件地图

```text
.
├── README.md                         # 任务范围、证据入口与候选概览
├── AGENTS.md                         # 本目录维护规则
├── CONTEXT.md                        # 仓库证据、约束、风险和假设
├── PLAN.md                           # 调研生命周期与后续复跑路径
├── ACCEPTANCE.md                     # 完成定义和验证门
├── ACCEPTANCE_CHECKLIST.md           # 逐任务验收清单
├── TODO.md                           # 叶子任务状态
├── STATUS.md                         # 当前事实、证据和下一步
├── SEARCH_PROTOCOL.md                # 检索范围、评分法和停止条件
├── SOURCE_LEDGER.md                  # 官方来源及其证据边界
├── SYNTHESIS.md                      # 选型结论、目标架构和首批组合
├── REVIEW.md                         # 当前审查结论、风险和未知项
├── REUSE_SAMPLING.json               # 主要任务复用价值采样结论
├── RETROSPECTIVE_FACTS.json           # 复盘 requirement 的任务事实输入
├── RETROSPECTIVE_REQUIREMENT.json     # auto-retro 派生的复盘门禁
├── supply-chain-candidates.json      # 候选事实与项目判断的机器真相源
├── validate_candidates.py            # 目录校验与 Markdown 视图生成器
└── CANDIDATE_TABLE.md                # 自动生成的人类可读候选表
```

## 依赖与边界

- `supply-chain-candidates.json` 是候选状态、字段和评分的唯一机器真相源。
- `CANDIDATE_TABLE.md` 只能由 `validate_candidates.py` 重建，禁止手工修补。
- `SOURCE_LEDGER.md` 解释来源能证明什么；`SYNTHESIS.md` 解释本项目据此作出的判断，二者不得混写。
- `mvp` 仅允许进入本地隔离样例，不表示已安装、已复跑、生产就绪或获得外部目标授权。
- 新增候选前必须证明填补真实能力缺口，禁止为了数量堆叠同类工具。
- `RETROSPECTIVE_HANDOFF.json` 当前不存在：全局 auto-retro registry 被无关项目的陈旧证据阻塞，修复 owner state 后才能签发。

## 验证

```bash
python3 validate_candidates.py
python3 -m py_compile validate_candidates.py
```

修改上游事实时更新 `snapshot_date`、`fact_sources` 和相应证据边界；修改采用结论时更新 `rationale`、`blockers` 与评分。
