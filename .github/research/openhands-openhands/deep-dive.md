# OpenHands/OpenHands 深度研究

## 研究级别

- 当前级别：L2 源码/结构深度研究。
- 研究对象：`OpenHands/OpenHands`。
- 证据来源：本目录 `raw/` 下的官方 README、架构文档、源码与测试。
- 观察日期：2026-09-08。

## L2 结论

当前仓库的关键变化是从单一开发 Agent 产品界面向 Agent Canvas 控制中心演进。Canvas 负责连接多个 Agent Server、后端和自动化；Agent Server/SDK 负责会话与执行；workspace、Git 和 secrets 负责环境边界。这种分层使“谁决定做什么”和“在哪里执行”可以独立变化。

## 源码证据

- `raw/repository/README.md`：本地、Docker、VM、云后端和 ACP Agent 的公开定位。
- `raw/repository/src/api/agent-server-adapter.ts`：Canvas 与 Agent Server 的适配边界。
- `raw/repository/src/api/backend-registry/`：后端注册、健康和会话相关状态。
- `raw/repository/src/api/workspaces-service/`、`src/api/git-service/`：工作区和 Git 接口。
- `raw/repository/src/hooks/mutation/`、`src/hooks/query/`：前端任务、配置、插件和状态读写。
- `raw/repository/docs/architecture.md`：架构分层与组件关系。
- `raw/repository/docs/ACP_AGENTS.md`：ACP Agent 的接入与贡献边界。
- `raw/repository/src/api/no-direct-agent-server-calls.test.ts`：通过测试约束调用边界的样本。

## 关键机制

### Agent 与控制中心分离

Canvas 并不需要知道每个 Agent 的内部推理；它只需维护连接、会话、后端和用户操作。这让 Codex、Claude Code 等不同执行器可以通过适配层接入。

### 工作区是显式资源

Agent 要改代码，必须有 workspace、Git 和文件权限。把它们作为 API/状态对象管理，比把宿主机路径隐式塞进 prompt 更可审计。

### 自动化是独立触发面

README 提到按计划或 webhook 触发自动化。自动化因此需要独立的调度、权限、重复执行和历史记录，不应与一次手工对话混为一谈。

### 测试约束架构边界

`no-direct-agent-server-calls.test.ts` 这类测试把“调用必须经过适配层”变成可执行约束，说明架构原则只有进入测试才不会随着迭代漂移。

## 可迁移模式

- 将本仓研究拉取、事实抽取、判断更新和索引同步拆成不同动作。
- 让每个动作写入可追踪产物，并能从失败位置恢复。
- 对外部工具使用适配文档和来源登记，不把工具实现混入知识层。
- 把目录职责、链接关系和 raw 隔离写成结构检查。

## 不可迁移条件

- 本仓不需要 Agent Server、前端控制中心或多租户后端。
- 本地 raw 快照不能作为生产工作区；它只保存研究证据。
- Docker/VM 隔离的安全边界必须结合实际配置验证，不能仅凭产品定位下结论。

## 验证计划

用本仓一次 `fetch-research-raw` 任务做映射：检查 source、raw、domain、analysis、索引五个节点是否有明确输入输出；人为让一个网络请求失败，验证旧事实不会被标记为新事实；恢复网络后再次运行，验证只更新受影响节点。
