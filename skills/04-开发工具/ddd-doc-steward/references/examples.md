# 场景示例（可直接套用）

## 示例 1：空仓库快速落地
- 输入：
```json
{
  "project_root": "~/project",
  "docs_root": "~/project/docs",
  "output_mode": "patch_diff",
  "change_type": "baseline",
  "scope_hint": "docs 为空",
  "use_git_diff": false
}
```
- 操作：
  1. A：`tree -L 2 docs` 为空 → 记录证据。
  2. B：盘点表全部标记“缺失”；计划新增 docs/README.md、guides/getting-started.md、development-workflow.md、integrations/<待确认>.md。
  3. C：输出补丁，命令/端口/变量均标【待确认】，并说明从 `.env` / `docker-compose` / 配置目录查证。
  4. D：摘要列出新增文件；检查清单提示需补全端口/env/API 证据。
- 预期：可直接应用的 diff；无臆测字段；每文含 Changelog。

## 示例 2：功能迭代—登录与刷新
- 输入：
```json
{
  "project_root": "~/project",
  "docs_root": "~/project/docs",
  "output_mode": "patch_diff",
  "truthfulness_mode": "strict",
  "change_type": "feature",
  "scope_hint": "auth 登录 & token 刷新",
  "related_paths": ["services/api/auth", "services/api/routes"],
  "use_git_diff": true
}
```
- 操作：
  1. A：`git diff --name-only` 聚焦 auth 路由/控制器；提取请求/响应字段与错误码。
  2. B：盘点表标识 features/prd-auth-login.md、spec-auth-login.md 缺失；integrations/auth-api.md 疑似过期（字段不一致）。
  3. C：新增 PRD/Spec；更新 integrations 文档含鉴权方式、错误码、验证 curl；token TTL 等未证实字段标【待确认】并指向配置文件。
  4. D：摘要列出新增/更新；检查清单包含“对照 auth/config 复核 TTL、错误码”。
- 预期：diff 覆盖 3 个文件；所有事实有路径；待确认项附验证方法。

## 示例 3：无法读取仓库的降级
- 输入：自然语言 “帮我生成 SSOT 文档模板”。
- 操作：
  1. 归一化 JSON，声明“无法真实扫描，进入 strict 模板模式”。
  2. 盘点表说明证据缺口（目录树/README/依赖/配置/API 位置缺失）。
  3. 计划仅生成模板；待确认清单列出需用户补充的命令与文件。
  4. 输出 full_files：六大目录的骨架文档，字段均标【待确认】+ 如何获取。
  5. 检查清单提示下一步需用户提供证据。
- 预期：完整可落盘模板，不含任何凭空事实。
