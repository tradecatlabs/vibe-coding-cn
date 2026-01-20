---
name: sop-generator
description: "标准作业程序（SOP）生成与规范化：将输入资料/需求/历史记录整理为可执行 SOP（结构化章节、步骤、控制点、异常处理、记录）。当用户要求“写 SOP/作业指导书/操作规程/流程说明”，或给出零散资料需要“整理成 SOP/流程”，或要求“按标准结构输出 SOP/质量检查”时使用。"
---

# sop-generator Skill

将碎片化资料与需求，转化为**可执行、可审核、可复用**的 SOP 文档，并输出统一结构与质量检查。

## When to Use This Skill

触发条件（满足任一即可）：
- 明确要求：写 SOP / 标准作业程序 / 作业指导书 / 操作规程 / 流程说明
- 给出零散记录、聊天日志、需求清单，要求“整理成 SOP/流程”
- 要求“统一结构、含关键控制点/异常处理/记录表”的过程文档

## Not For / Boundaries

- 不替代**法律/医疗/高危工艺**的强制合规文件（需专业审核）
- 不凭空编造组织内部流程；缺失信息必须**显式追问**
- 不输出“只有结论、没有步骤”的说明书

## 必要输入（缺失则先问 1-3 个关键问题）

1. 目标与范围：SOP 解决什么问题？适用于谁/哪些场景？
2. 关键产出：最终产物/结果是什么？验收标准如何定义？
3. 资源与约束：必需工具、系统权限、合规要求、时限/成本

## 工作流（高层步骤）

1. **拆解任务边界**：识别是否存在多个主题（需要拆分多份 SOP）
2. **抽取操作链路**：把目标拆成“输入 → 动作 → 输出”的步骤序列
3. **标注控制点**：关键参数/质量阈值/安全风险
4. **补齐异常处理**：偏离标准时的应对与升级路径
5. **结构化输出**：按统一模板生成 SOP
6. **质量自检**：完整性、可执行性、可追溯性

## 输出结构（统一模板）

```
SOP 标题 / 文档编号
版本与修订记录
编制/审核/批准

1. 目的（Purpose）
2. 适用范围（Scope）
3. 术语与定义（Definitions）
4. 角色与职责（Roles & Responsibilities）
5. 资源与前置条件（Resources/Prerequisites）
6. 标准作业步骤（Procedure）
   6.1 步骤 1（输入/动作/输出/耗时）
   6.2 步骤 2 ...
7. 关键控制点与质量标准（Critical Control Points）
8. 安全与风险提示（Safety/Risk）
9. 异常处理与升级路径（Deviations/Escalation）
10. 记录与表单（Records）
11. 相关文件/参考资料（References）
```

## Quick Reference

### Pattern 1: 一句话拆分判断
```text
如果输入里出现 >=2 个互不相关的目标/对象/系统，则拆分为多份 SOP；否则合并为一份并在范围中声明。
```

### Pattern 2: 最小可行 SOP（MVP）
```text
目的 + 范围 + 资源 + 3-7 步骤 + 关键控制点 + 异常处理 + 记录
```

### Pattern 3: 步骤写法模板
```text
步骤N：在[系统/地点]使用[工具]执行[动作]，输入为[输入]，输出为[输出]，耗时/阈值为[参数]。
```

### Pattern 4: 缺失信息快速追问
```text
请补充：1) 适用范围/角色 2) 关键产出与验收标准 3) 必需工具/系统权限
```

### Pattern 5: 一键生成 SOP 模板（脚本）
```text
python i18n/zh/skills/00-元技能/sop-generator/scripts/generate_sop.py --title "项目上线 SOP" --doc-id "SOP-001" --version "v1.0" --output sop.md
```

### Pattern 6: 生成最小可行 SOP（MVP）
```text
python i18n/zh/skills/00-元技能/sop-generator/scripts/generate_sop.py --title "巡检 SOP" --mvp --output sop-mvp.md
```

## 规则与约束

- MUST：步骤必须可执行、可复现；关键控制点必须量化
- SHOULD：每个步骤都包含输入/动作/输出；异常处理明确负责人
- NEVER：用“自行判断/视情况而定”替代关键步骤

## Examples

### Example 1：从杂乱记录生成 SOP（多主题拆分）

- Input（节选）：
  - “SOP 的定义、SOP 标准结构”
  - “mac 截屏到剪贴板快捷键”
  - “obs 同时推流 2 平台”
- Steps：
  1) 识别为 3 个主题 → 拆分 3 份 SOP  
  2) 每份按模板输出，并在范围里声明适用平台  
  3) 对缺失信息（如 OS 版本/软件版本）提出追问  
- Expected output / acceptance：
  - 3 份独立 SOP；每份含步骤、控制点、异常处理

### Example 2：需求驱动 SOP（六爻因子生成）

- Input：
  - 目标：用“六爻”作为唯一占卜流派  
  - 输出：方向、强度、置信、周期、原始卦象字段、解释  
  - 约束：不涉及个人八字  
- Steps：
  1) 明确适用范围：仅物品/交易对/商品  
  2) 设计步骤链：采集对象 → 起卦 → 解析 → 量化映射  
  3) 定义关键控制点：字段一致性、量化尺度  
- Expected output / acceptance：
  - SOP 中包含字段定义表、量化公式/区间、异常处理（如数据不足）

### Example 3：基于仓库资料生成 SOP（项目试玩/运行）

- Input：
  - GitHub 仓库：BloopAI/vibe-kanban  
  - 目标：快速试玩项目  
- Steps：
  1) 读取 README → 提取运行前置条件  
  2) 输出“本地启动 SOP”：安装依赖、配置密钥、启动命令  
  3) 标注关键控制点：API Key 必填、依赖管理工具  
- Expected output / acceptance：
  - 1 份“本地运行 SOP”，包含最少步骤与失败处理

## References

- `references/index.md`：导航与索引  
- `references/sop-foundations.md`：SOP 定义与核心特征  
- `references/sop-structure.md`：通用结构与章节说明  
- `references/writing-style.md`：写作与可执行性规范  
- `references/repo-vibe-kanban.md`：vibe-kanban 仓库摘要  
- `references/examples.md`：长样例与原始输入片段

## Assets & Scripts

- `assets/sop-template.md`：全量 SOP 模板
- `assets/sop-mvp.md`：最小可行 SOP 模板
- `assets/record-log-template.md`：记录表模板
- `scripts/generate_sop.py`：模板生成脚本（支持全量/MVP）

## Maintenance

- Sources: 官方/权威 SOP 资料 + 仓库 README（见 references）
- Last updated: 2026-01-20
- Known limits: 需按具体行业/合规要求补充细则

## Quality Gate

1. `description` 可触发且包含关键词（SOP/作业指导书/操作规程）
2. 有明确的输入缺口追问策略
3. 输出结构包含控制点/异常处理/记录
4. 至少 3 个可复现示例
5. 参考资料独立拆分且可导航
