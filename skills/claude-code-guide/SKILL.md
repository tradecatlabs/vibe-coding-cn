---
name: claude-code-guide
description: Claude Code 高级开发指南 - 全面的中文教程，涵盖工具使用、REPL 环境、开发工作流、MCP 集成、高级模式和最佳实践。适合学习 Claude Code 的高级功能和开发技巧。
---

# Claude Code 高级开发指南

全面的 Claude Code 中文学习指南，涵盖从基础到高级的所有核心概念、工具使用、开发工作流和最佳实践。

## 何时使用此技能

当需要以下帮助时使用此技能：
- 学习 Claude Code 的核心功能和工具
- 掌握 REPL 环境的高级用法
- 理解开发工作流和任务管理
- 使用 MCP 集成外部系统
- 实现高级开发模式
- 应用 Claude Code 最佳实践
- 解决常见问题和错误
- 进行大文件分析和处理

## 快速参考

### Claude Code 核心工具（7个）

1. **REPL** - JavaScript 运行时环境
   - 完整的 ES6+ 支持
   - 预加载库：D3.js, MathJS, Lodash, Papaparse, SheetJS
   - 支持 async/await, BigInt, WebAssembly
   - 文件读取：`window.fs.readFile()`

2. **Artifacts** - 可视化输出
   - React, Three.js, 图表库
   - HTML/SVG 渲染
   - 交互式组件

3. **Web Search** - 网络搜索
   - 仅美国可用
   - 域名过滤支持

4. **Web Fetch** - 获取网页内容
   - HTML 转 Markdown
   - 内容提取和分析

5. **Conversation Search** - 对话搜索
   - 搜索历史对话
   - 上下文检索

6. **Recent Chats** - 最近对话
   - 访问最近会话
   - 对话历史

7. **End Conversation** - 结束对话
   - 清理和总结
   - 会话管理

### 大文件分析工作流

```bash
# 阶段 1：定量评估
wc -l filename.md    # 行数统计
wc -w filename.md    # 词数统计
wc -c filename.md    # 字符数统计

# 阶段 2：结构分析
grep "^#{1,6} " filename.md  # 提取标题层次
grep "```" filename.md       # 识别代码块
grep -c "keyword" filename.md # 关键词频率

# 阶段 3：内容提取
Read filename.md offset=0 limit=50      # 文件开头
Read filename.md offset=N limit=100     # 目标部分
Read filename.md offset=-50 limit=50    # 文件结尾
```

### REPL 高级用法

```javascript
// 数据处理
const data = [1, 2, 3, 4, 5];
const sum = data.reduce((a, b) => a + b, 0);

// 使用预加载库
// Lodash
_.chunk([1, 2, 3, 4], 2);  // [[1,2], [3,4]]

// MathJS
math.sqrt(16);  // 4

// D3.js
d3.range(10);  // [0,1,2,3,4,5,6,7,8,9]

// 读取文件
const content = await window.fs.readFile('path/to/file');

// 异步操作
const result = await fetch('https://api.example.com/data');
const json = await result.json();
```

### 斜杠命令系统

**内置命令：**
- `/help` - 显示帮助
- `/clear` - 清除对话
- `/plugin` - 管理插件
- `/settings` - 配置设置

**自定义命令：**
创建 `.claude/commands/mycommand.md`：
```markdown
根据需求执行特定任务的指令
```

使用：`/mycommand`

### 开发工作流模式

#### 1. 文件分析工作流
```bash
# 探索 → 理解 → 实现
ls -la                  # 列出文件
Read file.py            # 读取内容
grep "function" file.py # 搜索模式
# 然后实现修改
```

#### 2. 算法验证工作流
```bash
# 设计 → 验证 → 实现
# 1. 在 REPL 中测试逻辑
# 2. 验证边界情况
# 3. 实现到代码
```

#### 3. 数据探索工作流
```bash
# 检查 → 分析 → 可视化
# 1. 读取数据文件
# 2. REPL 中分析
# 3. Artifacts 可视化
```

## 核心概念

### 工具权限系统

**自动授予权限的工具：**
- REPL
- Artifacts  
- Web Search/Fetch
- Conversation Search

**需要授权的工具：**
- Bash (读/写文件系统)
- Edit (修改文件)
- Write (创建文件)

### 项目上下文

Claude 自动识别：
- Git 仓库状态
- 编程语言（从文件扩展名）
- 项目结构
- 依赖配置

### 内存系统

**对话内存：**
- 存储在当前会话
- 200K token 窗口
- 自动上下文管理

**持久内存（实验性）：**
- 跨会话保存
- 用户偏好记忆
- 项目上下文保留

## MCP 集成

### 什么是 MCP？

Model Context Protocol - 连接 Claude 到外部系统的协议。

### MCP 服务器配置

配置文件：`~/.config/claude/mcp_config.json`

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["path/to/server.js"],
      "env": {
        "API_KEY": "your-key"
      }
    }
  }
}
```

### 使用 MCP 工具

Claude 会自动发现 MCP 工具并在对话中使用：

```
"使用 my-server 工具获取数据"
```

