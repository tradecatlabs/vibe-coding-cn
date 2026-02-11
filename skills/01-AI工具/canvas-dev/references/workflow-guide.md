# Canvas 白板驱动开发工作流指南

## 核心理念

```
传统开发：代码 → 口头沟通 → 脑补架构 → 代码失控
Canvas方式：代码 ⇄ 白板 ⇄ AI ⇄ 人类（白板为单一真相源）
```

**图形是第一公民，代码是白板的序列化形式。**

## 工具准备

1. **Obsidian** - 免费开源白板工具
   - 下载: https://obsidian.md/download
   - 启用 Canvas 功能（默认已启用）

2. **AI 助手** - Claude/GPT-4
   - 需支持读取 Canvas JSON 格式
   - 推荐使用 Claude Code 或 Codex CLI

## 完整工作流

### Phase 1: 生成架构白板

**场景**: 接手新项目，快速理解架构

```
1. 提供项目代码路径给 AI
2. 使用架构分析提示词
3. AI 生成 .canvas 文件
4. 用 Obsidian 打开查看
```

**提示词模板**:
```
分析 {PROJECT_PATH} 项目，生成 Obsidian Canvas 架构白板。
粒度: {file/class/service}
重点关注: API路由、数据库模型、外部服务调用
```

### Phase 2: 人工优化白板

**场景**: 调整自动生成的白板

```
1. 拖动节点调整布局
2. 补充遗漏的依赖连线
3. 添加注释节点标注设计决策
4. 删除错误的连接
```

**布局原则**:
- 按功能分层（前端 → API → 服务 → 数据）
- 同层节点垂直对齐
- 保持连线不交叉

### Phase 3: 白板驱动编码

**场景**: 新功能开发

```
1. 在白板上画出新模块框
2. 添加预期的调用连线
3. 导出白板 JSON 发给 AI
4. AI 根据白板生成代码
```

**提示词模板**:
```
根据以下 Canvas 白板生成代码:
{CANVAS_JSON}

技术栈: {TECH_STACK}
目标目录: {TARGET_DIR}
```

### Phase 4: 白板驱动重构

**场景**: 架构调整

```
1. 在白板上删除/重连依赖线
2. 标注需要拆分的大模块
3. 发送修改后的白板给 AI
4. AI 生成重构代码
```

**提示词模板**:
```
白板已更新，请对比新旧版本重构代码:
旧白板: {OLD_CANVAS}
新白板: {NEW_CANVAS}
只输出需要修改的文件
```

### Phase 5: 一致性检查

**场景**: PR/MR 合并前

```
1. 运行一致性检查脚本
2. 对比白板节点与实际文件
3. 修复不一致之处
4. 优先修正白板（白板是事实来源）
```

## 场景速查

| 场景 | 操作 | 提示词关键词 |
|:---|:---|:---|
| 接手新项目 | 生成白板 | "分析项目，生成架构白板" |
| 新功能开发 | 画白板 → 生成代码 | "按这个白板实现代码" |
| 架构重构 | 改白板 → 重构代码 | "按新白板重构" |
| Code Review | 看白板全局 | "检查这条调用链" |
| 团队协作 | 共享白板 | "指着白板讲" |

## 最佳实践

### DO ✅

- 每次代码变更后更新白板
- 用颜色区分不同类型的模块
- 为复杂依赖添加 label 说明
- 定期运行一致性检查

### DON'T ❌

- 不要让白板与代码长期不同步
- 不要在白板中包含敏感信息
- 不要创建过于复杂的白板（拆分为多个）
- 不要忽略循环依赖警告

## 与其他工具集成

### CI/CD 集成

```yaml
# .github/workflows/canvas-check.yml
name: Canvas Sync Check
on:
  pull_request:
    paths: ['**.py', '**.canvas']
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/canvas_sync_check.py
```

### VS Code 集成

1. 安装 Obsidian 插件
2. 配置 `.canvas` 文件关联
3. 使用 Claude Code 读取白板

## 相关资源

- [Canvas白板驱动开发详解](../../../documents/02-方法论/图形化AI协作-Canvas白板驱动开发.md)
- [架构分析提示词](../../../workflow/canvas-dev/prompts/01-架构分析.md)
- [白板驱动编码提示词](../../../workflow/canvas-dev/prompts/02-白板驱动编码.md)
- [白板同步检查提示词](../../../workflow/canvas-dev/prompts/03-白板同步检查.md)
