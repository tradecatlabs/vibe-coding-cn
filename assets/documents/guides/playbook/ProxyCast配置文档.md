# ProxyCast 完整配置文档

## 系统原理

```
你的 AI 凭证                ProxyCast              任意 AI 工具
┌─────────────────┐      ┌─────────────┐      ┌─────────────────────┐
│ Kiro OAuth      │      │             │      │ Claude Code         │
│ Gemini API Keys │ ───▶ │  本地 API   │ ───▶ │ Cherry Studio       │
│ Qwen OAuth      │      │  代理服务    │      │ Cursor / Cline      │
│ OpenRouter      │      │  :8999      │      │ 你的 AI Agent       │
└─────────────────┘      └─────────────┘      └─────────────────────┘
```

ProxyCast 把你已有的 AI 凭证转换成标准 OpenAI/Anthropic API，让任何支持这些接口的工具都能用。

---

## 一、启动 ProxyCast

```bash
cd /mnt/d/.projects/kiro-account-manager-main.zip/proxycast-main && ./src-tauri/target/release/proxycast &
```

服务监听：`http://127.0.0.1:8999`

---

## 二、Claude Code 启动命令

### Claude Opus 4.7 (Kiro 凭证，最强)
```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model claude-opus-4-7
```

### Claude Sonnet 4.5 (Kiro 凭证)
```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model claude-sonnet-4-5
```

### DeepSeek R1 (OpenRouter 免费，推理最强)
```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model deepseek/deepseek-r1-0528:free
```

### Gemini 2.0 Flash (OpenRouter 免费)
```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model google/gemini-2.0-flash-exp:free
```

### Llama 3.1 405B (OpenRouter 免费，综合最强)
```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model meta-llama/llama-3.1-405b-instruct:free
```

### Devstral 2 (OpenRouter 免费，代码专精)
```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model mistralai/devstral-2512:free
```

### Gemini 3.1 Pro Preview - 最新预览版
```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model gemini-3.1-pro-preview
```

### Gemini 2.5 Pro - Pro 版本
```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model gemini-2.5-pro
```

### Gemini 2.5 Pro Preview
```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model gemini-2.5-pro-preview-06-05
```

### Gemini 2.5 Flash - 快速版本
```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model gemini-2.5-flash
```

### Gemini 2.5 Flash Lite - 轻量版本
```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model gemini-2.5-flash-lite
```

---

## 三、API 直接调用

### 通用配置
```
API Base URL: http://127.0.0.1:8999/v1
API Key: proxy_cast
```

### cURL 示例
```bash
curl http://127.0.0.1:8999/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer proxy_cast" \
  -d '{
    "model": "claude-opus-4-5",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### 获取可用模型列表
```bash
curl http://127.0.0.1:8999/v1/models -H "Authorization: Bearer proxy_cast"
```

---

## 四、可用模型列表

### Kiro 凭证 (Claude)
| 模型 | 说明 |
|------|------|
| `claude-opus-4-5` | 最强模型 |
| `claude-sonnet-4-5` | 平衡性能 |
| `claude-sonnet-4-5-20250929` | Sonnet 特定版本 |
| `claude-3-7-sonnet-20250219` | Claude 3.7 |
| `claude-3-5-sonnet-latest` | Claude 3.5 |

### Gemini API Keys (8个轮询负载均衡)
| 模型 | 说明 |
|------|------|
| `gemini-3-pro-preview` | 最新预览版 |
| `gemini-2.5-pro` | Pro 版本 |
| `gemini-2.5-flash` | 快速版本 |
| `gemini-2.5-flash-lite` | 轻量版本 |

### Qwen OAuth
| 模型 | 说明 |
|------|------|
| `qwen3-coder-plus` | 代码增强版 |
| `qwen3-coder-flash` | 快速版本 |

### OpenRouter 免费模型
| 模型 | 说明 |
|------|------|
| `deepseek/deepseek-r1-0528:free` | 推理最强 |
| `google/gemini-2.0-flash-exp:free` | 翻译首选 |
| `meta-llama/llama-3.1-405b-instruct:free` | 综合最强 |
| `meta-llama/llama-3.3-70b-instruct:free` | 速度快 |
| `mistralai/devstral-2512:free` | 代码专精 123B |
| `nousresearch/hermes-3-llama-3.1-405b:free` | 指令遵循好 |
| `openai/gpt-oss-120b:free` | GPT 开源 120B |
| `openai/gpt-oss-20b:free` | GPT 开源 20B |
| `moonshotai/kimi-k2:free` | Kimi K2.5 月之暗面 |
| `z-ai/glm-4.5-air:free` | 中文原生 |
| `alibaba/tongyi-deepresearch-30b-a3b:free` | 中文研究 |
| `kwaipilot/kat-coder-pro:free` | 代码 Agent |
| `qwen/qwen-2.5-vl-7b-instruct:free` | 视觉理解 |
| `allenai/olmo-3.1-32b-think:free` | 深度推理 |

---

## 五、凭证配置详情

### 凭证文件位置
| Provider | 路径 |
|----------|------|
| Kiro | `~/.aws/sso/cache/kiro-auth-token.json` |
| Gemini | `~/.gemini/oauth_creds.json` |
| Qwen | `~/.qwen/oauth_creds.json` |
| Codex | `~/.codex/auth.json` |

### ProxyCast 数据目录
- 配置文件：`~/.config/proxycast/config.json`
- 数据库：`~/.proxycast/proxycast.db`
- 凭证副本：`~/.local/share/proxycast/credentials/`

### 当前凭证池
```
kiro          - Kiro OAuth (Claude)
qwen          - Qwen OAuth
gemini_api_key - Gemini Key 1-8 (8个轮询)
openai        - OpenRouter Free
```

---

## 六、刷新 Kiro Token

Kiro Token 过期后，使用以下命令刷新：

```bash
REFRESH_TOKEN=$(cat ~/.aws/sso/cache/kiro-auth-token.json | jq -r '.refreshToken')

