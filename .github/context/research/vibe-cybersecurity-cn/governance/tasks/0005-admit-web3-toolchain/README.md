# Task Overview

- Task ID: `0005`
- Slug: `admit-web3-toolchain`
- Objective: Web3 工具链 8 门禁准入、Echidna 属性基线全覆盖、验证控制面升级为强制门禁。
- Status: `In Progress`

## In Scope

- Foundry / Slither / Echidna / solc(solc-select) / forge-std 完成 8 门禁正式准入（admitted）。
- forge-std 固定到 v1.16.2（重新安装固定 tag）。
- Echidna 属性测试扩展到全部 4 个靶场漏洞（重入、溢出、访问控制、预言机操纵）。
- 验证控制面升级：git init + 初始提交、policy 转 enforce、closeout 全门禁通过。
- 治理同步与 closeout。

## Out of Scope

- 不推送任何 Git 远端、不开 PR。
- 不接入公网目标、不安装额外新工具（超出 5 项核心工具）。
- 不修改 0004 已 closeout 的机器真相源语义（可补充证据）。

## Task Package Tree

```text
ROOT
├── TP-01 Web3 工具链 8 门禁准入
├── TP-02 forge-std 固定版本
├── TP-03 Echidna 属性基线全覆盖
├── TP-04 验证控制面升级与强制门禁
└── TP-05 治理同步与 closeout
```

## Requirement Alignment

- 用户要求"工具链相关补齐到 100%"：从固定版本+隔离运行升级到正式准入与强制验证。
- 项目操作模型：`admitted` 要求不可变版本和全部正式门禁通过。
- 验证控制面：多叶子任务自动强制 verification plan，需要 git 输入摘要基线。

## Reading Order

1. `CONTEXT.md`
2. `ADMISSION_TABLE.md`
3. `PLAN.md`
4. `STATUS.md`

## Task Package Overview

| Node | Output | Acceptance |
|---|---|---|
| TP-01 | `web3-admission-candidates.json`、`ADMISSION_TABLE.md` | 5 项 admitted，校验器 PASS |
| TP-02 | `web3-lab/lib/forge-std` v1.16.2 | forge build/test 4/4 |
| TP-03 | 4 份 Echidna 反例证据 | 属性覆盖 4 漏洞 |
| TP-04 | git 基线 + enforce 验证 | closeout gate ready |
| TP-05 | 治理同步与 closeout | strict/health 通过 |
