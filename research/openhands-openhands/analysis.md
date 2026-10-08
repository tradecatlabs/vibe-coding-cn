# OpenHands/OpenHands 研究分析

## 本轮结论

当前 `OpenHands/OpenHands` 的 README 将项目定位为 Agent Canvas：一个自托管的开发者控制中心，可以连接 OpenHands、Claude Code、Codex、Gemini 或 ACP 兼容 Agent，并在本地、Docker、虚拟机和云环境之间切换。它的研究价值是展示“Agent 编排层”和“具体 Agent”可以分离。

## 本地证据

- `raw/github-readme.raw.md.txt`：Agent Canvas、后端切换、自动化、ACP、sandbox 和本地运行方式。
- `raw/repository/src/api/`：Agent Server、workspace、Git 和后端适配。
- `raw/repository/src/hooks/`、`src/stores/`、`src/routes/`：前端任务状态和配置。
- `raw/repository/docs/architecture.md`：系统结构说明。
- `raw/repository/docs/ACP_AGENTS.md`：ACP Agent 接入边界。
- `raw/repository/tests/` 与 `__tests__/`：UI、API 和状态行为测试。

## 对标拆解

| 项 | 内容 |
|:---|:---|
| 参考对象 | `OpenHands/OpenHands` |
| 它解决的核心问题 | 让多个 Agent 后端在统一控制中心中运行、切换、自动化和管理工作区 |
| 核心机制 | Agent Canvas、Agent Server、backend registry、workspace、ACP、automation 和 Git 服务 |
| 真正带来结果的动作 | 把 Agent 运行环境、会话状态和外部服务接入从单个 Agent 中抽离 |
| 可迁移做法 | 运行环境分层、后端适配、任务状态、工作区边界和自动化触发 |
| 不可迁移条件 | 不把自托管平台、云服务和多仓系统当成本仓教程的默认复杂度 |
| 下一步试用动作 | 为本仓研究刷新任务写一个“事实获取 -> 判断 -> 下沉”的可恢复任务状态表 |

## 改良迭代

| 改良目标 | 本仓版本 | 验证指标 |
|:---|:---|:---|
| 后端与任务分离 | 研究对象事实拉取与判断文档分离 | raw 失败不会伪装成分析成功 |
| 工作区边界 | raw repository 只作本地缓存，主仓只提交事实摘要 | Git 状态和证据来源可审计 |
| 自动化触发 | 用 Make 目标和脚本承载重复研究动作 | 相同参数能重跑且失败非零 |
| 人机接管 | 把动态事实、权限和发布动作保留人工确认 | 高风险操作不会隐式执行 |

## 可迁移清单

- 把 Agent、workspace、backend 和 automation 视为不同责任边界。
- 为长任务保存状态、恢复入口和当前工作区。
- 对外部 Agent 采用适配层，不把某个供应商 API 写死在知识库核心。
- 为自托管或本地执行明确宿主机权限风险。

## 不可迁移清单

- 不复制完整 Agent Canvas、Agent Server 或商业云架构。
- 不把容器存在等同于完全安全；挂载目录和密钥仍需审查。
- 不因多后端可接入就默认启用多 Agent 并行。

## 验证动作

| 动作 | 成功信号 | 失败信号 |
|:---|:---|:---|
| 断网刷新一个研究对象 | 任务明确失败并保留旧事实日期 | 使用旧数据却显示为最新 |
| 重新运行同一研究脚本 | raw 更新幂等、sources 可追溯 | 重复创建目录或覆盖未知文件 |
| 模拟 Agent 后端不可用 | UI/文档能说明降级和恢复 | 把配置缺失吞成空结果 |

## 沉淀判断

“模型/Agent、Harness、工作区和自动化是不同层”适合下沉到 `docs/gongfa/`；OpenHands 的平台部署、ACP 和商业服务细节继续保留在研究域。
