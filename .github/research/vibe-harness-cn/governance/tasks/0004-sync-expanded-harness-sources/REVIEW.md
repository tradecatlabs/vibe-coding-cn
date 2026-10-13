# Review: 十一项 Harness 扩容审查

## Scope

- `target`: merge_gate
- `review_depth`: deep
- `selected_profiles`: agent-harness,architecture,build-release,concurrency,correctness,future-optimal-drift,harness-quality,operability,performance,ponytail-complexity,reliability,repo-hygiene,security,test-quality
- `specialized_routes`: agent-harness-runtime,knowledge-assets-zone,document-drift,completion-verification
- `files`: 15 源 registry/lock、同步器、集合与状态机回归、研究/治理/任务文档和目录自述
- `base`: `7ed56ad9b384eaad9618202bd7c194e42ac88469`
- `review mode`: 主 Codex 自审；只证明本地确定性门禁，不冒充外部独立 reviewer provenance

## Verdict

- `decision`: PASS
- `summary`: 未发现剩余 BLOCK/WARN。11 个新增来源与用户清单一一对应，最终 15 源由既有单一 registry 驱动；checkout、lock、许可证和源码边界已绑定实际 revision。审查中发现的可见性枚举概念分裂已收敛为统一 Harness core 状态并重新验证。

## Fixed Finding

### RV-001：按产品形态分裂核心源码可见性枚举

- `severity`: WARN（已修复）
- `confidence`: high
- `evidence`: Claude Code 使用 `public-repository-without-cli-core-source`，初版 OpenHands 条目另增 `public-repository-without-agent-core-source`。
- `impact`: 每出现一种 Harness 产品形态都可能新增枚举，令控制面类型系统围绕供应商命名增长，而不是表达稳定治理事实。
- `minimal fix`: 统一为 `public-repository-without-harness-core-source`；CLI 与 Agent Canvas 的具体边界保留在 revision-bound limitation。
- `verification`: registry parse、15 源精确集合回归、连续 lock 重算、六类项目 capability 与原则扫描均 PASS。

## Correctness And Source Boundaries

- 11 个新增 official origin、登记分支、当前 HEAD、工作树 clean 状态和 lock 一致；最终集合恰好 15 个唯一名称/URL。
- Pi、Goose、Kimi 使用当前 canonical 组织或仓库；旧来源只作为迁移说明，不进入同步集合。
- 13 个 checkout 具有登记的核心源码路径；Claude Code 与 OpenHands 使用 revision-bound manual negative assessment，不从公开插件、客户端或独立 SDK 推断缺失核心。
- Crush 当前许可证为 FSL-1.1-MIT，Future License 不被误写为当前 MIT；DeepSeek preview、OpenClaw sandbox 默认关闭等限制继续绑定 lock。

## Reliability And Security

- 复用现有 `git`/`timeout`/`flock` 状态机：原子首次 clone、每源超时、单进程互斥、origin/branch/dirty/detached/non-FF fail closed。
- 上游内容只作为不可信研究输入；本轮没有运行、构建、安装或测试上游代码，没有读取凭据。
- 同步是逐仓库 fail-fast 而非 15 仓库事务：中途失败会非零退出且不刷新 lock，后续一致性检查可检测 mixed checkout；本轮完整同步成功。若未来失败率成为实际运营问题，再以测量决定是否引入 staging transaction。
- checkout 和 verification runtime 均由 Git ignore 保护，不进入本项目提交。

## Performance Audit