curl -s -X POST "https://prod.us-east-1.auth.desktop.kiro.dev/refreshToken" \
  -H "Content-Type: application/json" \
  -d "{\"refreshToken\": \"$REFRESH_TOKEN\"}" | jq '.' > /tmp/new_token.json

# 更新 token 文件
cat ~/.aws/sso/cache/kiro-auth-token.json | jq --slurpfile new /tmp/new_token.json '
  .accessToken = $new[0].accessToken |
  .expiresAt = (now + 3600 | todate)
' > ~/.aws/sso/cache/kiro-auth-token.json.tmp

mv ~/.aws/sso/cache/kiro-auth-token.json.tmp ~/.aws/sso/cache/kiro-auth-token.json
```

或者直接在 ProxyCast 界面点"刷新 Token"按钮。

---

## 七、配置文件参考

### ~/.config/proxycast/config.json
```json
{
  "server": {
    "host": "127.0.0.1",
    "port": 8999,
    "api_key": "proxy_cast"
  },
  "providers": {
    "kiro": {
      "enabled": true,
      "credentials_path": "~/.aws/sso/cache/kiro-auth-token.json"
    },
    "gemini": {
      "enabled": true,
      "credentials_path": "~/.gemini/oauth_creds.json"
    },
    "qwen": {
      "enabled": true,
      "credentials_path": "~/.qwen/oauth_creds.json"
    }
  },
  "default_provider": "kiro"
}
```

---

## 八、其他工具配置

### Cherry Studio / Cursor / Cline
```
API Base URL: http://127.0.0.1:8999/v1
API Key: proxy_cast
Model: claude-opus-4-5
```

### Python 代码
```python
import openai

client = openai.OpenAI(
    base_url="http://127.0.0.1:8999/v1",
    api_key="proxy_cast"
)

