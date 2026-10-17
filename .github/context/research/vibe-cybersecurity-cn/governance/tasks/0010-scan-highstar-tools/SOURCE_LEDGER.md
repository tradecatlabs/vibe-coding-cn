# 来源账本：0010 扫描与目标拉取

## S-A：Euler Vault Kit（S0 目标）

| 字段 | 值 |
|---|---|
| URL | `https://github.com/euler-xyz/euler-vault-kit` |
| commit | `bfb325a6e6ca09613d940b46f72ccfe017353933` |
| 沙盒路径 | `.sandbox/s0-targets/euler-vault-kit/` |
| 工程类型 | 纯 Foundry（foundry.toml + lib + src + test + certora + medusa.json） |
| 规模 | src 62 sol / test 126 sol / audits 11 份专业审计 PDF |
| submodule | forge-std b6a506d / OZ e682c7e / permit2 cc56ad0 / EVC 084b322 |
| 用途 | M1 管线骨架验证 + 与 11 份公开审计报告做对照样本 |

## S-B：GitHub 高 star 工具扫描

| 字段 | 值 |
|---|---|
| 时间 | 2026-09-02 |
| 方式 | `gh api search/repositories`（认证账号，search API 30 req/min） |
| 查询数 | 12 组（见 SCAN_REPORT.md） |
| 新增候选 | 14 条 reference 级，写入 0001 `supply-chain-candidates.json` |
| 证据 | 每条候选均记录 star 截面、许可、upstream URL |

## 边界确认

- 扫描仅访问 GitHub 公开元数据；未对任何第三方目标发起探测。
- 全部新增条目 disposition=reference：未做逐工具代码审计，不进入自动执行面。
