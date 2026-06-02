# 参考资料

## 字多不看

- 本目录回答“具体工程怎么组织、怎么选技术、怎么设置硬门禁”。
- 项目结构、Python 骨架、企业架构、Dataset First 已拆成独立模板。
- 质量门禁、常见坑、技术栈和底层逻辑作为查阅型参考文档维护。

## 快速导航

| 文档 | 定位 |
|:---|:---|
| <a id="reference-engineering-practice"></a>[工程实践总入口](project-architecture-template.md) | 项目架构、代码组织、开发经验、质量门禁与常见坑的入口。 |
| <a id="reference-engineering-practice-1-项目架构模板"></a>[项目架构模板](project-architecture-template.md) | 常见项目结构、架构设计原则、最低门禁和检查清单。 |
| <a id="reference-engineering-practice-通用-python-项目骨架"></a>[通用 Python 项目骨架](python-project-skeleton.md) | Python 应用、服务、脚本工具和库项目的通用骨架。 |
| <a id="reference-engineering-practice-enterprise-monorepo-multi-repo-reference-architecture-template"></a>[企业级 Monorepo / Multi-repo 架构模板](enterprise-architecture-template.md) | 中大型工程组织、平台工程和多产品线参考模型。 |
| <a id="reference-modern-enterprise-architecture-template"></a>[现代企业数字化平台架构](modern-enterprise-architecture-template.md) | 面向领域产品网络、微服务容器 GitOps 边界、AI 原生能力、微调治理、AI 事件响应、内部平台、数据产品、供应链安全、FinOps 成本治理、版本治理、版本控制面、基线迁移工作单、基线消费锁定文件、基线准入执行策略、基线撤销与隔离记录、基线发布事务回执、基线门禁执行报告、基线证据追踪图、基线会审裁决记录、基线 EOL 退役证书、基线状态对账报告、基线生命周期状态机、基线就绪评分卡、基线例外总账、基线回滚验证记录、基线通知确认总账、基线验证环境锁定、基线制品清单、基线发布证据、基线兼容性总账、基线采纳总账、基线支持矩阵、基线发布列车、基线符合性声明、外部标准版本锁定、可执行标准、执行控制面、门禁决策、RACI 决策权、可靠性分级、仓库拓扑、迁移弃用、审计证据、联邦治理和行业对标矩阵的完整说明文档。 |
| <a id="reference-engineering-practice-7-dataset-first-数据服务结构"></a>[Dataset First 数据服务结构](dataset-first-data-service.md) | 以 dataset、contract、registry、runtime 为核心的数据服务模板。 |
| <a id="reference-engineering-practice-2-代码组织"></a>[代码组织](code-organization.md) | 模块化、命名、注释、格式化、文档和工具。 |
| <a id="reference-engineering-practice-3-开发经验"></a>[开发经验](development-experience.md) | 变量名、文件结构、编码规范、架构原则和常见基础设施经验。 |
| <a id="quality-gates"></a>[AI 编程质量门禁与常见坑](quality-gates-and-pitfalls.md) | 系统提示词、强前置条件、常见坑和硬门禁。 |
| <a id="reference-engineering-practice-4-ai-编程质量门禁与常见坑"></a>[AI 编程质量门禁与常见坑](quality-gates-and-pitfalls.md) | 系统提示词、强前置条件、常见坑和硬门禁。 |
| <a id="reference-engineering-practice-5-底层程序逻辑设计与工程优化项"></a>[底层程序逻辑设计与工程优化项](low-level-program-logic.md) | 运行模型、并发模型、数据模型、性能模型和工程交付检查清单。 |
| <a id="reference-technology-stack"></a>[技术栈](technology-stack.md) | 技术栈选型、组合案例与学习路径。 |
| <a id="tech-stack-selection"></a>[如何选择技术栈](technology-stack.md) | 从目标、约束、团队能力、生态成熟度和长期维护评估方案。 |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

### 细粒度目录

- [工程实践总入口](project-architecture-template.md) - 项目架构、代码组织、开发经验、质量门禁与常见坑的入口。
- [项目架构模板](project-architecture-template.md) - 常见项目结构、架构设计原则、最低门禁和检查清单。
- [通用 Python 项目骨架](python-project-skeleton.md) - Python 应用、服务、脚本工具和库项目的通用骨架。
- [企业级 Monorepo / Multi-repo 架构模板](enterprise-architecture-template.md) - 中大型工程组织、平台工程和多产品线参考模型。
- [现代企业数字化平台架构](modern-enterprise-architecture-template.md) - 面向领域产品网络、微服务容器 GitOps 边界、AI 原生能力、微调治理、AI 事件响应、内部平台、数据产品、供应链安全、FinOps 成本治理、版本治理、版本控制面、基线迁移工作单、基线消费锁定文件、基线准入执行策略、基线撤销与隔离记录、基线发布事务回执、基线门禁执行报告、基线证据追踪图、基线会审裁决记录、基线 EOL 退役证书、基线状态对账报告、基线生命周期状态机、基线就绪评分卡、基线例外总账、基线回滚验证记录、基线通知确认总账、基线验证环境锁定、基线制品清单、基线发布证据、基线兼容性总账、基线采纳总账、基线支持矩阵、基线发布列车、基线符合性声明、外部标准版本锁定、可执行标准、执行控制面、门禁决策、RACI 决策权、可靠性分级、仓库拓扑、迁移弃用、审计证据、联邦治理和行业对标矩阵的完整说明文档。
- [Dataset First 数据服务结构](dataset-first-data-service.md) - 以 dataset、contract、registry、runtime 为核心的数据服务模板。
- [代码组织](code-organization.md) - 模块化、命名、注释、格式化、文档和工具。
- [开发经验](development-experience.md) - 变量名、文件结构、编码规范、架构原则和常见基础设施经验。
- [AI 编程质量门禁与常见坑](quality-gates-and-pitfalls.md) - 系统提示词、强前置条件、常见坑和硬门禁。
- [AI 编程质量门禁与常见坑](quality-gates-and-pitfalls.md) - 系统提示词、强前置条件、常见坑和硬门禁。
- [底层程序逻辑设计与工程优化项](low-level-program-logic.md) - 运行模型、并发模型、数据模型、性能模型和工程交付检查清单。
- [技术栈](technology-stack.md) - 技术栈选型、组合案例与学习路径。
- [如何选择技术栈](technology-stack.md) - 从目标、约束、团队能力、生态成熟度和长期维护评估方案。

</details>

## 使用方式

- 新项目先看项目架构模板，再根据语言或组织规模选择 Python 骨架或企业架构模板。
- AI 产出不稳定时，查质量门禁与常见坑。
- 技术选型、学习路线和组合案例进入技术栈。

## 正文

正文已拆分到上方独立文档；本 README 只保留索引、旧锚点兼容入口和阅读顺序。