response = client.chat.completions.create(
    model="claude-opus-4-5",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

---

## 九、故障排查

### ProxyCast 没运行
```bash
ps aux | grep proxycast
# 如果没有，启动它：
cd /mnt/d/.projects/kiro-account-manager-main.zip/proxycast-main && ./src-tauri/target/release/proxycast &
```

### 检查端口
```bash
ss -tlnp | grep 8999
```

### 测试 API
```bash
curl http://127.0.0.1:8999/v1/models -H "Authorization: Bearer proxy_cast"
```

### Token 过期
在 ProxyCast 界面点"刷新 Token"，或手动刷新（见第六节）。

---

## 十、Gemini API Keys

当前配置的 8 个 Key（轮询负载均衡）：
```
# 请在此处填入你自己的 Gemini API Keys
# 格式：AIzaSy... （每行一个）
# 获取地址：https://aistudio.google.com/app/apikey
```

每日限制：每个 Key 20 RPD，8 个 Key = 160 次/天

---

## 十一、OpenRouter API Key

```
# 请在此处填入你自己的 OpenRouter API Key
# 格式：sk-or-v1-...
# 获取地址：https://openrouter.ai/keys
```

免费模型无限制使用。

---

*文档生成时间：2025-12-20 16:38*


---

## 十二、Claude Code 完整启动命令大全

### Kiro 凭证 (Claude 系列)

```bash
# Claude Opus 4.7 - 最强模型
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model claude-opus-4-7

# Claude Sonnet 4.5 - 平衡性能
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model claude-sonnet-4-5

# Claude Sonnet 4.5 特定版本
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model claude-sonnet-4-5-20250929

# Claude 3.7 Sonnet
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model claude-3-7-sonnet-20250219

# Claude 3.5 Sonnet Latest
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model claude-3-5-sonnet-latest
```

### Gemini 系列 (8个 API Key 轮询)

```bash
# Gemini 3.1 Pro Preview - 最新预览版
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model gemini-3.1-pro-preview

# Gemini 2.5 Pro - Pro 版本
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model gemini-2.5-pro

# Gemini 2.5 Pro Preview
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model gemini-2.5-pro-preview-06-05

# Gemini 2.5 Flash - 快速版本
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model gemini-2.5-flash

# Gemini 2.5 Flash Lite - 轻量版本
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model gemini-2.5-flash-lite
```

### Qwen 系列 (阿里通义千问)

```bash
# Qwen3 Coder Plus - 代码增强版
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model qwen3-coder-plus

# Qwen3 Coder Flash - 快速版本
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model qwen3-coder-flash
```

### OpenRouter 免费模型

```bash
# DeepSeek R1 - 推理最强
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model deepseek/deepseek-r1-0528:free

# Gemini 2.0 Flash Exp - 翻译首选
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model google/gemini-2.0-flash-exp:free

# Llama 3.1 405B - 综合最强
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model meta-llama/llama-3.1-405b-instruct:free

# Llama 3.3 70B - 速度快
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model meta-llama/llama-3.3-70b-instruct:free

# Hermes 3 405B - 指令遵循好
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model nousresearch/hermes-3-llama-3.1-405b:free

# Devstral 2 - 代码专精 123B
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model mistralai/devstral-2512:free

# GLM 4.5 Air - 中文原生
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model z-ai/glm-4.5-air:free

# 通义深度研究 - 中文研究
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model alibaba/tongyi-deepresearch-30b-a3b:free

# KAT-Coder Pro - 代码 Agent
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model kwaipilot/kat-coder-pro:free

# Qwen 2.5 VL - 视觉理解
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model qwen/qwen-2.5-vl-7b-instruct:free

# NVIDIA Nemotron 12B VL - 视觉/文档
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model nvidia/nemotron-nano-12b-v2-vl:free

# Olmo 3.1 32B Think - 深度推理
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model allenai/olmo-3.1-32b-think:free
```

---

## 十三、快捷别名配置

在 `~/.bash_aliases` 或 `~/.bashrc` 中添加：

```bash
# ProxyCast 启动
alias proxycast='cd /mnt/d/.projects/kiro-account-manager-main.zip/proxycast-main && ./src-tauri/target/release/proxycast &'

# Claude Code 快捷命令
alias cc-opus='CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model claude-opus-4-5'
alias cc-sonnet='CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model claude-sonnet-4-5'
alias cc-gemini='CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model gemini-3-pro-preview'
alias cc-deepseek='CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model deepseek/deepseek-r1-0528:free'
alias cc-qwen='CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model qwen3-coder-plus'
alias cc-llama='CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model meta-llama/llama-3.1-405b-instruct:free'
alias cc-devstral='CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model mistralai/devstral-2512:free'
```

添加后执行 `source ~/.bashrc` 生效。

---

## 十四、模型推荐场景

| 场景 | 推荐模型 | 启动命令 |
|------|----------|----------|
| 复杂推理/架构设计 | claude-opus-4-5 | `cc-opus` |
| 日常编码 | claude-sonnet-4-5 | `cc-sonnet` |
| 快速问答 | gemini-2.5-flash | 见上方命令 |
| 深度推理 | deepseek/deepseek-r1-0528:free | `cc-deepseek` |
| 代码专精 | mistralai/devstral-2512:free | `cc-devstral` |
| 中文任务 | qwen3-coder-plus | `cc-qwen` |
| 免费综合 | meta-llama/llama-3.1-405b-instruct:free | `cc-llama` |

---

*文档更新时间：2025-12-20 16:41*


---

## 十五、从零部署完整教程

### 1. 环境要求

```bash
# 系统要求
- Linux / WSL2 / macOS
- Node.js >= 20.0.0
- Rust >= 1.70
- pnpm 或 npm

# 检查环境
node -v    # v20.x.x
rustc -V   # rustc 1.70+
```

### 2. 获取源码

```bash
# 克隆或下载 ProxyCast
cd /mnt/d/.projects
git clone https://github.com/aiclientproxy/proxycast.git
# 或解压已有的 zip 包
```

### 3. 编译构建

```bash
cd proxycast-main

# 安装前端依赖
npm install

# 构建 Tauri 应用
npm run tauri build

# 构建产物位置
# Linux: src-tauri/target/release/proxycast
# macOS: src-tauri/target/release/bundle/dmg/
# Windows: src-tauri/target/release/bundle/msi/
```

### 4. 准备凭证文件

#### Kiro 凭证
```bash
# 安装 Kiro IDE 并登录，凭证自动生成在：
~/.aws/sso/cache/kiro-auth-token.json
```

#### Gemini 凭证
```bash
# 安装 Gemini CLI 并登录
pip install gemini-cli
gemini auth login
# 凭证位置：~/.gemini/oauth_creds.json
```

#### Qwen 凭证
```bash
# 安装通义千问 CLI 并登录
# 凭证位置：~/.qwen/oauth_creds.json
```

### 5. 首次启动配置

```bash
# 启动 ProxyCast
./src-tauri/target/release/proxycast &

# 等待 GUI 启动后：
# 1. 进入 "凭证池" 页面
# 2. 点击 "一键读取凭证" 或手动添加
# 3. 进入 "Dashboard" 点击 "启动服务器"
```

### 6. 手动添加凭证到数据库（无 GUI 方式）

```bash
# Kiro 凭证
sqlite3 ~/.proxycast/proxycast.db "INSERT INTO provider_pool_credentials (uuid, provider_type, credential_data, is_healthy, check_health, error_count, is_disabled, name, usage_count, created_at, updated_at, source) VALUES (
  '$(uuidgen)',
  'kiro',
  '{\"type\":\"kiro_o_auth\",\"creds_file_path\":\"$HOME/.aws/sso/cache/kiro-auth-token.json\"}',
  1, 1, 0, 0, 'Kiro OAuth', 0, $(date +%s), $(date +%s), 'manual'
);"

# Gemini OAuth
sqlite3 ~/.proxycast/proxycast.db "INSERT INTO provider_pool_credentials (uuid, provider_type, credential_data, is_healthy, check_health, error_count, is_disabled, name, usage_count, created_at, updated_at, source) VALUES (
  '$(uuidgen)',
  'gemini',
  '{\"type\":\"gemini_o_auth\",\"creds_file_path\":\"$HOME/.gemini/oauth_creds.json\",\"project_id\":null}',
  1, 1, 0, 0, 'Gemini OAuth', 0, $(date +%s), $(date +%s), 'manual'
);"

# Gemini API Key
sqlite3 ~/.proxycast/proxycast.db "INSERT INTO provider_pool_credentials (uuid, provider_type, credential_data, is_healthy, check_health, error_count, is_disabled, name, usage_count, created_at, updated_at, source) VALUES (
  '$(uuidgen)',
  'gemini_api_key',
  '{\"type\":\"gemini_api_key\",\"api_key\":\"你的API_KEY\",\"base_url\":null,\"excluded_models\":[]}',
  1, 1, 0, 0, 'Gemini Key 1', 0, $(date +%s), $(date +%s), 'manual'
);"

# Qwen OAuth
sqlite3 ~/.proxycast/proxycast.db "INSERT INTO provider_pool_credentials (uuid, provider_type, credential_data, is_healthy, check_health, error_count, is_disabled, name, usage_count, created_at, updated_at, source) VALUES (
  '$(uuidgen)',
  'qwen',
  '{\"type\":\"qwen_o_auth\",\"creds_file_path\":\"$HOME/.qwen/oauth_creds.json\"}',
  1, 1, 0, 0, 'Qwen OAuth', 0, $(date +%s), $(date +%s), 'manual'
);"

# OpenRouter (OpenAI 兼容)
sqlite3 ~/.proxycast/proxycast.db "INSERT INTO provider_pool_credentials (uuid, provider_type, credential_data, is_healthy, check_health, error_count, is_disabled, name, usage_count, created_at, updated_at, source) VALUES (
  '$(uuidgen)',
  'openai',
  '{\"type\":\"open_a_i_key\",\"api_key\":\"sk-or-v1-xxx你的key\",\"base_url\":\"https://openrouter.ai/api\"}',
  1, 1, 0, 0, 'OpenRouter Free', 0, $(date +%s), $(date +%s), 'manual'
);"
```

### 7. 创建配置文件

```bash
mkdir -p ~/.config/proxycast

cat > ~/.config/proxycast/config.json << 'EOF'
{
  "server": {
    "host": "127.0.0.1",
    "port": 8999,
    "api_key": "proxy_cast",
    "tls": {"enable": false}
  },
  "providers": {
    "kiro": {"enabled": true, "credentials_path": "~/.aws/sso/cache/kiro-auth-token.json"},
    "gemini": {"enabled": true, "credentials_path": "~/.gemini/oauth_creds.json"},
    "qwen": {"enabled": true, "credentials_path": "~/.qwen/oauth_creds.json"}
  },
  "default_provider": "kiro"
}
EOF
```

### 8. 验证部署

```bash
# 启动服务
./src-tauri/target/release/proxycast &

# 等待几秒后测试
curl http://127.0.0.1:8999/v1/models -H "Authorization: Bearer proxy_cast"

# 测试聊天
curl http://127.0.0.1:8999/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer proxy_cast" \
  -d '{"model":"claude-sonnet-4-5","messages":[{"role":"user","content":"Hi"}]}'
```

---

## 十六、无头模式（Headless）部署教程

适用于服务器、Docker、无 GUI 环境。

### 1. 无头启动

```bash
# 设置无显示环境
export DISPLAY=

# 或使用虚拟显示（如果需要）
Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99

# 启动 ProxyCast
./src-tauri/target/release/proxycast &
```

### 2. 纯命令行配置（无需 GUI）

```bash
#!/bin/bash
# headless-setup.sh - 无头模式一键配置脚本

PROXYCAST_DIR="/path/to/proxycast-main"
DB_PATH="$HOME/.proxycast/proxycast.db"
CONFIG_PATH="$HOME/.config/proxycast/config.json"

# 创建目录
mkdir -p ~/.proxycast ~/.config/proxycast

# 初始化数据库（首次运行会自动创建）
$PROXYCAST_DIR/src-tauri/target/release/proxycast &
sleep 3
pkill -f proxycast

# 添加凭证
add_credential() {
  local type=$1
  local data=$2
  local name=$3
  sqlite3 $DB_PATH "INSERT INTO provider_pool_credentials (uuid, provider_type, credential_data, is_healthy, check_health, error_count, is_disabled, name, usage_count, created_at, updated_at, source) VALUES ('$(uuidgen)', '$type', '$data', 1, 1, 0, 0, '$name', 0, $(date +%s), $(date +%s), 'manual');"
}

# 添加 Kiro
add_credential "kiro" '{"type":"kiro_o_auth","creds_file_path":"'$HOME'/.aws/sso/cache/kiro-auth-token.json"}' "Kiro OAuth"

# 添加 Gemini API Keys
GEMINI_KEYS=(
  "${GOOGLE_API_KEY}"
  "${GOOGLE_API_KEY}"
  # 添加更多 keys...
)
for i in "${!GEMINI_KEYS[@]}"; do
  add_credential "gemini_api_key" '{"type":"gemini_api_key","api_key":"'${GEMINI_KEYS[$i]}'","base_url":null,"excluded_models":[]}' "Gemini Key $((i+1))"
done

# 添加 OpenRouter
add_credential "openai" '{"type":"open_a_i_key","api_key":"sk-or-v1-xxx","base_url":"https://openrouter.ai/api"}' "OpenRouter"

echo "配置完成！"
```

### 3. Systemd 服务（Linux 后台运行）

```bash
# 创建服务文件
sudo cat > /etc/systemd/system/proxycast.service << 'EOF'
[Unit]
Description=ProxyCast API Proxy Service
After=network.target

[Service]
Type=simple
User=lenovo
Environment=DISPLAY=
WorkingDirectory=/mnt/d/.projects/kiro-account-manager-main.zip/proxycast-main
ExecStart=/mnt/d/.projects/kiro-account-manager-main.zip/proxycast-main/src-tauri/target/release/proxycast
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 启用并启动服务
sudo systemctl daemon-reload
sudo systemctl enable proxycast
sudo systemctl start proxycast

# 查看状态
sudo systemctl status proxycast

# 查看日志
journalctl -u proxycast -f
```

### 4. Docker 部署（可选）

```dockerfile
# Dockerfile
FROM rust:1.70 as builder
WORKDIR /app
COPY . .
RUN cargo build --release -p proxycast

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y libwebkit2gtk-4.1-0 libgtk-3-0 && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/proxycast /usr/local/bin/
EXPOSE 8999
CMD ["proxycast"]
```

```bash
# 构建并运行
docker build -t proxycast .
docker run -d -p 8999:8999 -v ~/.proxycast:/root/.proxycast -v ~/.config/proxycast:/root/.config/proxycast proxycast
```

### 5. 无头模式下刷新 Token

```bash
#!/bin/bash
# refresh-kiro-token.sh - 自动刷新 Kiro Token

TOKEN_FILE="$HOME/.aws/sso/cache/kiro-auth-token.json"
REFRESH_TOKEN=$(jq -r '.refreshToken' "$TOKEN_FILE")

# 调用刷新 API
RESPONSE=$(curl -s -X POST "https://prod.us-east-1.auth.desktop.kiro.dev/refreshToken" \
  -H "Content-Type: application/json" \
  -d "{\"refreshToken\": \"$REFRESH_TOKEN\"}")

# 检查是否成功
if echo "$RESPONSE" | jq -e '.accessToken' > /dev/null 2>&1; then
  NEW_ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.accessToken')
  NEW_EXPIRES=$(date -d "+1 hour" --iso-8601=seconds)
  
  # 更新 token 文件
  jq --arg token "$NEW_ACCESS_TOKEN" --arg exp "$NEW_EXPIRES" \
    '.accessToken = $token | .expiresAt = $exp' "$TOKEN_FILE" > "${TOKEN_FILE}.tmp"
  mv "${TOKEN_FILE}.tmp" "$TOKEN_FILE"
  
  echo "Token 刷新成功！"
else
  echo "Token 刷新失败：$RESPONSE"
  exit 1
fi
```

```bash
# 添加到 crontab，每 50 分钟刷新一次
crontab -e
# 添加：*/50 * * * * /path/to/refresh-kiro-token.sh >> /var/log/kiro-refresh.log 2>&1
```

### 6. 健康检查脚本

```bash
#!/bin/bash
# health-check.sh

API_URL="http://127.0.0.1:8999"
API_KEY="proxy_cast"

# 检查服务是否运行
if ! curl -s "$API_URL/v1/models" -H "Authorization: Bearer $API_KEY" > /dev/null; then
  echo "ProxyCast 服务异常，正在重启..."
  pkill -f proxycast
  sleep 2
  cd /mnt/d/.projects/kiro-account-manager-main.zip/proxycast-main
  ./src-tauri/target/release/proxycast &
  sleep 5
  
  if curl -s "$API_URL/v1/models" -H "Authorization: Bearer $API_KEY" > /dev/null; then
    echo "重启成功！"
  else
    echo "重启失败，请检查日志"
    exit 1
  fi
else
  echo "服务正常运行"
fi
```

### 7. 远程访问配置

```bash
# 修改配置允许外部访问
sed -i 's/"host": "127.0.0.1"/"host": "0.0.0.0"/' ~/.config/proxycast/config.json

# 重启服务
pkill -f proxycast
./src-tauri/target/release/proxycast &

# 获取 IP
ip addr show | grep "inet " | grep -v 127.0.0.1

# 外部访问
# API Base URL: http://<你的IP>:8999/v1
# API Key: proxy_cast
```

---

## 十七、常用运维命令

```bash
# 启动
cd /mnt/d/.projects/kiro-account-manager-main.zip/proxycast-main && ./src-tauri/target/release/proxycast &

# 停止
pkill -f proxycast

# 重启
pkill -f proxycast; sleep 2; cd /mnt/d/.projects/kiro-account-manager-main.zip/proxycast-main && ./src-tauri/target/release/proxycast &

# 查看进程
ps aux | grep proxycast

# 查看端口
ss -tlnp | grep 8999

# 查看日志
tail -f ~/.proxycast/logs/*.log

# 查看凭证池
sqlite3 ~/.proxycast/proxycast.db "SELECT provider_type, name, is_healthy FROM provider_pool_credentials;"

# 测试 API
curl http://127.0.0.1:8999/v1/models -H "Authorization: Bearer proxy_cast" | jq

# 清空凭证池
sqlite3 ~/.proxycast/proxycast.db "DELETE FROM provider_pool_credentials;"
```

---

*文档更新时间：2025-12-20 16:42*


---

## 十八、断线问题修复

### 问题原因

Claude Code 使用自定义 API endpoint 时，仍会尝试向 Anthropic 发送遥测数据。遥测失败会导致程序异常退出。

### 解决方案

所有启动命令都需要添加环境变量禁用遥测：

```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
```

### 完整单行启动命令（无遥测）

```bash
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model claude-opus-4-5
```

---

*文档更新时间：2025-12-20 17:46*


---

## 十九、Codex (OpenAI) 凭证集成（待实现）

### 凭证来源

Codex 凭证来自 OpenAI 官方 CLI 工具，存储在 `~/.codex/auth.json`：

```json
{
  "id_token": "eyJhbGciOiJSUzI1NiI...",
  "access_token": "eyJhbGciOiJSUzI1NiI...",
  "refresh_token": "rt_TK67iD7Pdgg...",
  "account_id": "24e8f403-dbdb-42f9-8309-98951fc2862e",
  "email": "xxx@gmail.com",
  "type": "codex",
  "expired": "2025-12-30T08:16:48..."
}
```

### 当前状态

- ✅ 凭证已添加到 ProxyCast 数据库
- ✅ `providers/codex.rs` 已实现 OAuth 刷新逻辑
- ❌ `server.rs` 中 `call_provider_openai` 函数尚未集成 Codex 调用
- ❌ WSL 编译环境链接器问题，无法编译新版本

### 代码修改位置

需要在 `src-tauri/src/server.rs` 的 `call_provider_openai` 函数中添加：

```rust
CredentialData::CodexOAuth { creds_file_path } => {
    // 加载凭证、刷新 token、调用 OpenAI API
    // 参考 KiroOAuth 的实现模式
}
```

### 支持的模型

Codex 凭证支持所有 OpenAI 模型：
- gpt-5.5, gpt-5.4, gpt-5.2
- gpt-4o, gpt-4o-mini, gpt-4-turbo
- o1, o1-mini, o1-preview
- o3-mini

---

## 二十、Antigravity 凭证分析

### 凭证位置

Antigravity (Google AI IDE) 的凭证存储在 SQLite 数据库中：

```
Windows: %APPDATA%\Antigravity\User\globalStorage\state.vscdb
```

### 凭证结构

```sql
-- 查询凭证
SELECT value FROM ItemTable WHERE key = 'antigravityAuthStatus';
```

返回 JSON：
```json
{
  "name": "git",
  "apiKey": "ya29.a0Aa7pCA-1M5dtt...",  // Google OAuth access_token
  "email": "xxx@gmail.com",
  "userStatusProtoBinaryBase64": "..."   // 用户状态 protobuf
}
```

### 限制

- **只有 access_token**，没有 refresh_token
- access_token 有效期约 1 小时
- 无法自动刷新，需要通过 Antigravity 应用重新登录
- refresh_token 可能存储在 Windows Credential Manager（WSL 无法访问）

### 结论

Antigravity 凭证不适合集成到 ProxyCast，因为无法自动刷新。建议使用 Gemini API Key 或 Gemini CLI OAuth 代替。

---

## 二十一、WSL 编译问题

### 问题描述

在 WSL 环境下编译 Rust 项目时，链接器报错：

```
error: unknown option '-Wl,--no-undefined-version'
error: unknown option '-Wl,--as-needed'
```

### 原因

Rust 1.90+ 默认使用 `lld` 链接器，但 WSL 的 `lld` 版本不兼容。

### 尝试的解决方案

1. **使用 gold 链接器**（失败）
```bash
RUSTFLAGS="-C link-arg=-fuse-ld=gold" cargo build --release
```

2. **配置 cargo**（失败）
```toml
# ~/.cargo/config.toml
[target.x86_64-unknown-linux-gnu]
linker = "gcc"
rustflags = ["-C", "link-arg=-fuse-ld=gold"]
```

### 建议

- 在原生 Linux 或 Windows 上编译
- 使用 Docker 容器编译
- 使用预编译的 Release 版本

---

## 二十二、数据库路径差异

### WSL vs Windows

| 环境 | 数据库路径 |
|------|-----------|
| WSL/Linux | `~/.proxycast/proxycast.db` |
| Windows | `%APPDATA%\proxycast\proxycast.db` |
| macOS | `~/Library/Application Support/proxycast/proxycast.db` |

### 注意事项

- WSL 中运行的 ProxyCast 使用 Linux 路径
- Windows GUI 版本使用 Windows 路径
- 两者数据库不共享，需要分别配置凭证

---

## 二十三、本次配置总结

### 已配置的凭证池

| Provider | 名称 | 状态 |
|----------|------|------|
| kiro | Kiro OAuth | ✅ 正常 |
| qwen | Qwen OAuth | ✅ 正常 |
| gemini_api_key | Gemini Key 1-8 | ✅ 8个轮询 |
| openai | OpenRouter Free | ✅ 正常 |
| codex | Codex OAuth | ⚠️ 待实现 |

### 可用模型

**Claude (Kiro)**
- claude-opus-4-5, claude-sonnet-4-5, claude-3-7-sonnet-20250219

**Gemini (API Keys)**
- gemini-3-pro-preview, gemini-2.5-pro, gemini-2.5-flash, gemini-2.5-flash-lite

**Qwen**
- qwen3-coder-plus, qwen3-coder-flash

**OpenRouter Free**
- deepseek/deepseek-r1-0528:free
- meta-llama/llama-3.1-405b-instruct:free
- mistralai/devstral-2512:free
- 等 10+ 免费模型

### 快速启动

```bash
# 启动 ProxyCast
cd /mnt/d/.projects/kiro-account-manager-main.zip/proxycast-main && ./src-tauri/target/release/proxycast &

# 使用 Claude Code
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model claude-opus-4-5
```

---

---

## 二十四、新增 OpenRouter 免费模型（2025-12-21 测试通过）

### 新增模型列表

| 模型 | 说明 | 状态 |
|------|------|------|
| `openai/gpt-oss-120b:free` | GPT 开源 120B | ✅ 已测试 |
| `openai/gpt-oss-20b:free` | GPT 开源 20B | ✅ 已测试 |
| `moonshotai/kimi-k2:free` | Kimi K2.5 | ✅ 已测试 |

### Claude Code 启动命令

```bash
# GPT-OSS 120B - 大参数开源模型
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model openai/gpt-oss-120b:free

# GPT-OSS 20B - 轻量开源模型
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model openai/gpt-oss-20b:free

# Kimi K2.5 - 月之暗面最新模型
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 ANTHROPIC_BASE_URL=http://127.0.0.1:8999 ANTHROPIC_API_KEY=proxy_cast claude --dangerously-skip-permissions --model moonshotai/kimi-k2:free
```

### API 测试命令

```bash
# 测试 GPT-OSS 120B
curl -s http://127.0.0.1:8999/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer proxy_cast" \
  -d '{"model":"openai/gpt-oss-120b:free","messages":[{"role":"user","content":"Hi"}],"max_tokens":10}'

# 测试 Kimi K2.5
curl -s http://127.0.0.1:8999/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer proxy_cast" \
  -d '{"model":"moonshotai/kimi-k2:free","messages":[{"role":"user","content":"Hi"}],"max_tokens":10}'
```

### 更新后的 OpenRouter 免费模型完整列表

| 模型 | 说明 | 推荐场景 |
|------|------|----------|
| `deepseek/deepseek-r1-0528:free` | 推理最强 | 复杂推理 |
| `meta-llama/llama-3.1-405b-instruct:free` | 综合最强 | 通用任务 |
| `mistralai/devstral-2512:free` | 代码专精 123B | 编程 |
| `openai/gpt-oss-120b:free` | GPT 开源 120B | 通用 |
| `openai/gpt-oss-20b:free` | GPT 开源 20B | 快速响应 |
| `moonshotai/kimi-k2:free` | Kimi K2.5 | 中文任务 |
| `google/gemini-2.0-flash-exp:free` | Gemini 2.0 | 翻译 |
| `meta-llama/llama-3.3-70b-instruct:free` | Llama 3.3 | 速度快 |
| `nousresearch/hermes-3-llama-3.1-405b:free` | Hermes 3 | 指令遵循 |
| `z-ai/glm-4.5-air:free` | GLM 4.5 | 中文原生 |
| `alibaba/tongyi-deepresearch-30b-a3b:free` | 通义深研 | 中文研究 |
| `kwaipilot/kat-coder-pro:free` | KAT-Coder | 代码 Agent |
| `qwen/qwen-2.5-vl-7b-instruct:free` | Qwen VL | 视觉理解 |
| `allenai/olmo-3.1-32b-think:free` | Olmo 3.1 | 深度推理 |

---

*文档更新时间：2025-12-21 17:07*
