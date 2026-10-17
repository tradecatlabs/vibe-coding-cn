# audit/ — S0 审计管线骨架（M1）

职责：把「公开协议仓库 -> 固定 commit -> 编译 -> 候选 -> 测试空跑 -> 证据」
编译为一条可重跑、可纠错的本地管线。只处理 Foundry 工程（M1 范围）；
Hardhat/Node 路径在 Node v22 环境验证后扩展（见 `COMBAT_READINESS.md` P1）。

## 用法

```bash
# 本地独立克隆（推荐，避免重复拉取；工作树必须干净才允许切换 commit）
audit/run.sh --path .sandbox/s0-targets/euler-vault-kit \
  --commit bfb325a6e6ca09613d940b46f72ccfe017353933

# 直接按 URL 拉取（自动固定 commit + submodule）
audit/run.sh --repo https://github.com/euler-xyz/euler-vault-kit --commit <sha>

# 输出根与测试过滤
audit/run.sh --path <dir> --commit <sha> --out audit/out --test-match 'test_addIgnored'
```

## 产物

```text
audit/out/run-<时间戳>/
├── evidence.json      # 机器可读证据摘要（commit/工具版本/计数/测试摘要）
├── slither.json       # Slither 结构化候选（detectors 列表）
├── forge-test.log     # forge test 原始输出
└── out/               # Foundry 编译产物（ABI/bytecode，隔离在运行目录）
```

## 设计约束

- 幂等：每次运行生成独立 `run-<时间戳>` 目录，不覆盖旧证据。
- 安全：`--path` 仅接受干净工作树（避免覆盖用户改动）；`--repo` 使用独立 workspace。
- 失败即非零退出；slither 异常时保留日志并标记 `slither_failed`，不吞错。
- 目标响应、工具输出一律视为数据；管线本身不产生任何链上或网络副作用。

## 验收（M1）

- [x] EVK `forge build` 编译成功（321 个 artifact，2026-09-02）
- [x] `--path` 本地克隆路径全链路（build -> slither 198 候选 -> test 3 passed）
- [x] `--repo` 克隆路径全链路（blob:none -> 固定 commit -> submodule -> 同上）
- [x] Slither 结构化 JSON 产出（success=true；退出码 255 为已知清理阶段异常，见下）
- [x] forge test 空跑与日志归档
- [x] 证据摘要（commit/工具版本/计数）与运行时产物隔离（audit/out 不入库）
- [ ] 完整测试套件跑通（M2：含 fuzz/invariant 与耗时预算）
- [ ] Hardhat/Node 路径（M2/M3）

## 已知问题

- slither 0.11.6 在 EVK 上完成分析并写出完整 JSON 后以 255 退出
  （crytic-compile 清理/重编译阶段异常，日志尾部可见 `forge build --build-info` 卡住）。
  脚本以 `slither_success=true` 判定候选有效并记录 warning；M2 建议排查
  是否与 FOUNDRY_OUT 隔离或 crytic-compile 版本有关。
