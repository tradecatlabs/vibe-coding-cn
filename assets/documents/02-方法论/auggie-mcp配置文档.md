# auggie-mcp 详细配置文档

## 安装步骤

### 1. 安装 Auggie CLI
```bash
npm install -g @augmentcode/auggie@prerelease
```

### 2. 用户认证
```bash
# 方式一：交互式登录
auggie login

# 方式二：使用 token（适用于 CI/CD）
export AUGMENT_API_TOKEN="your-token"
export AUGMENT_API_URL="https://i0.api.augmentcode.com/"
```

## Claude Code 配置

### 添加到用户配置（全局）
```bash
claude mcp add-json auggie-mcp --scope user '{
  "type": "stdio",
  "command": "auggie",
  "args": ["--mcp"],
  "env": {
    "AUGMENT_API_TOKEN": "your-token",
    "AUGMENT_API_URL": "https://i0.api.augmentcode.com/"
  }
}'
```

### 添加到项目配置（当前项目）
```bash
claude mcp add-json auggie-mcp --scope project '{
  "type": "stdio",
  "command": "auggie",
  "args": ["-w", "/path/to/project", "--mcp"],
  "env": {
    "AUGMENT_API_TOKEN": "your-token",
    "AUGMENT_API_URL": "https://i0.api.augmentcode.com/"
  }
}'
```

## Codex 配置

编辑 `~/.codex/config.toml`：
```toml
[mcp_servers."auggie-mcp"]
command = "auggie"
args = ["-w", "/path/to/project", "--mcp"]
startup_timeout_ms = 20000
```

## 验证安装

```bash
# 检查 MCP 状态
claude mcp list

# 应该显示：
# auggie-mcp: auggie --mcp - ✓ Connected

# 测试功能
claude --print "使用 codebase-retrieval 搜索当前目录下的所有文件"
```

## 工具使用示例

### 1. 搜索特定文件
```bash
# 搜索所有 Python 文件
claude --print "使用 codebase-retrieval 搜索 *.py 文件"

# 搜索特定目录
claude --print "使用 codebase-retrieval 搜索 src/ 目录下的文件"
```

### 2. 代码分析
```bash
# 分析函数实现
claude --print "使用 codebase-retrieval 查找 main 函数的实现"

# 搜索 API 端点
claude --print "使用 codebase-retrieval 搜索所有 API 端点定义"
```

## 环境变量配置

创建 `~/.augment/config` 文件：
```json
{
  "apiToken": "your-token",
  "apiUrl": "https://i0.api.augmentcode.com/",
  "defaultModel": "gpt-4",
  "workspaceRoot": "/path/to/project"
}
```

## 故障排除

### 1. 连接失败
```bash
# 检查 token
auggie token print

# 重新登录
auggie logout && auggie login
```

### 2. 路径错误
```bash
# 使用绝对路径
auggie -w $(pwd) --mcp

# 检查路径是否存在
ls -la /path/to/project
```

### 3. 权限问题
```bash
# 检查文件权限
ls -la ~/.augment/

# 修复权限
chmod 600 ~/.augment/session.json
```

## 高级配置

### 自定义缓存目录
```bash
export AUGMENT_CACHE_DIR="/custom/cache/path"
```

### 设置重试超时
```bash
export AUGMENT_RETRY_TIMEOUT=30
```

### 禁用确认提示
```bash
auggie --allow-indexing --mcp
```
