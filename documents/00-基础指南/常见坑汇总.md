# 🕳️ 常见坑汇总

> Vibe Coding 过程中的常见问题和解决方案

---

<details open>
<summary><strong>🤖 AI 对话相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| AI 生成的代码跑不起来 | 上下文不足 | 提供完整错误信息，说明运行环境 |
| AI 反复修改同一个问题 | 陷入循环 | 换个思路描述，或开新对话 |
| AI 幻觉，编造不存在的 API | 模型知识过时 | 提供官方文档链接，让 AI 参考 |
| 代码越改越乱 | 没有规划 | 先让 AI 出方案，确认后再写代码 |
| AI 不理解我的需求 | 描述模糊 | 用具体例子说明，给输入输出示例 |
| AI 忘记之前的对话 | 上下文丢失 | 重新提供关键信息，或用 memory bank |
| AI 改了不该改的代码 | 指令不明确 | 明确说"只改 xxx，不要动其他文件" |
| AI 生成的代码风格不一致 | 没有规范 | 提供代码规范或示例代码 |

</details>

---

<details open>
<summary><strong>🐍 Python 虚拟环境相关</strong></summary>

### 为什么要用虚拟环境？

- 避免不同项目依赖冲突
- 保持系统 Python 干净
- 方便复现和部署

### 创建和使用 .venv

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 退出虚拟环境
deactivate
```

### 常见问题

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 死活配不好环境 | 全局污染 | 删掉重来，用 `.venv` 虚拟环境隔离 |
| `python` 命令找不到 | 没激活虚拟环境 | 先运行 `source .venv/bin/activate` |
| 装了包但 import 报错 | 装到全局了 | 确认激活虚拟环境后再 pip install |
| 不同项目依赖冲突 | 共用全局环境 | 每个项目单独建 `.venv` |
| VS Code 用错 Python | 解释器没选对 | Ctrl+Shift+P → "Python: Select Interpreter" → 选 .venv |
| pip 版本太旧 | 虚拟环境默认旧版 | `pip install --upgrade pip` |
| requirements.txt 缺依赖 | 没导出 | `pip freeze > requirements.txt` |

### 一键重置环境

环境彻底乱了？删掉重来：

```bash
# 删除旧环境
rm -rf .venv

# 重新创建
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

</details>

---

<details open>
<summary><strong>📦 Node.js 环境相关</strong></summary>

### 常见问题

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| node 版本不对 | 项目要求特定版本 | 用 nvm 管理多版本：`nvm install 18` |
| npm install 报错 | 网络/权限问题 | 换源、清缓存、删 node_modules 重装 |
| 全局包找不到 | PATH 没配 | `npm config get prefix` 加到 PATH |
| package-lock 冲突 | 多人协作 | 统一用 `npm ci` 而不是 `npm install` |
| node_modules 太大 | 正常现象 | 加到 .gitignore，不要提交 |

### 常用命令

```bash
# 换淘宝源
npm config set registry https://registry.npmmirror.com

# 清缓存
npm cache clean --force

# 删除重装
rm -rf node_modules package-lock.json
npm install

# 用 nvm 切换 Node 版本
nvm use 18
```

</details>

---

<details open>
<summary><strong>🔧 环境配置相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 命令找不到 | 环境变量没配 | 检查 PATH，重启终端 |
| 端口被占用 | 上次没关干净 | `lsof -i :端口号` 或 `netstat -ano \| findstr :端口号` |
| 权限不足 | Linux/Mac 权限 | `chmod +x` 或 `sudo` |
| 环境变量不生效 | 没 source | `source ~/.bashrc` 或重启终端 |
| .env 文件不生效 | 没加载 | 用 `python-dotenv` 或 `dotenv` 包 |
| Windows 路径问题 | 反斜杠 | 用 `/` 或 `\\` 或 `Path` 库 |

</details>

---

