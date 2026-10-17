# Acceptance Checklist

# Global Standards
- [x] 用户指定的 11 个新增来源全部核验并登记，最终集合恰好为 15。
- [x] 未执行上游代码、未读取或输出凭据，checkout/runtime 均保持 ignored。
- [x] Task Intent、Verification Plan、项目 capability、governance/task validators 全部 PASS。
- [x] 文档、性能审查、回滚路径、证据边界和本地交付已记录。

# Task Package Checklists
## TP-01
- [x] canonical origin/default branch/license/core paths/limitations 已绑定当前 revision。
- Verify: 实际 checkout Git/tree/license inspection。
- Gate: 11 个来源事实无推断补齐。

## TP-02
- [x] 单一 registry 驱动 15 源同步与 lock，回归和文档已同步。
- Verify: `bash tests/test_sync_upstreams.sh`。
- Gate: 集合精确、拒绝路径不退化。

## TP-03
- [x] 真实 15 源同步、幂等 digest、性能证据、门禁和本地提交完成。
- Verify: sync twice、项目/治理/任务 validators、post-commit smoke。
- Gate: 当前输入无 BLOCK 且工作树 clean。
