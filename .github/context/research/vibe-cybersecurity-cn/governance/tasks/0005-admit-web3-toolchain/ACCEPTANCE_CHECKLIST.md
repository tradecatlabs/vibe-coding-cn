# Acceptance Checklist

## Global Standards

- [x] 未来终态、真实约束、proof point 和 falsifier 已记录。
- [x] 新增长期对象通过存在性检查（准入目录/校验器为门禁必需）。
- [x] 成熟工具优先；自研仅准入校验与属性 wrapper。
- [x] 网络副作用为零；git 仅本地 init/提交，无远端。

## Task Package Checklists

### TP-01

- [x] 5 项工具 9 门禁全过并 admitted。
- Verify: `validate_web3_admission.py` PASS。
- Gate: 每项门禁绑定真实证据，无 blocking_conditions。

### TP-02

- [x] forge-std v1.16.2（commit bf647bd）固定重装。
- Verify: `forge build` + `forge test` 4/4。
- Gate: tag 与 commit 可追溯；旧目录备份在 /tmp。

### TP-03

- [x] Echidna 属性覆盖 4 漏洞，反例证据落盘。
- Verify: `evidence/echidna-*-2026-08-14.log` 4 份。
- Gate: 反例语义与 ground truth 一致。

### TP-04

- [x] git 初始化 + 2 笔提交；policy enforce；验证门禁全绿。
- Verify: `validate_task_verification.py` enforced=True ready=True。
- Gate: `build_task_closeout.py` closeout_gate.ready=true。

### TP-05

- [x] 治理同步与 closeout 完成。
- Verify: task docs closeout + governance strict/health。
- Gate: 无占位、死链或过度声明。
