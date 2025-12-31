---
name: canvas-dev
description: "Canvas白板驱动开发技能：从代码生成架构白板、根据白板生成代码、校验白板与代码一致性。使用场景：接手新项目快速理解架构、新功能开发先画白板再编码、架构重构可视化、团队协作共享架构图。"
---

# canvas-dev Skill

Canvas白板驱动开发：图形是第一公民，代码是白板的序列化形式。通过 Obsidian Canvas 实现人类与AI的共享工作区。

## When to Use This Skill

触发条件（满足任一即可）：
- 需要快速理解现有项目架构（接手遗留代码）
- 新功能开发前需要设计架构（先画后写）
- 架构重构需要可视化依赖关系
- Code Review 需要全局视角
- 团队协作需要共享架构图
- 需要生成 Obsidian Canvas 格式的 `.canvas` 文件

## Not For / Boundaries

此技能不适用于：
- 纯文本文档生成（使用 Markdown 即可）
- 流程图/时序图（使用 Mermaid）
- 数据库 ER 图（使用专用工具）
- 不需要双向同步的静态架构图

必要输入（缺失时需询问）：
1. 项目代码路径或代码片段
2. 分析粒度（file/class/service）
3. 技术栈（用于生成代码时）

## Quick Reference

### Canvas JSON 基础结构

```json
{
  "nodes": [
    {"id": "n1", "type": "text", "x": 0, "y": 0, "width": 200, "height": 100, "text": "# ModuleName\n- method1()\n- method2()"}
  ],
  "edges": [
    {"id": "e1", "fromNode": "n1", "toNode": "n2", "fromSide": "right", "toSide": "left", "label": "调用"}
  ]
}
```

### 节点类型

| type | 用途 | 示例 |
|:---|:---|:---|
| `text` | 模块/类/文件 | `{"type": "text", "text": "# UserService"}` |
| `group` | 功能分组 | `{"type": "group", "label": "API层"}` |
| `file` | 链接文件 | `{"type": "file", "file": "src/user.py"}` |

### 连线方向

| fromSide/toSide | 含义 |
|:---|:---|
| `right` → `left` | 水平调用（推荐） |
| `bottom` → `top` | 垂直依赖 |
| `top` → `bottom` | 继承关系 |

### 常用 label 标注

- `调用` - 函数/方法调用
- `依赖` - import/require
- `继承` - extends/implements
- `数据流` - 参数传递
- `FK: field` - 外键关系

### 分层布局约定

```
x轴: -400 (前端) → 0 (API) → 400 (服务) → 800 (数据)
y轴: 每层内按功能分组，间距 120-150
```

### 颜色编码（Obsidian Canvas）

| color | 含义 |
|:---|:---|
| `1` | 红色 - 缓存/热点 |
| `2` | 橙色 - 消息队列 |
| `3` | 黄色 - 上游依赖 |
| `4` | 绿色 - 数据库 |
| `5` | 蓝色 - 搜索/外部服务 |
| `6` | 紫色 - 注释/设计决策 |

## Rules & Constraints

### MUST（必须遵守）

- 节点 `id` 必须唯一且有意义（如 `svc-user`，非 `node1`）
- 连线必须反映真实的代码依赖关系
- 生成的 `.canvas` 文件必须是合法 JSON
- 白板修改后必须同步更新相关代码

### SHOULD（强烈建议）

- 按功能域分组（API层/服务层/数据层）
- 节点 text 使用 Markdown 格式（`# 标题` + 列表）
- 保持布局整洁（对齐、等间距）
- 为复杂依赖添加 label 说明

### NEVER（禁止）

- 不要生成与代码不一致的白板
- 不要在白板中包含敏感信息（密钥/密码）
- 不要创建循环依赖的连线（除非代码确实如此）

## Examples

### Example 1: 从代码生成架构白板

**Input:**
```
项目路径: /home/user/my-api
技术栈: Python FastAPI
粒度: file
```

**Steps:**
1. 扫描项目目录，识别 `.py` 文件
2. 分析 `import` 语句提取依赖关系
3. 识别 FastAPI 路由、数据库模型、外部调用
4. 按三层架构布局节点
5. 生成 `.canvas` JSON