<details open>
<summary><strong>🌐 网络相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| GitHub 访问慢/超时 | 网络限制 | 配置代理，参考 [网络环境配置](../从零开始vibecoding/01-网络环境配置.md) |
| API 调用失败 | 网络/Key 问题 | 检查代理、API Key 是否有效 |
| 终端不走代理 | 代理配置不全 | 设置环境变量（见下方） |
| SSL 证书错误 | 代理/时间问题 | 检查系统时间，或临时关闭 SSL 验证 |
| pip/npm 下载慢 | 源在国外 | 换国内镜像源 |
| git clone 超时 | 网络限制 | 配置 git 代理或用 SSH |

### 终端代理配置

```bash
# 临时设置（当前终端有效）
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890

# 永久设置（加到 ~/.bashrc 或 ~/.zshrc）
echo 'export http_proxy=http://127.0.0.1:7890' >> ~/.bashrc
echo 'export https_proxy=http://127.0.0.1:7890' >> ~/.bashrc
source ~/.bashrc

# Git 代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```

</details>

---

<details open>
<summary><strong>📝 代码相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 代码文件太大，AI 处理不了 | 超出上下文 | 拆分文件，只给 AI 相关部分 |
| 改了代码没生效 | 缓存/没保存 | 清缓存、确认保存、重启服务 |
| 合并代码冲突 | Git 冲突 | 让 AI 帮你解决：贴出冲突内容 |
| 依赖版本冲突 | 版本不兼容 | 指定版本号，或用虚拟环境隔离 |
| 中文乱码 | 编码问题 | 统一用 UTF-8，文件开头加 `# -*- coding: utf-8 -*-` |
| 热更新不生效 | 监听问题 | 检查文件是否在监听范围内 |

</details>

---

<details open>
<summary><strong>🎯 Claude Code / Cursor 相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| Claude Code 连不上 | 网络/认证 | 检查代理，重新 `claude login` |
| Cursor 补全很慢 | 网络延迟 | 检查代理配置 |
| 额度用完了 | 免费额度有限 | 换账号或升级付费 |
| 规则文件不生效 | 路径/格式错误 | 检查 `.cursorrules` 或 `CLAUDE.md` 位置 |
| AI 读不到项目文件 | 工作区问题 | 确认在正确目录打开，检查 .gitignore |
| 生成代码位置错误 | 光标位置 | 先把光标放到正确位置再生成 |

</details>

---

<details open>
<summary><strong>🚀 部署相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 本地能跑，部署失败 | 环境差异 | 检查 Node/Python 版本，环境变量 |
| 构建超时 | 项目太大 | 优化依赖，增加构建时间限制 |
| 环境变量没生效 | 没配置 | 在部署平台设置环境变量 |
| CORS 跨域错误 | 后端没配置 | 添加 CORS 中间件 |
| 静态文件 404 | 路径问题 | 检查 build 输出目录配置 |
| 内存不足 | 免费套餐限制 | 优化代码或升级套餐 |

</details>

---

<details open>
<summary><strong>🗄️ 数据库相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 连接被拒绝 | 服务没启动 | 启动数据库服务 |
| 认证失败 | 密码错误 | 检查用户名密码，重置密码 |
| 表不存在 | 没迁移 | 运行 migration |
| 数据丢失 | 没持久化 | Docker 加 volume，或用云数据库 |
| 连接数过多 | 没关连接 | 用连接池，及时关闭连接 |

</details>

---

<details open>
<summary><strong>🐳 Docker 相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 镜像拉取失败 | 网络问题 | 配置镜像加速器 |
| 容器启动失败 | 端口冲突/配置错误 | 检查日志 `docker logs 容器名` |
| 文件修改不生效 | 没挂载 volume | 加 `-v` 参数挂载目录 |
| 磁盘空间不足 | 镜像太多 | `docker system prune` 清理 |

</details>

---