## 钩子系统

### 钩子类型

在 `.claude/settings.json` 配置：

```json
{
  "hooks": {
    "tool-pre-use": "echo 'About to use tool'",
    "tool-post-use": "echo 'Tool used'",
    "user-prompt-submit": "echo 'Processing prompt'"
  }
}
```

### 常见钩子用途

- 自动格式化代码
- 运行测试
- Git 提交检查
- 日志记录
- 通知发送

## 高级模式

### 多代理协作

使用 Task 工具启动子代理：

```
"启动一个专门的代理来优化这个算法"
```

子代理特点：
- 独立上下文
- 专注单一任务
- 返回结果到主代理

### 智能任务管理

使用 TodoWrite 工具：

```
"创建任务列表来跟踪这个项目"
```

任务状态：
- `pending` - 待处理
- `in_progress` - 进行中  
- `completed` - 已完成

### 代码生成模式

**渐进式开发：**
1. 生成基础结构
2. 添加核心功能
3. 实现细节
4. 测试和优化

**验证驱动：**
1. 写测试用例
2. 实现功能
3. 运行测试
4. 修复问题

## 质量保证

### 自动化测试

```bash
# 运行测试
npm test
pytest

# 类型检查
mypy script.py
tsc --noEmit

# 代码检查
eslint src/
flake8 .
```

### 代码审查模式

使用子代理进行审查：

```
"启动代码审查代理检查这个文件"
```

审查重点：
- 代码质量
- 安全问题
- 性能优化
- 最佳实践

## 错误恢复

### 常见错误模式

1. **工具使用错误**
   - 检查权限
   - 验证语法
   - 确认路径

2. **文件操作错误**
   - 确认文件存在
   - 检查读写权限
   - 验证路径正确

3. **API 调用错误**
   - 检查网络连接
   - 验证 API 密钥
   - 确认请求格式

### 渐进式修复策略

1. 隔离问题
2. 最小化复现
3. 逐步修复
4. 验证解决方案

## 最佳实践

### 开发原则

1. **清晰优先** - 明确需求和目标
2. **渐进实现** - 分步骤开发
3. **持续验证** - 频繁测试
4. **适当抽象** - 合理模块化

### 工具使用原则

1. **正确的工具** - 选择合适的工具
2. **工具组合** - 多工具协同
3. **权限最小化** - 只请求必要权限
4. **错误处理** - 优雅处理失败

### 性能优化

1. **批量操作** - 合并多个操作
2. **增量处理** - 处理大文件
3. **缓存结果** - 避免重复计算
4. **异步优先** - 使用 async/await

## 安全考虑

### 沙箱模型

每个工具在隔离环境中运行：
- REPL：无文件系统访问
- Bash：需要明确授权
- Web：仅特定域名

### 最佳安全实践

1. **最小权限** - 仅授予必要权限
2. **代码审查** - 检查生成的代码
3. **敏感数据** - 不要共享密钥
4. **定期审计** - 检查钩子和配置

## 故障排除

### 工具无法使用

**症状：** 工具调用失败

**解决方案：**
- 检查权限设置
- 验证语法正确
- 确认文件路径
- 查看错误消息

### REPL 性能问题

**症状：** REPL 执行缓慢

**解决方案：**
- 减少数据量
- 使用流式处理
- 优化算法
- 分批处理

### MCP 连接失败

**症状：** MCP 服务器无响应

**解决方案：**
- 检查配置文件
- 验证服务器运行
- 确认环境变量
- 查看服务器日志

## 实用示例

### 示例 1：数据分析

```javascript
// 在 REPL 中
const data = await window.fs.readFile('data.csv');
const parsed = Papa.parse(data, { header: true });
const values = parsed.data.map(row => parseFloat(row.value));
const avg = _.mean(values);
const std = math.std(values);
console.log(`平均值: ${avg}, 标准差: ${std}`);
```

### 示例 2：文件搜索

```bash
# 在 Bash 中
grep -r "TODO" src/
find . -name "*.py" -type f
```

### 示例 3：网络数据获取

```
"使用 web_fetch 获取 https://api.example.com/data 的内容，
然后在 REPL 中分析 JSON 数据"
```

## 参考文件

此技能包含详细文档：

- **README.md** (9,594 行) - 完整的 Claude Code 高级指南

包含以下主题：
- 核心工具深度解析
- REPL 高级协同模式
- 开发工作流详解
- MCP 集成完整指南
- 钩子系统配置
- 高级模式和最佳实践
- 故障排除和安全考虑

使用 `view` 命令查看参考文件获取详细信息。

## 资源

- **GitHub 仓库**: https://github.com/karminski/claude-code-guide-study
- **原始版本**: https://github.com/Cranot/claude-code-guide
- **Anthropic 官方文档**: https://docs.claude.com

## 注意事项

本指南结合了：
- 官方功能和公告
- 实际使用观察到的模式
- 概念性方法和最佳实践
- 第三方工具集成

请在使用时参考最新的官方文档。

---

**使用这个技能深入掌握 Claude Code 的强大功能！**
