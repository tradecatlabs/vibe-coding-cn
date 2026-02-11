# 快速开始 & 术语表

## 使命

让 `~/project/docs` 成为单一可信来源（SSOT）：先盘点、先计划、增量更新，所有事实可追溯。

## 最短落地路径

1. **收集最小证据集**：`tree -L 3`、README、依赖清单、主要配置（.env*/yaml/toml/docker/k8s）、路由/API 定义位置、最近 git diff。
2. **归一化输入**：把用户自然语言转成 JSON（见 `SKILL.md` 快速参考），缺省 `output_mode=patch_diff`、`truthfulness_mode=strict`。
3. **执行 A→D 流程**：A 扫描→B 盘点与计划→C 生成文档（按 output_mode）→D 变更摘要与一致性检查。
4. **落盘或回传**：有写权用 direct_write；否则输出 patch/full_files 供用户应用。

## 核心术语

- **SSOT**：Single Source of Truth，docs 与代码/配置/运行方式一致。
- **output_mode**：`direct_write`（直接写）、`patch_diff`（推荐）、`full_files`（无法写入时）。
- **truthfulness_mode=strict**：无证据不写；写则附路径或命令；敏感值用占位符。
- **prefer_priority**：默认 `guides > integrations > features > architecture > incidents > archive`。
- **enforce_docs_index**：true 时必须维护 `docs/README.md` 导航。
- **Evidence**：文件路径、命令输出、日志位置；每个关键事实都需来源。
- **【待确认】**：无法推导的字段，需附验证路径（文件/命令/负责人）。
- **max_doc_size_kb**：单文档建议体积，超限应拆分。

## 自动化采集（可选）

- 需要批量抓取外部文档/代码仓库时，可用 `libs/external/Skill_Seekers-development` 的 CLI（如 `skill-seekers scrape --config <config.json>`）生成参考素材，再按本技能流程落盘。

## 交付物检查

- 五段结构齐全；每文含 Purpose/Scope/Status/Evidence/Related/Changelog；所有事实有证据或【待确认】。
