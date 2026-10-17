# Web3/EVM 供应链候选表

检索截面：`2026-08-14`。本表由 `web3-supply-chain-candidates.json` 生成，请勿手工编辑。

评分是本项目的选型判断，不是上游官方声明，也不代表已完成本地能力验证。

| 状态 | 候选 | 类别 | 角色 | 接口 / 输出 | 网络副作用 | 许可 | 分数 | 主要门禁 |
|---|---|---|---|---|---|---|---:|---|
| mvp | [Halmos](https://github.com/a16z/halmos) | formal-verification | Solidity 符号执行（Foundry 测试为 spec） | CLI, Foundry 测试兼容 / 反例, 路径结果, 覆盖结果 | none | Apache-2.0 | 21/25 | 路径爆炸；需要精确 spec |
| mvp | [Medusa](https://github.com/crytic/medusa) | fuzzing-property | 并行属性模糊测试器（Foundry 兼容） | CLI, JSON 配置, Foundry 集成 / 失败序列, 覆盖率, 属性结果 | none | Apache-2.0 | 21/25 | 成熟度低于 Echidna；文档较少 |
| mvp | [Aderyn](https://github.com/cyfrin/aderyn) | static-analysis | Solidity 快速静态分析（Rust，低误报目标） | CLI, 报告输出 / 检测报告, 严重度分级 | none | GPL-3.0 | 19/25 | 规则覆盖面较新；误报率未在本项目基线 |
| mvp | [solc-select](https://github.com/crytic/solc-select) | toolchain-stdlib | Solidity 编译器多版本管理（与 Slither/Echidna 配套） | CLI / 版本列表 | none | AGPL-3.0 | 18/25 | 无独立风险 |
| mvp | [Solodit (Cyfrin)](https://solodit.cyfrin.io/) | vulnerability-intel | 审计发现数据库（漏洞模式、报告检索 API） | REST API, Web / 漏洞模式 JSON, 报告条目 | data-only | 商业 API（部分内容公开） | 17/25 | 商业 API 条款；需要密钥管理 |
| pilot | [Foundry (forge/cast/anvil)](https://github.com/foundry-rs/foundry) | static-analysis | EVM 构建、测试、模糊测试与本地链（forge test/fuzz、cast、anvil） | CLI, Solc 兼容, JSON 输出 / 测试报告, 覆盖报告, trace, RPC 日志 | none | Apache-2.0 | 25/25 | 需固定 nightly/release 版本；规则依赖 solc 版本 |
| pilot | [Damn Vulnerable DeFi v4](https://github.com/theredguild/damn-vulnerable-defi) | benchmarks-labs | 本地 DeFi 已知漏洞靶场（Foundry，ground truth 来源） | Foundry 工程, 测试断言 / 测试失败/通过, POC 脚本 | none | MIT | 23/25 | 需固定版本；漏洞清单需人工对账 |
| pilot | [Forge-std](https://github.com/foundry-rs/forge-std) | toolchain-stdlib | Foundry 测试标准库（断言、作弊码、事件、控制台） | Solidity library / 测试断言结果 | none | MIT OR Apache-2.0 | 23/25 | 无独立风险 |
| pilot | [Slither](https://github.com/crytic/slither) | static-analysis | Solidity 静态分析候选漏洞生成器（数据流/污点分析） | CLI, JSON output / 检测结果 JSON, IR 中间表示 | none | AGPL-3.0 | 23/25 | 误报消解需独立验证；依赖 solc 精确版本 |
| pilot | [Echidna](https://github.com/crytic/echidna) | fuzzing-property | Solidity 属性模糊测试与不变量验证 | CLI, EVM 模式, crytic-compile 集成 / 失败序列, 覆盖报告, 属性结果 | none | AGPL-3.0 | 22/25 | 配置门槛；复杂状态空间耗时 |
| reference | [SWC Registry](https://github.com/SmartContractSecurity/SWC-registry) | intelligence-standards | 智能合约弱点分类标准（SWC-101..） | Markdown/JSON / 分类条目 | data-only | MIT | 19/25 | 部分条目过时，需对照实际模式 |
| reference | [Hardhat](https://github.com/NomicFoundation/hardhat) | toolchain-stdlib | EVM 开发框架（备选执行面） | CLI, Node API / 测试报告, 部署记录 | none | MIT | 18/25 | 与 Foundry 职责重叠 |
| reference | [Mythril](https://github.com/ConsenSysDiligence/mythril) | formal-verification | EVM 字节码符号执行与漏洞检测 | CLI, JSON 输出, MythX 生态 / 检测结果 JSON, 执行 trace | none | MIT | 18/25 | 维护放缓；路径爆炸 |
| reference | [OpenZeppelin Contracts](https://github.com/OpenZeppelin/openzeppelin-contracts) | intelligence-standards | 安全合约基线参考与依赖审计基准 | Solidity library / 无 | none | MIT | 18/25 | 仅参考 |
| reference | [DeFiHackLabs](https://github.com/SunWeb3Sec/DeFiHackLabs) | benchmarks-labs | 真实 DeFi 漏洞事件复现库（历史攻击 POC） | Foundry 工程, 文档 / POC 测试, 时间线 | none | Apache-2.0 | 17/25 | 质量参差；依赖版本旧 |
| reference | [Ethernaut](https://github.com/OpenZeppelin/ethernaut) | benchmarks-labs | Solidity CTF 靶场（本地可跑，训练与工具评估） | Web, 合约 / 完成状态 | none | AGPL-3.0 | 17/25 | 与 DeFi 业务漏洞重叠度低 |
| reference | [Pyrometer](https://github.com/nascentxyz/pyrometer) | static-analysis | Solidity 静态分析（Rust 实现，SIF 框架） | CLI, JSON 输出 / 检测结果 JSON | none | Apache-2.0（文件级复核） | 16/25 | 较新、无正式 release；社区与文档薄 |
| reference | [4naly3er](https://github.com/Picodes/4naly3er) | static-analysis | C4 审计报告脚手架与代码质量检查 | CLI / 审计报告模板, 检查清单 | none | GPL-3.0 | 14/25 | 仅报告层辅助 |
| reference | [Secureum](https://secureum.substack.com/) | intelligence-standards | 智能合约安全知识体系（RACE/MENTOR 课程资料） | 文章, 测验 / 无 | data-only | 公开内容 | 14/25 | 非机器接口 |
| hold | [Certora Prover](https://www.certora.com/) | formal-verification | EVM 形式化验证（规则证明） | CLI, 规则语言 / 证明/反例报告 | none | 商业 | 18/25 | 商业；远程执行；规则学习成本 |

## 汇总

- 总候选：20
- 状态：mvp=5，pilot=5，reference=9，hold=1
- 类别：benchmarks-labs=3，formal-verification=3，fuzzing-property=2，intelligence-standards=3，static-analysis=5，toolchain-stdlib=3，vulnerability-intel=1

## 状态语义

- `mvp`：允许进入本地隔离纵向样例；仍需固定版本和真实复跑。
- `pilot`：价值明确，但部署、许可、动作风险或运维成本需要先校准。
- `reference`：仅用于架构、方法、数据或评测研究，不进入默认执行工具面。
- `hold`：当前阻塞未闭合，不进入实施计划。
