# 工程复盘（待外部 Review）

- status: `REQUIRES_EXTERNAL_REVIEW`
- risk: `high`
- canonical handoff: 未生成；不得由实现者自签。

## 做对了什么

- 先用真实 RED 证明伪 locator、伪 hash 与自报 `independent` 可污染解库，再取得同源 GREEN 与 counterfactual；证据见 `REGRESSION_EVIDENCE.json`。
- 把信任边界放在 registry、output policy、真实 artifact、现场 SHA-256 和 verifier receipt，而不是 Agent 自评；攻击矩阵覆盖路径逃逸、symlink、自验证、回执覆盖和输出篡改。
- 用 `flock + WAL + fsync + os.replace` 建立单机唯一 writer，并在锁内验证 Problem→Attempt→Result 完整性；并发、故障恢复与断链写入负例均通过。
- 没有因 `norm_num` 构建成功就接受隐式 `propext`；改用 `rfl` 后，Lean 4.33 实际输出“不依赖任何公理”。
- 深审发现伪 invalidation 与断链 writer 后先修复再重跑 100/100，没有沿用旧审计。

可复制条件：单机 Linux/WSL、可用 `fcntl`、明确 schema、固定 verifier policy、能提供确定性 fixture。多主机 writer、动态开放问题和外部人工 review 不适用。

## 做错了什么

- 初版验证器把摘要字段当成事实，导致不存在 artifact 也可晋升；根因是结构校验错误承担真实性校验职责。
- 初版 invalidation 在验证回执前生效；根因是先过滤再验证，漏检来自测试只覆盖合法失效记录。
- 初版 Store 只做单表 schema，直接调用可写断链记录；根因是跨表不变量只存在于离线 validator。
- 初次 Lean fixture 使用 `norm_num`，引入 `propext`；根因是把 kernel PASS 错当成零公理依赖，所幸 `#print axioms` 门禁及时发现。
- 最初尝试在 task closeout 之前构建 Completion Exemplar，被 owner 正确拒绝；根因是没有先检查 owner 工具的 bootstrap 顺序。

这些问题均为本轮首次发现，但“调用者声明替代派生事实”属于系统性风险，已由既有全局 CASE-0008 覆盖。

## 重新来一遍怎么做

1. 先冻结信任图：谁生成、谁验证、什么原始输出可重算、谁有撤销权；再写 schema 和代码。
2. 同时设计 accept 与 invalidation 的攻击矩阵，任何状态变化都必须由受信回执派生。
3. Store 第一天就验证最终三表快照，不把跨表完整性留给离线检查。
4. Lean fixture 从 `rfl`/最小 TCB 起步，固定 toolchain + manifest，并把 `#print axioms` 当独立 gate。
5. 执行前先运行 task closeout/asset/retro owner 的 requirement 与顺序检查，区分产品完成、Git 交付和外部 provenance。

验证方式：`pipeline_maturity_audit.py --strict` 必须保持 100/100；恢复任何旧漏洞时专项测试必须失败。

## 经验寿命

- 适用范围：单机证据驱动 agent runtime、JSONL 小规模事实源、CAS/proof assistant 垂直验证。
- 失效条件：迁移多主机 writer、替换证据格式/Lean 版本、引入外部 reviewer、改变 Problem/Attempt/Result 模型。
- 复查日期：2026-11-11。
- 晋升状态：Completion Exemplar candidate；单次成功不得晋升 active SOP。
