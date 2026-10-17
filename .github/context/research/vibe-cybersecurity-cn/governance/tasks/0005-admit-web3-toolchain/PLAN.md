# Planning Summary

把 0004 的"固定版本+隔离运行"升级为"正式准入+强制验证"：
5 项核心工具 8 门禁全过（admitted）、forge-std 固定 v1.16.2、
Echidna 属性覆盖 4 漏洞、验证控制面从 shadow 转 enforce。

# Lifecycle Gates

`SPEC -> PLAN -> BUILD -> TEST -> REVIEW -> SHIP`，任一 gate 不得跳过。

# Simplest Path

- 复用 0002 准入模型，新建指向 0004 源的 Web3 准入 JSON + 校验器。
- forge-std 旧目录备份后重装固定 tag。
- 属性合约只写 wrapper + 不变量，不引入新框架。
- git init + 一次初始提交（不 push），policy 改 enforce。

# Split Strategy

- TP-01：Web3 工具 8 门禁准入（JSON + 校验器 + 表）。
- TP-02：forge-std v1.16.2 固定重装。
- TP-03：Echidna 属性基线 4 漏洞全覆盖。
- TP-04：git 初始化 + 验证控制面 enforce + closeout 全绿。
- TP-05：治理同步与 closeout。

# Execution Waves

```text
TP-02 -> TP-03 -> TP-01 -> TP-04 -> TP-05
```

（TP-01 的 behavior_test 证据依赖 TP-02/TP-03 先完成。）

# Runtime Workflow Contract

- Allowed：本地工具安装/运行、文件编辑、git init/初始提交、校验命令。
- Forbidden：push、PR、切换分支、破坏性 git、公网目标。
- Evidence：门禁检查表、属性反例输出、git status/log、closeout 包。
- Stop：门禁证据缺失、验证控制面强制门禁失败且无法定位。

# Next Executable Leaves

- TP-02：forge-std 固定重装。

# Dependency Graph

```text
0004 工具链/靶场/证据
        |
        v
TP-02 forge-std 固定 --> TP-03 属性基线 --> TP-01 8门禁准入 --> TP-04 验证控制面 --> TP-05 治理
```

# Rollback Protocol

- 删除 `0005` 目录与 `web3-admission-*` 资产；恢复 lib/forge-std 备份。
- git：删除 `.git` 即回到非仓库状态（工作区文件不变）。
- 无远端、无部署状态需要迁移。