<details open>
<summary><strong>🧠 大模型使用相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| Token 超限 | 输入太长 | 精简上下文，只给必要信息 |
| 回复被截断 | 输出 token 限制 | 让 AI 分段输出，或说"继续" |
| 不同模型结果差异大 | 模型特性不同 | 根据任务选模型：Claude 写代码，GPT 通用 |
| 温度参数影响 | temperature 设置 | 代码生成用低温度(0-0.3)，创意用高温度 |
| 系统提示词被忽略 | 提示词太长/冲突 | 精简系统提示词，放重要的在前面 |
| JSON 输出格式错误 | 模型不稳定 | 用 JSON mode，或让 AI 只输出代码块 |
| 多轮对话质量下降 | 上下文污染 | 定期开新对话，保持上下文干净 |
| API 调用报错 429 | 频率限制 | 加延迟重试，或升级 API 套餐 |
| 流式输出乱码 | 编码/解析问题 | 检查 SSE 解析，确保 UTF-8 |

</details>

---

<details open>
<summary><strong>🏗️ 软件架构相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 代码越写越乱 | 没有架构设计 | 先画架构图，再写代码 |
| 改一处坏多处 | 耦合太紧 | 拆分模块，定义清晰接口 |
| 不知道代码放哪 | 目录结构混乱 | 参考 [通用项目架构模板](../模板与资源/通用项目架构模板.md) |
| 重复代码太多 | 没有抽象 | 提取公共函数/组件 |
| 状态管理混乱 | 全局状态滥用 | 用状态管理库，单向数据流 |
| 配置散落各处 | 没有统一管理 | 集中到 config 文件或环境变量 |
| 难以测试 | 依赖太多 | 依赖注入，mock 外部服务 |

</details>

---

<details open>
<summary><strong>🔄 Git 版本控制相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 提交了不该提交的文件 | .gitignore 没配 | 加到 .gitignore，`git rm --cached` |
| 提交了敏感信息 | 没检查 | 用 git-filter-branch 清理历史，换 key |
| 合并冲突不会解决 | 不熟悉 Git | 用 VS Code 冲突解决工具，或让 AI 帮忙 |
| commit 信息写错了 | 手滑 | `git commit --amend` 修改 |
| 想撤销上次提交 | 提交错了 | `git reset --soft HEAD~1` |
| 分支太多太乱 | 没有规范 | 用 Git Flow 或 trunk-based |
| push 被拒绝 | 远程有新提交 | 先 pull --rebase 再 push |

### 常用 Git 命令

```bash
# 撤销工作区修改
git checkout -- 文件名

# 撤销暂存区
git reset HEAD 文件名

# 撤销上次提交（保留修改）
git reset --soft HEAD~1

# 查看提交历史
git log --oneline -10

# 暂存当前修改
git stash
git stash pop
```

</details>

---

<details open>
<summary><strong>🧪 测试相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 不知道测什么 | 没有测试思维 | 测边界条件、异常情况、核心逻辑 |
| 测试太慢 | 测试粒度太大 | 多写单元测试，少写 E2E |
| 测试不稳定 | 依赖外部服务 | mock 外部依赖 |
| 测试通过但线上出 bug | 覆盖不全 | 增加边界测试，用 coverage 检查 |
| 改代码就要改测试 | 测试耦合实现 | 测试行为而非实现 |
| AI 生成的测试没用 | 只测 happy path | 让 AI 补充边界和异常测试 |

</details>

---

<details open>
<summary><strong>⚡ 性能相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 页面加载慢 | 资源太大 | 压缩、懒加载、CDN |
| API 响应慢 | 查询没优化 | 加索引、缓存、分页 |
| 内存泄漏 | 没清理资源 | 检查事件监听、定时器、闭包 |
| CPU 占用高 | 死循环/重复计算 | 用 profiler 定位热点 |
| 数据库查询慢 | N+1 问题 | 用 JOIN 或批量查询 |
| 前端卡顿 | 重渲染太多 | React.memo、useMemo、虚拟列表 |

</details>

---

<details open>
<summary><strong>🔐 安全相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| API Key 泄露 | 提交到 Git | 用环境变量，加到 .gitignore |
| SQL 注入 | 拼接 SQL | 用参数化查询/ORM |
| XSS 攻击 | 没转义用户输入 | 转义 HTML，用 CSP |
| CSRF 攻击 | 没有 token 验证 | 加 CSRF token |
| 密码明文存储 | 安全意识不足 | 用 bcrypt 等哈希算法 |
| 敏感信息日志 | 打印了不该打印的 | 脱敏处理，生产环境关闭 debug |

