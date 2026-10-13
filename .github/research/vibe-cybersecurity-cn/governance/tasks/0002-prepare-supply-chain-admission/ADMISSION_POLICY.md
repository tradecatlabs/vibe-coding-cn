# 供应链准入政策

## 状态机

```text
researched
  -> admission-candidate
  -> pinned
  -> verified
  -> admitted
  -> suspended / retired
```

- `admission-candidate`：进入准入检查队列，默认禁用。
- `pinned`：已固定 release/commit/schema/data snapshot 和 digest，但尚未证明可安全运行。
- `verified`：许可、来源、安全、接口、隔离、行为与回滚证据全部闭合。
- `admitted`：允许进入项目供应链，但不代表具体任务可以运行。
- `suspended/retired`：安全通告、许可、接口漂移或证据过期后退出执行面。

具体任务是否启用由运行时 `ScopeGrant`、策略和预算共同决定，不属于供应链目录状态，避免供应链 owner 越权批准网络动作。

禁止从研究状态直接跳到 `admitted` 或 `enabled`。

## 八个正式门禁

1. `license_review`：按固定制品检查 LICENSE、NOTICE、规则、数据和再分发边界。
2. `immutable_pin`：固定 release、commit、OCI digest、schema 或数据快照。
3. `integrity_verification`：验证 checksum、签名、Sigstore bundle 或等价来源证明。
4. `security_review`：检查上游 advisory、安装脚本、运行时下载、插件和高权限入口。
5. `interface_contract`：固定 CLI/API、输入输出 schema、错误码、超时和产物大小。
6. `isolation_policy`：定义文件、网络、凭据、权限、速率、目标和资源边界。
7. `behavior_test`：在本地 fixture/靶场执行正例、边界和 fail-closed 负例。
8. `rollback_test`：证明可以停用、移除固定制品并保留既有证据。

`research_source=pass` 只表示 0001 已用官方或原始来源完成研究，不计入上述八个正式门禁。

## 波次

- `W0`：先固定标准、信任根和情报数据契约。
- `W1`：再纳入无主动网络动作的本地只读分析工具。
- `W2`：只在隔离 Juice Shop 靶场打通 Web 候选—验证闭环。
- `W3`：在核心闭环证明后，再扩大综合扫描和攻击面发现能力。

## 硬边界

- 准入候选不触发下载、安装、镜像拉取、远程 API 或扫描。
- 正式纳入不等于默认启用；启用必须绑定具体任务、授权范围和预算。
- 扫描器只能产生 `Observation` 或 `CandidateFinding`，不能自行写入实证漏洞。
- engine、模板/规则、插件和漏洞数据库分别固定、分别失效。
- 任何安全通告、许可变化、签名失败或接口漂移都使既有验证失效并转为 `suspended`。

## 本轮终态与天花板

本轮只建立准入队列和机械门禁，不选择具体版本，也不运行候选。下一步从 `W0` 开始逐项固定 artifact；只有 `W0` 形成可信来源与数据契约后，才进入 `W1/W2` 的真实复跑。
