---
id: GOV-TOOLCHAIN-MODEL
type: context
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
---

# Toolchain Model

本文件记录项目工具链的当前真相，帮助人类和代理优先复用成熟能力、项目既有脚本和稳定验证入口。

## 成熟工具优先

- 优先使用语言标准工具、官方 CLI、包管理器、测试框架、lint/typecheck、数据库迁移工具和云平台能力。
- 自研脚本只用于连接、编排、适配和表达项目特有流程。
- 新增工具前必须证明：已有工具无法满足、引入后总拥有成本更低、验证和回滚路径明确。

## 项目命令

| 场景 | 命令 | 备注 |
|---|---|---|
| 安装依赖 | 无 | 当前校验器只使用 Python 标准库 |
| 候选目录校验 | `python3 governance/tasks/0001-survey-cybersecurity-supply-chain/validate_candidates.py` | 校验字段、来源、评分、风险决策并重建 Markdown 表 |
| 准入目录校验 | `python3 governance/tasks/0002-prepare-supply-chain-admission/validate_admission_candidates.py` | 跨目录校验研究血缘、准入状态、固定版本和八门禁并重建表 |
| Web3 候选校验 | `python3 governance/tasks/0004-web3-vertical-proof/validate_web3_candidates.py` | 校验 Web3/EVM 候选并重建 Markdown 表 |
| Web3 准入校验 | `python3 governance/tasks/0005-admit-web3-toolchain/validate_web3_admission.py` | 校验 9 门禁、固定版本并重建准入表 |
| 靶场证据校验 | `python3 web3-lab/validate_lab_evidence.py` | 校验 ground truth 与证据账本一致性、artifact 存在性 |
| Web3 构建与测试 | `export PATH="$HOME/.foundry/bin:$PATH"; cd web3-lab && forge build && forge test -vv` | Foundry 1.7.1 固定版本；仅本地 |
| Web3 静态候选 | `cd web3-lab && export PATH="../.venv-web3/bin:$PATH"; slither . --json <out> --solc-solcs-select 0.8.35` | Slither 0.11.6；候选不直接当实证 |
| Web3 属性模糊 | `web3-lab/../../.tools/echidna test/OverflowEchidna.t.sol --contract OverflowEchidna --config echidna.yaml` | Echidna 2.3.3；本地二进制 |
| 只读 fork 分析 | `anvil --fork-url <rpc> --fork-block-number <n>` | 只读研究默认放行；遵守端点 ToS 与速率；凭据经凭据管理器注入 |
| 验证门禁（test） | `bash web3-lab/verify_tests.sh` | 候选+证据+forge test 一键验证 |
| 验证门禁（coverage） | `bash web3-lab/verify_coverage.sh` | forge coverage 摘要 |
| 验证门禁（architecture） | `bash governance/tools/verify_architecture.sh` | 治理 strict + health |
| 治理校验 | `python3 governance/tools/validate_governance_package.py --project-root . --strict` | 校验治理结构、frontmatter 和内部链接 |
| 治理健康 | `python3 governance/tools/governance_health_report.py --project-root . --strict` | 检查占位、过期与待处理项 |
| 类型检查 | 不适用 | 尚无业务代码 |
| 构建 | `cd web3-lab && forge build` | Foundry 仅用于本地靶场 |
| 本地运行 | `cd web3-lab && forge test` | 仅本地链与本地合约；只读 fork 需单独声明 RPC |
| 发布 | 未定义 | 生产能力未实现，不得部署 |
| 回滚 | 普通文件回退 | 不依赖数据迁移或外部资源 |

## 候选工具采用边界

- `mvp` 表示值得进入本地隔离样例，不表示已安装、已验证或生产批准。
- `pilot` 必须先固定版本、校验来源、隔离运行并测量证据质量。
- `reference` 仅用于架构或方法研究，不进入默认执行工具面。
- `hold` 表示许可证、动作风险、复杂度或供应链条件尚未闭合。
- `admission-candidate` 只表示进入准入检查队列，不授予运行权。
- `admitted` 要求不可变版本和全部正式门禁通过；只读研究默认允许，
  主动交互能否运行由 `ScopeGrant` 和运行时策略决定，不写入供应链目录。
- Web3 工具链 5 项（Foundry/Slither/Echidna/solc-select/forge-std）已于 2026-08-14 完成 9 门禁 admitted。
- 任何工具升级都必须重新核对许可证、输出契约、规则/模板来源和安全默认值。

## 禁止或谨慎使用

- 禁止绕过项目已有脚本直接调用内部实现细节，除非在调试任务中明确说明。
- 禁止新增无 owner、无验证、无回滚说明的脚本。
- 禁止把一次性命令伪装成长期工具链。

## 工具链变更流程

1. 先检查现有命令、脚本、CI 和文档。
2. 记录新增或替换工具的存在性理由。
3. 更新本文件和相关流程文档。
4. 运行最小验证。
5. 在任务 closeout 中记录验证证据和回滚方式。