</details>

---

<details open>
<summary><strong>📱 前端开发相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 样式不生效 | 优先级/缓存 | 检查选择器优先级，清缓存 |
| 移动端适配问题 | 没做响应式 | 用 rem/vw，媒体查询 |
| 白屏 | JS 报错 | 看控制台，加错误边界 |
| 状态不同步 | 异步问题 | 用 useEffect 依赖，或状态管理库 |
| 组件不更新 | 引用没变 | 返回新对象/数组，不要直接修改 |
| 打包体积太大 | 没有优化 | 按需引入、代码分割、tree shaking |
| 跨域问题 | 浏览器安全策略 | 后端配 CORS，或用代理 |

</details>

---

<details open>
<summary><strong>🖥️ 后端开发相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 接口返回慢 | 同步阻塞 | 用异步，耗时任务放队列 |
| 并发问题 | 竞态条件 | 加锁、用事务、乐观锁 |
| 服务挂了没发现 | 没有监控 | 加健康检查、告警 |
| 日志找不到问题 | 日志不全 | 加 request_id，结构化日志 |
| 配置不同环境 | 硬编码 | 用环境变量区分 dev/prod |
| OOM 崩溃 | 内存泄漏/数据太大 | 分页、流式处理、检查泄漏 |

</details>

---

<details open>
<summary><strong>🔌 API 设计相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 接口命名混乱 | 没有规范 | 遵循 RESTful，动词用 HTTP 方法 |
| 返回格式不统一 | 没有约定 | 统一响应结构 `{code, data, message}` |
| 版本升级困难 | 没有版本控制 | URL 加版本号 `/api/v1/` |
| 文档和实现不一致 | 手动维护 | 用 Swagger/OpenAPI 自动生成 |
| 错误信息不明确 | 只返回 500 | 细分错误码，返回有用信息 |
| 分页参数不统一 | 各写各的 | 统一用 `page/size` 或 `offset/limit` |

</details>

---

<details open>
<summary><strong>📊 数据处理相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 数据格式不对 | 类型转换问题 | 做好类型校验和转换 |
| 时区问题 | 没统一时区 | 存 UTC，显示时转本地 |
| 精度丢失 | 浮点数问题 | 金额用整数（分），或 Decimal |
| 大文件处理 OOM | 一次性加载 | 流式处理、分块读取 |
| 编码问题 | 不是 UTF-8 | 统一用 UTF-8，读文件指定编码 |
| 空值处理 | null/undefined | 做好空值判断，给默认值 |

</details>

---

<details open>
<summary><strong>🤝 协作相关</strong></summary>

| 问题 | 原因 | 解决方案 |
|:---|:---|:---|
| 代码风格不统一 | 没有规范 | 用 ESLint/Prettier/Black，配置统一 |
| PR 太大难 review | 改动太多 | 小步提交，一个 PR 一个功能 |
| 文档过时 | 没人维护 | 代码和文档一起改，CI 检查 |
| 不知道谁负责 | 没有 owner | 用 CODEOWNERS 文件 |
| 重复造轮子 | 不知道有现成的 | 建立内部组件库/文档 |

</details>

1. **看错误信息** - 完整复制给 AI
2. **最小复现** - 找到最简单能复现问题的代码
3. **二分法** - 注释一半代码，定位问题范围
4. **换环境** - 换浏览器/终端/设备试试
5. **重启大法** - 重启服务/编辑器/电脑
6. **删掉重来** - 环境乱了就删掉重建虚拟环境

---

## 🔥 终极解决方案

实在搞不定？试试这个提示词：

```
我遇到了一个问题，已经尝试了很多方法都没解决。

错误信息：
[粘贴完整错误]

我的环境：
- 操作系统：
- Python/Node 版本：
- 相关依赖版本：

我已经尝试过：
1. xxx
2. xxx

请帮我分析可能的原因，并给出解决方案。
```

---

## 📝 贡献

遇到新坑？欢迎 PR 补充！
