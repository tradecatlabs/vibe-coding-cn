# affaan-m/ECC 深度研究

## 研究级别

- 当前级别：L2 Harness、技能和配置生命周期研究。
- 研究对象：affaan-m/ECC。
- 证据来源：本目录 raw/ 下的 README、.codex、.codex-plugin、manifests、skills、hooks、rules、contexts 和 scripts。
- 观察日期：2026-09-08。

## L2 结论

ECC 的结构把可复用能力、持久规则、上下文、会话钩子、安装清单和工具适配拆开；README 还区分 Codex 原生 plugin 与 legacy sync。这个分层与本仓需求直接相关：配置分发不是复制几个文件，而是一个拥有来源、版本、备份、所有权、迁移和卸载边界的生命周期。

## 关键机制

### Manifest 驱动安装

manifests/install-components.json、install-modules.json 和 install-profiles.json 把安装选择从脚本逻辑中抽出，便于审查组件组合和提供最小 profile。

### Codex 双路径

.codex-plugin/ 表示原生插件路径，scripts/codex/ 下的 legacy sync 则处理兼容配置合并。两者的所有权和回滚责任不同，不能在用户文档中混为一谈。

### Hook 生命周期

hooks/ 和 scripts/hooks/ 覆盖 session start/end、配置保护、成本跟踪、质量 gate、文档提示、类型检查和 tmux 提醒。Hook 的优势是自动化，风险是隐式改变每次会话行为。

### 记忆与上下文

contexts/、memory-persistence 和 session 相关脚本说明跨会话记忆需要边界、裁剪、保留期限和隐私处理，不能把所有对话永久注入上下文。

### 安全审查

仓库有 security guide、gitleaks、配置保护和权限相关材料，但外部仓库的存在不构成对每个脚本的信任证明。

## 可迁移模式

- 为 .github/tools/config/.codex 设计备份目录、manifest、dry-run、restore 和版本记录。
- 将本仓 skill 的通用规则与项目 AGENTS 分开。
- 对 hook 和全局配置默认采用最小 profile。
- 将性能、质量和安全指标分别记录，避免一个分数掩盖风险。

## 迁移边界

- 本仓不安装 ECC，也不启用其 hook。
- 不把外部规则当作当前项目 AGENTS 的更高优先级。
- 所有配置实验必须在临时用户目录或隔离项目验证。

## L3 验证任务

1. 比较本仓 .github/tools/config/.codex 一键配置需求与 ECC manifest/legacy sync 的边界。
2. 设计不执行副作用的配置安装 dry-run 输出。
3. 为恢复脚本增加“只恢复自己拥有字段”的负例验证。
