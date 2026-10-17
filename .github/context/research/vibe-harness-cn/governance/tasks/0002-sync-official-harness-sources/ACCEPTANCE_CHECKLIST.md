# Acceptance Checklist

# Global Standards
- [x] 只使用实际官方 origin、branch、commit 与许可证证据。
- [x] 上游 checkout 被 Git 忽略且未执行任何上游脚本。
- [x] Claude Code 核心源码不可见性已写入机器和人类真相源。
- [x] 同步入口幂等、失败非零、无 reset/强制覆盖。
- [x] 根、research、scripts、tests 的 AGENTS 与 governance module context 已同步。
- [x] 当前输入的 high-risk required capability 工作树预检全部 PASS；正式结果由 clean HEAD runtime evidence 与 strict 重验裁决。
- [x] 最终 review、task docs、governance health 与本地 Git 交付边界已收口。

# Task Package Checklists
## TP-01
- [x] OpenCode 官方仓库与核心路径核验。
- [x] Codex 官方仓库与核心路径核验。
- [x] Claude Code 官方仓库、许可证和公开范围核验。
- Verify: 检查实际 checkout 的 origin、branch、license 和核心路径。
- Gate: 三个来源均绑定官方 revision，未知实现不被推断补齐。

## TP-02
- [x] checkout 目录 gitignored。
- [x] 同步脚本固定官方 origin 与登记分支。
- [x] lock 保存 revision、license、visibility、paths/counts/limitation。
- [x] 研究基线声明不执行、不 vendoring、不推断。
- Verify: `bash scripts/sync_upstreams.sh` 并校验 lock JSON。
- Gate: 三仓同步成功，同 revision 重跑不漂移。

## TP-03
- [x] 真实 failure 已观察并形成三条假设。
- [x] 最小 deepen 实验证实根因。
- [x] 本地 Git 回归覆盖前进、分支、脏树、改写。
- [x] RED/GREEN/counterfactual owner contract 已建立。
- Verify: 运行 `auto-debug` 的 debug note 与 regression evidence validators。
- Gate: 最终脚本/测试摘要绑定的 RED、GREEN、counterfactual 均有效。

## TP-04
- [x] 真实三仓同步与 lock 幂等复验。
- [x] Verification Plan READY，required gates 工作树预检 PASS；正式 closeout 只接受 clean HEAD strict 结果。
- [x] governance rebuild/strict/health。
- [x] review、审计/复用采样与 task-local 复盘边界收口。
- Verify: 执行 Verification Plan、governance、task docs、review/closeout validators。
- Gate: 当前输入无未处理 BLOCK，unknowns 与外部 provenance 边界明确。
