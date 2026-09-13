---
id: GOV-STANDARDS-AGENTS
type: context
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
---

# Standards Guide

本目录保存跨任务长期生效的项目标准。任务证据留在 `governance/tasks/`，架构取舍留在 `governance/decisions/adr/`，可阻止交付的检查留在 `governance/architecture-gates/rules/`。

## 目录结构

```text
standards/
├── AGENTS.md                       # 标准目录职责、文件地图和维护边界
├── VIBE-MATHING-SPEC-v0.1.md        # 数学研究闭环的三条基本法则
├── POINT-LINE-FACE-BODY-METAMODEL-v0.1.md # 唯一概念元模型根、Face 与 Body 边界
├── FORMAL-METHODS-MAP.md            # 形式化方法主线与 Lean 二级地图
├── RESEARCH-LIFECYCLE-MODEL-v0.1.md # F05 中的 Project → Workflow → Task → Step → Job
├── Ponytail工程阶梯标准.md          # 新增所有权面的存在性判断
├── 未来最优解原则.md                # 从长期正确终态倒推迁移切片
├── 工程质量标准.md                  # 通用工程质量要求
├── 劣质代码定义.md                  # 不可接受的工程模式
└── 非功能性需求标准.md              # 性能、可靠性、安全等默认检查面
```

## 依赖与边界

- `VIBE-MATHING-SPEC-v0.1.md` 是研究闭环规范真相源；ADR-0000 解释决策，GATE-0002 和研究空间校验器执行准入。
- `POINT-LINE-FACE-BODY-METAMODEL-v0.1.md` 是唯一概念元模型根；它定义 Point、Line、F01–F13、reference-only Body、PWTSJ/OSPS 定位和跨面非传播规则，但不宣称相关 runtime 已实现。
- `FORMAL-METHODS-MAP.md` 是方法层主线和 Lean 定位的教学/路由地图；它不替代对象 schema、tool registry 或数学证据。
- `RESEARCH-LIFECYCLE-MODEL-v0.1.md` 是 F05 过程面内 Project → Workflow → Task → Step → Job 的生命周期模型；它不宣称已有通用调度器或新增持久化层级。
- 标准只定义长期规则，不保存任务状态、运行输出或临时研究结论。
- 新增或修改标准后必须重建治理索引，并运行 governance strict/health 与相关项目测试。
