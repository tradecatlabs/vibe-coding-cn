# Repo Evidence

- 项目操作模型已定义 `ScopeGrant -> CandidateFinding -> ValidationRun -> Evidence -> Finding`。
- 任务 0001 保存 46 项代表性候选，分为八类；任务 0002 保存其中 18 项准入候选，0 admitted。
- 当前无业务运行时、已安装扫描器、生产入口或外部目标授权。
- 既有研究已证明工具目录丰富，但尚缺一个统一坐标系说明覆盖、空白和产品位置。

# Constraints Matrix

| 约束 | 强制决策 |
|---|---|
| 框架职责不同 | NIST、ATT&CK、OWASP、CVE/CWE/CVSS 等分层使用，不压成单一排名 |
| 动态版本会演进 | 记录检索截面和官方链接，文档设置 P90D 复核周期 |
| 候选不是能力 | 只写 research coverage，不写 installed、verified 或 production-ready |
| 全局不等于全做 | 明确直接建设、对接和禁止自治三类边界 |
| 不能重复事实 | 工具详情继续引用 0001，不在本任务复制逐工具许可和接口 |
| 无授权主动动作 | 本轮只读网页和本地文档，不运行安全工具 |

# Change Boundary

修改长期景观、一个架构 ADR、任务 0003 证据和相关入口/索引；不改变 0001/0002 机器真相源、
不创建业务代码、不触碰外部系统。

# Risk Matrix

| 风险 | 影响 | 控制 |
|---|---|---|
| 把市场术语当架构事实 | 未来按产品名堆系统 | 以资产、行为、生命周期、证据为稳定坐标 |
| 把候选覆盖当运行能力 | 错误完成声明 | 明确 research-only 与 0 admitted |
| 景观太大导致范围膨胀 | 首个纵向样例失焦 | 空白默认对接或延后，以消费者触发扩展 |
| 标准版本过时 | 决策依据漂移 | 时点、官方来源、review_cycle 和复核入口 |
| 主动安全内容越界 | 非授权副作用 | 文档研究限定；不扫描、不安装、不利用 |

# Assumptions and Falsification

- 假设：四轴足以为后续产品和供应链决策定位；若后续任务无法唯一映射到资产、行为、防御和证据，扩展坐标而非增加营销分类。
- 假设：薄证据控制面是长期正确边界；若本地 ground truth 表明独立验证无法提高事实质量，重新评估 ADR。
- 假设：现有八类可完整解释 46 项候选；通过目录计数检查验证。
- 推翻条件：官方标准发生不兼容重大更新、项目核心对象变化，或运行实验否定候选—实证分离。

# Critical Ambiguities

- 法律和合规具有司法辖区差异；本任务只给技术景观，不给法律结论。
- 市场类别重叠且持续改名；使用责任边界，不声称市场分类穷尽。
- AI/Agent 与 OT 的专项标准仍快速发展；当前只标出域和安全边界。

# Debug Evidence Contract

- 调试模式: `Optional`
- 本任务没有程序缺陷修复；失败由任务文档、治理链接、索引或严格健康检查非零退出暴露。

# Task Package Context Map

- TP-01：`SOURCE_LEDGER.md`、`TASK_INTENT.json`
- TP-02：`governance/context/CYBERSECURITY_LANDSCAPE.md`、ADR-0001
- TP-03：`LANDSCAPE_COVERAGE.md`、0001 机器目录分类计数
- TP-04：项目入口、索引、`REVIEW.md` 和校验输出
