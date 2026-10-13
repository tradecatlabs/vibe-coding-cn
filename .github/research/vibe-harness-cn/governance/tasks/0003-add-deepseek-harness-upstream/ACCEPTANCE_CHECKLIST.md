# Acceptance Checklist

# Global Standards
- [x] Task Intent 与 Verification Plan 为 READY。
- [x] 改动范围只覆盖第四源接入、必要测试、文档与治理证据。
- [x] 未执行上游代码，未读取或输出凭据。
- [x] Required capabilities、governance strict/health 和 task docs validator PASS。
- [x] 文档同步与回滚路径已记录。

# Task Package Checklists
## TP-01
- [x] 官方 origin/branch/license/core paths/preview 已核验。
- Verify: checkout Git/tree/license inspection。
- Gate: 来源事实绑定当前 revision。

## TP-02
- [x] 单一 registry 同时驱动同步和 lock，回归覆盖第四源与拒绝路径。
- Verify: `bash tests/test_sync_upstreams.sh`。
- Gate: 四源定义一致且拒绝路径不退化。

## TP-03
- [x] 真实四源同步、幂等 digest、lock/checkouts inspection 和本地交付完成。
- Verify: sync twice、项目与治理门禁、task validators。
- Gate: 当前输入无 BLOCK 且本地 commit 可追踪。
