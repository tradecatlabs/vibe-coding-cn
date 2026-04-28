---
name: ddd-doc-steward
description: "文档驱动开发（DDD）文档管家：以仓库真实证据为准，盘点 ~/project 与 docs 目录，生成/更新 SSOT 文档（计划→补丁/全文→摘要→一致性检查）。触发：需要让文档与代码/配置/运行方式同步、补齐 guides/integrations/features/architecture/incidents/archive、无法推导时标注【待确认】并给验证路径。"
---

# DDD 文档管家 Skill

让 `~/project/docs` 成为单一可信来源（SSOT）：先盘点、后计划、再增量写文档，所有事实有证据来源，没有证据就【待确认】。

## When to Use This Skill

- 需要为真实仓库建立/维护文档 SSOT，输出「盘点表 → 计划 → 文档补丁/全文 → 变更摘要 → 一致性检查」的固定交付物。
- 新增/改动功能、集成或事故复盘，需要同步更新 docs 下对应目录。
- 需要在 strict 模式下，避免任何臆测，所有关键事实必须给出代码/配置/命令的路径或说明验证方法。
- 只能获取部分信息时，仍需生成最小可落地模板并标注【待确认】。

## Not For / Boundaries

- 与工程无关的纯创作文案。
- 无法提供最小证据集（目录树、README/依赖/配置/路由位置）且不接受【待确认】输出时。
- 涉及密钥明文输出；文档中仅可写占位符与获取方式。
- 未提供 `project_root/docs_root/output_mode` 等输入时，先将自然语言归一到输入 JSON（参见快速参考）。

## Quick Reference

1) 归一化输入（缺省值）
```json
{
  "project_root": "~/project",
  "docs_root": "~/project/docs",
  "output_mode": "patch_diff",
  "truthfulness_mode": "strict",
  "change_type": "baseline",
  "scope_hint": null,
  "related_paths": [],
  "prefer_priority": ["guides","integrations","features","architecture","incidents","archive"],
  "enforce_docs_index": true,
  "use_git_diff": true,
  "max_doc_size_kb": 200,
  "style": "standard"
}
```

2) Phase A 扫描要点（证据链）
- `tree -L 3` 或目录枚举；`rg` 聚焦 README、依赖、配置、路由/API 定义。
- 记录证据路径清单（文件/命令），不写结论。

3) Phase B 先输出计划
- 《文档盘点表》：按六大目录标记「存在/缺失/疑似过期」，附证据路径。
- 《生成/更新计划》：新增/更新/待确认清单；理由=证据。

4) Phase C 生成文档（遵循 output_mode）
- `patch_diff` 推荐；无写权限时用 `full_files`。
- 每个文档必含 Purpose/Scope/Status/Evidence/Related/Changelog。
- 命名规范：ADR `architecture/adr-YYYYMMDD-<kebab>.md`；PRD/Spec/Integration/Guide/Incident/Archive 详见 `references/api.md`。

5) Phase D 收尾
- 变更摘要：每文件 3-8 条关键变化。
- 一致性检查：文档-代码验证点 + 未解的【待确认】与下一步。

6) 关键规则
- 真实性优先：无证据不写，写则附路径；敏感值用占位符。
- 没有就创建，有就增量更新，禁止大面积重写无关内容。
- 超过 `max_doc_size_kb` 拆分；缺少访问时生成模板并给证据采集命令。

## 规则 & 约束

- MUST：输出五段结构；严格遵守目录/命名规范；Changelog 每文必有；冲突以代码/配置为准。
- SHOULD：优先用 git diff/related_paths 聚焦；guides 与 integrations 先行；为每个【待确认】提供验证路径。
- NEVER：编造端口/环境变量/接口字段；输出密钥明文；跳过盘点直接写文档。

## Examples

### Example 1: 空仓库初始化
- 输入：`change_type=baseline`，docs 为空。
- 步骤：A 扫描→B 盘点表标记全部缺失→计划新增 docs/README.md、guides/getting-started.md 等→C 生成骨架补丁→D 摘要与检查。
- 验收：输出 patch diff，所有命令标【待确认】或给寻找路径。

### Example 2: 新增登录功能
- 输入：`change_type=feature`，`scope_hint="auth 登录"`，`use_git_diff=true`。
- 步骤：用 diff 找受影响路由；盘点 features/integrations；计划新增 PRD/Spec，更新 integrations/auth-api；标记 token 过期时间待确认。
- 验收：变更摘要指出新增文档与更新字段；检查清单含鉴权/错误码/验证 curl。

### Example 3: 无法读取仓库
- 输入：仅自然语言“帮我做 SSOT 文档”。
- 步骤：先归一化 JSON，声明“无法真实扫描”→生成六类文档模板，全量标【待确认】并列证据缺口与采集命令。
- 验收：输出 full_files；每条待确认可直接行动补证。

## FAQ

- Q: 没有写权限怎么办？  
  A: 将 `output_mode` 设为 `patch_diff` 或 `full_files`，给出可落盘内容。
- Q: 目录过大处理不过来？  
  A: 按 prefer_priority 分批；声明本次范围与剩余批次计划。

## References

- `references/index.md`：导航与长文入口。
- `references/getting_started.md`：DDD 文档管家流程与术语。
- `references/api.md`：输入/输出规范、目录命名与质量门禁。
- `references/examples.md`：可套用场景示例。
- `references/troubleshooting.md`：降级与故障处理。

## Maintenance

- 来源：提示词库（在线表格入口见 `assets/prompt/README.md`）；元技能 `assets/skills/auto-skill/`；自动化辅助工具 `assets/repos/Skill_Seekers-development`.
- 最后更新：2026-04-28
- 已知限制：依赖用户提供真实证据；大体量仓库需分批；不输出敏感值。

## 质量门禁（出厂前自检）

1. `name/description` 符合触发条件、目录名一致。
2. 五段交付结构齐全；每段内容可直接给人/脚本消费。
3. 每个文档含 Purpose/Scope/Status/Evidence/Related/Changelog。
4. 所有事实有证据路径；无证据标【待确认】且给验证路径。
5. Quick Reference ≤20 条且可直接执行；示例 ≥3。
6. 长文本放 `references/`，`references/index.md` 可导航。
7. 安全：不输出密钥明文，敏感值使用占位符。
