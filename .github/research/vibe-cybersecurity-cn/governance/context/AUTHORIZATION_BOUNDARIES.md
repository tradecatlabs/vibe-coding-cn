---
id: GOV-AUTHORIZATION-BOUNDARIES
type: context
status: current
owner: security-architecture
created: 2026-08-14
last_reviewed: 2026-08-14
review_cycle: P30D
---

# 授权边界（合规最宽松口径）

本文件是"什么动作需要授权"的唯一真相源。目标是零摩擦放行只读研究，
同时把硬门禁只保留在真正会改变目标状态或针对目标系统的主动交互上。

## 核心原则

1. **公开即研究输入**：公开协议源码、仓库与链上公开数据默认允许研究。
2. **只读默认放行**：不修改目标状态的读取、查询、分析和复现动作默认允许；
   只读 RPC 查询须遵守端点 ToS 与速率限制，凭据经凭据管理器注入。
3. **主动交互 fail closed**：发交易、状态修改、利用验证、主动扫描等会改变目标状态的动作，
   必须绑定真实授权来源；目标可达或"有响应"不构成授权。
4. **授权来源三通道**：自有资产声明、赏金项目规则、书面授权。

## 场景矩阵

| 场景 | 动作示例 | 需要 ScopeGrant | 依据 |
|---|---|---:|---|
| 公开协议源码 + 仓库 | clone、编译、静态分析、本地复现 | 否 | 代码公开即研究输入 |
| fork 主网区块只读分析 | `anvil --fork-url <rpc>`、只读调用、事件与状态分析 | 否 | 只读数据，无目标交互 |
| 链上主动交互 | 发交易、状态修改、利用验证、主动扫描 | 是 | 需自有资产/赏金/书面授权 |
| 自有资产 / 赏金范围 | 注册表内资产、bounty 规则覆盖的目标 | 是（一键导入） | 授权来源自动生成 ScopeGrant |

## ScopeGrant 草案（v1 字段契约）

```yaml
grant_id: string            # 唯一授权标识
source: self-owned | bounty | written   # 授权来源通道
grantee: string             # 执行主体（agent 标识）
scope:
  targets: [string]         # 网络 / 合约地址 / 仓库 URL
  networks: [string]        # 主网 / 测试网 / 本地
actions: [probe, transaction, state-change]  # 允许的动作等级
rate_limit: number          # 每秒请求上限
budget: number              # 最大成本（gas / 请求数）
stop_conditions: [string]   # 触发即停的条件
expires_at: string          # ISO 时间；过期自动失效
evidence_ref: string        # 授权证据引用（bounty 规则页 / 书面授权文件 / 资产注册表条目）
```

## 授权来源三通道

- **自有资产注册表**：声明所有权的资产一键生成 ScopeGrant（默认长期有效）。
- **赏金项目规则导入**：把平台项目范围自动转换为 ScopeGrant（按项目周期生效）。
- **书面授权**：扫描书面授权文件生成 ScopeGrant（按约定范围/期限生效）。

## 反模式（禁止）

- 无速率限制的扫描。
- 无停止条件的持续测试。
- 把"目标有响应 / 可 ping / 可 curl"当作授权来源。
- 用"Discovered Public Surface"等改名掩盖主动交互缺授权的事实。
- 用公开代码审计名义执行主动交互动作。
- 无界并发、无速率、无停止条件的主动动作。

## 与既有门禁的关系

- 只读研究默认放行；任何主动交互动作必须在运行时可审计地回溯到 ScopeGrant 与 evidence_ref。
- 目标"可达 / 有响应"不构成主动测试授权依据；无授权来源的主动动作 fail closed。
- 供应链 `admitted` 只表示工具就绪，不改变本文件的动作分级。
