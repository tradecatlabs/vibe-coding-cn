# Repo Evidence

- 0001 保存 46 项全局安全候选；0002 保存 18 项准入候选（0 admitted）；
  0003 结论是下一步做本地 ground-truth 纵向样例。
- 用户已确认范围：Web3/区块链；首个切片为 EVM/Solidity + 已授权源码 + 本地链。
- 本机网络可达 GitHub/PyPI/npm；具备 Docker/Node/Python，原先无 Web3 工具链。
- 本任务新装：Foundry 1.7.1（foundryup）、Slither 0.11.6（PyPI）、
  Echidna 2.3.3（GitHub release）、solc 0.8.35（solc-select）。

# Constraints Matrix

| 约束 | 强制决策 |
|---|---|
| 用户范围是 Web3 | 候选表按 EVM/Solidity 聚焦，不铺全局 |
| 静态分析有误报 | 候选与实证分离，验证必须独立复现 |
| 工具来自外部供应链 | 固定版本、记录来源与许可证、隔离运行 |
| 靶场是教学用途 | 明确 ground truth，禁止用于真实协议 |
| 无公网授权 | 所有执行绑定本地目录与本地链 |
| 不重复造轮子 | 复用 Foundry/Slither/Echidna，自研仅靶场与证据 |

# Change Boundary

新增 `governance/tasks/0004-web3-vertical-proof/` 与 `web3-lab/`；
更新操作模型、工具链模型、拓扑、路由、README/AGENTS 与任务索引。
不改变 0001/0002/0003 机器真相源，不触碰外部系统。

# Risk Matrix

| 风险 | 影响 | 控制 |
|---|---|---|
| 工具供应链不可信 | 恶意二进制/依赖 | 官方安装器、固定版本、来源与许可证记录 |
| 静态候选当实证 | 假阳性结论 | 只认独立攻击测试复现，证据账本强制分离 |
| 靶场合约泄漏 | 误用于真实协议 | ground truth 标注教学用途 |
| 外部动作越权 | 非授权副作用 | 全部动作限定本地；无公网 RPC |
| 版本漂移 | 证据不可复现 | 工具版本与命令写入证据账本 |

# Assumptions and Falsification

- 假设：EVM/Solidity 是 Web3 安全自动化的正确起点；若真实授权项目表明需要
  非 EVM 链或更复杂状态建模，扩展而非重写。
- 假设：多通道验证（静态+攻击测试+属性模糊）能覆盖单工具漏报；若后续基准显示
  三通道仍漏报某类漏洞，增加通道或规则集。
- 假设：本地靶场召回率可以外推到真实协议；推翻条件：真实协议上工具组合
  无法找到任何已知漏洞或误报率不可控。

# Critical Ambiguities

- 真实授权协议尚未确定；本轮用本地靶场证明链路，授权对象由用户后续指定。
- Echidna 属性 spec 只覆盖 EXP-02；完整属性基线是后续任务。
- 工具正式准入（8 门禁）不在本任务范围；本任务只固定版本并隔离运行。

# Debug Evidence Contract

- 调试模式: `Optional`
- 本任务不是缺陷修复任务；失败由校验器非零退出、测试失败或证据账本不一致暴露。

# Task Package Context Map

- TP-01：`web3-supply-chain-candidates.json`、`validate_web3_candidates.py`
- TP-02：工具版本与来源记录（`web3-lab/README.md` 工具表）
- TP-03：`web3-lab/src/`、`web3-lab/test/`、`web3-lab/ground-truth.json`
- TP-04：`web3-lab/evidence/`、`validate_lab_evidence.py`
- TP-05：治理上下文、`STATUS.md`、`REVIEW.md`、校验输出