**Expected Output:**
```json
{
  "nodes": [
    {"id": "api-user", "type": "text", "x": -200, "y": 0, "width": 200, "height": 100, "text": "# user_router.py\n- POST /users\n- GET /users/{id}"},
    {"id": "svc-user", "type": "text", "x": 100, "y": 0, "width": 200, "height": 100, "text": "# user_service.py\n- create_user()\n- get_user()"},
    {"id": "model-user", "type": "text", "x": 400, "y": 0, "width": 200, "height": 100, "text": "# user_model.py\n- User\n- id, name, email"}
  ],
  "edges": [
    {"id": "e1", "fromNode": "api-user", "toNode": "svc-user", "fromSide": "right", "toSide": "left", "label": "调用"},
    {"id": "e2", "fromNode": "svc-user", "toNode": "model-user", "fromSide": "right", "toSide": "left", "label": "操作"}
  ]
}
```

### Example 2: 根据白板生成代码

**Input:**
```
Canvas JSON: (包含 UserAPI → UserService → UserModel 的白板)
技术栈: Python FastAPI + SQLAlchemy
目标目录: /home/user/new-project
```

**Steps:**
1. 解析节点 → 生成文件/类
2. 解析连线 → 生成 import 和调用
3. 按技术栈最佳实践填充代码

**Expected Output:**
```python
# user_router.py
from fastapi import APIRouter
from .user_service import UserService

router = APIRouter()
service = UserService()

@router.post("/users")
def create_user(data: dict):
    return service.create_user(data)
```

### Example 3: 白板与代码一致性检查

**Input:**
```
Canvas: architecture.canvas
项目: /home/user/my-project
```

**Steps:**
1. 提取白板节点列表
2. 扫描项目文件列表
3. 对比差异

**Expected Output:**
```
🔴 严重不一致:
- 白板缺失: payment_service.py (代码存在但白板未记录)
- 错误连线: UserService → Database (代码中无直接调用)

🟢 覆盖率: 85%

📋 修复建议:
1. 在白板添加 payment_service 节点
2. 删除 UserService → Database 连线，改为 UserService → UserRepository → Database
```

## FAQ

**Q: 为什么选择 Obsidian Canvas 而不是其他工具？**
- A: Obsidian Canvas 是免费开源的，`.canvas` 文件是纯 JSON 格式，AI 可以直接读写，支持双向同步。

**Q: 白板粒度选 file 还是 class？**
- A: 小项目（<20文件）选 file，大项目选 class 或 service。关键是保持白板可读性。

**Q: 如何处理循环依赖？**
- A: 如果代码确实存在循环依赖，在白板中如实标注，并添加注释节点说明这是技术债务。

## Troubleshooting

| 症状 | 可能原因 | 解决方案 |
|:---|:---|:---|
| Obsidian 无法打开 .canvas | JSON 格式错误 | 用 `jq .` 验证 JSON |
| 节点重叠 | x/y 坐标冲突 | 调整布局，保持 200+ 间距 |
| 连线不显示 | fromNode/toNode id 错误 | 检查节点 id 是否匹配 |
| AI 生成代码与白板不符 | 白板描述不够具体 | 在节点 text 中添加更多细节 |

## References

- `references/index.md` - 导航索引
- `references/canvas-json-spec.md` - Canvas JSON 完整规范
- `references/workflow-guide.md` - 完整工作流指南
- `references/prompts.md` - 提示词集合

外部资源：
- [Obsidian Canvas 官方文档](https://obsidian.md/canvas)
- [Canvas白板驱动开发详解](../../documents/02-方法论/图形化AI协作-Canvas白板驱动开发.md)
- [Canvas开发工作流](../../workflow/canvas-dev/README.md)

## Maintenance

- Sources: Obsidian Canvas 官方文档 + 本地工作流实践
- Last updated: 2026-01-01
- Known limits: 仅支持 Obsidian Canvas 格式，不支持其他白板工具

## Quality Gate

发布前检查：
1. ✅ `description` 包含具体触发关键词
2. ✅ "When to Use" 列出可判定的触发条件
3. ✅ "Not For / Boundaries" 明确边界
4. ✅ Quick Reference <= 20 个模式
5. ✅ >= 3 个可复现的示例
6. ✅ 长内容放入 `references/`
7. ✅ 无虚构内容，不确定处标注验证路径