- `Complexity`: registry 处理为时间/空间 `O(S)`；同步和 lock 生成约为 `O(B + F)`，其中 `S=15`、`B` 为 clone/fetch 字节、`F=89,448` 个 tracked files；登记 core files 共 `12,686`。
- `Hot path`: GitHub 网络、磁盘写入和 `git ls-files`；JSON 解析与集合校验不是瓶颈。
- `Evidence`: 新增 11 源首次拉取约 140 秒，首次完整 15 源同步约 82 秒；checkout 总量约 2.6 GiB；冻结 registry/revision 后两次 lock SHA-256 均为 `90ea55f6fa0f4ba14443fa3cfaf7df7f2640e540ff1cfbe26a516eb48d615512`。
- `Decision`: 立即保留 depth=1、串行 fail-fast 与每源 300 秒上限。单轮样本不能证明并发净收益；重复测量 p95 超过明确预算后，再测试小规模有界并发，并同时测错误率、GitHub 限流、峰值带宽和磁盘压力。
- `Tradeoff`: 当前串行耗时较高但失败位置和本地状态清晰；无界并发会放大网络、磁盘和远端限流风险，不值得仅为一次同步增加协调所有权面。

## Principle And Document Review

- `Ponytail`: 复用现有静态 JSON、Bash、Python 标准库和系统 Git；没有新增依赖、服务、数据库、插件框架或第二同步器。Lean already. Ship.
- `Future-Optimal`: 终态仍是单一 official source registry 驱动 checkout/lock；本轮删除了按产品形态增长的错误枚举，没有引入兼容壳或双清单。
- `Document drift`: README、根/局部 AGENTS、研究基线、领域模型、项目操作模型、research module context 和既有 ADR 已同步；工具命令未改变，`TOOLCHAIN_MODEL.md` 无需改写。
- `Test quality`: 15 源精确集合、唯一 URL、许可证/可见性关键边界及既有原子 clone、互斥、dirty/ignored、wrong branch/origin、non-FF 拒绝路径均有可运行回归。

## Audit Case Consumption

- `CASE-0003 task-closeout-status-drift`: 实际命中；完成声明前必须统一 TODO、STATUS、验收清单、INDEX，并通过 closeout validator。本 REVIEW 生成时任务仍保持 In Progress，不提前声称 closeout PASS。
- `CASE-0004/0005/0006/0007`: 路由返回 `matched_signals` 为空，且本任务无量化研究、专业回测、交互回调或可选运行依赖，均为 N/A。

## Unknowns And Evidence Boundary

- 没有远端、CI、PR 或外部 reviewer provenance；PASS 只表示本地确定性审查。
- `shellcheck` 当前未作为项目 capability；已有 `bash -n`、离线 Git 状态机回归和真实 checkout 证据覆盖本次改动边界。
- 上游未来可能改变 HEAD、默认分支、许可证、目录或产品定位；registry/lock 的 revision 绑定会使旧结论失效，但不会自动完成新的人工负面评估。

## Gate Checklist

- [x] correctness：11 个新增来源与用户清单、checkout、registry、lock 一致。
- [x] reliability：原子 clone、超时、互斥、现场保护、FF-only 和失败非零未退化。
- [x] security：只允许 official GitHub HTTPS、相对路径、无上游执行、无凭据。
- [x] architecture：单一 registry 驱动 15 源，没有第二真相源或运行时扩权。
- [x] performance：复杂度、89,448 文件、2.6 GiB 与 140/82 秒实测已记录；无证据不并发。
- [x] Ponytail/Future-Optimal：错误可见性枚举已删除，最低技术阶梯和升级触发明确。
- [x] test-quality：精确集合和 Git 拒绝路径回归通过。
- [x] document drift：长期真相源和目录自述同步，runtime adapter 与研究 checkout 概念分离。
- [x] repo hygiene：上游 checkout/runtime ignored，diff check 与 secret gate PASS。

## Required Post-Commit Verification

- 在最终提交后的 clean HEAD 上重跑 15 源离线回归、六类 project capability、governance strict/health 和 Task Verification Plan。
- Task Verification 只有 owner-derived input digest、stored result 与 fresh reexecution 一致时才能 PASS。
- 无 remote 时只形成本地 commit，不声称已 push、PR、CI 或生产就绪。
