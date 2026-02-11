# 输入 / 输出 / 目录命名规范

## 输入字段

- **required**
  - `project_root` (默认 `~/project`)
  - `docs_root` (默认 `~/project/docs`)
  - `output_mode` ∈ {`direct_write`,`patch_diff`,`full_files`}，默认 `patch_diff`
  - `truthfulness_mode`，默认 `strict`
- **optional**
  - `scope_hint`：聚焦模块/目录提示
  - `change_type` ∈ {`baseline`,`feature`,`bugfix`,`refactor`,`release`}
  - `related_paths`：受影响路径列表
  - `prefer_priority`：文档优先级顺序
  - `enforce_docs_index`：是否强制维护 docs/README.md
  - `use_git_diff`：true 时优先以 git diff 定位
  - `max_doc_size_kb`：单文档体积上限（默认 200KB）
  - `style` ∈ {`concise`,`standard`,`verbose`}

## 输出固定顺序

1) 文档盘点表  
2) 生成/更新计划  
3) 逐文件创建/更新内容（遵循 output_mode）  
4) 变更摘要  
5) 一致性检查清单

## 目录与命名

```
docs/
├── architecture/
├── features/
├── integrations/
├── guides/
├── incidents/
└── archive/
```

- ADR：`docs/architecture/adr-YYYYMMDD-<kebab>.md`
- PRD：`docs/features/prd-<kebab>.md`
- Spec：`docs/features/spec-<kebab>.md`
- Integration：`docs/integrations/<kebab-service>.md`
- Guide：`docs/guides/<kebab-topic>.md`
- Incident：`docs/incidents/incident-YYYYMMDD-<kebab>.md`
- Archive：`docs/archive/YYYY/<orig-or-topic>.md`（原处留指向）

## 每个文档必备结构

- Purpose（目的）
- Scope（适用范围）
- Status（Active/Draft/Deprecated）
- Evidence（代码/配置/命令路径）
- Related（交叉链接或路径）
- Changelog（含最后更新时间 + 变更摘要）

## 质量门禁速查

- 五段交付结构齐全，顺序正确。
- 所有关键事实附证据路径；缺失用【待确认】+验证指引。
- guides / integrations 优先生成，且 integrations 含可验证步骤（curl/脚本）。
- 超限文档拆分；无权限时使用 patch/full_files 仍可落地。
