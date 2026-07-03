# openai/codex 研究分析

## 本轮结论

- OpenAI Codex 是官方 terminal coding agent 源码，属于 P1 核心研究对象。
- 仓库采用 Rust core、CLI、SDK、docs、Bazel/Nix/PNPM 等多工具组合，体现了生产级 agent 工具链的复杂度。
- 本仓应重点研究其权限、沙箱、命令执行、AGENTS.md 读取、CLI 分发和 SDK 边界。

## 本地证据

- 研究对象：`openai/codex`
- 当前研究角色：官方 coding agent 工具源码
- 本轮成熟度：L1 初步理解
- 原始仓库：`raw/repository/`
- 原始来源清单：`raw/sources.yml`
- 事实摘要：`domain.yml`

## 结构观察

- 根目录包含 `codex-rs/`、`codex-cli/`、`sdk/`、`docs/`、`AGENTS.md`、`justfile`、`package.json`、`pnpm-workspace.yaml`、`BUILD.bazel`。
- README 聚焦 Codex CLI 安装、运行和 Docs 入口。
- 存在 `.codex/`、`.devcontainer/`、Bazel、Nix 等开发环境和构建基础设施。

## 可借鉴点

- 官方 agent 工具把本地运行、权限边界、CLI 交互和项目规则文件作为核心能力。
- Rust core + CLI 包装适合研究高可靠本地工具的工程形态。
- `AGENTS.md` 作为项目规则入口与本仓方向高度一致。

## 风险和边界

- 官方产品快速演进，结论容易过期。
- 仓库构建系统复杂，不能只读 README 下结论。
- 需要区分 Codex CLI、本地 app、Web/Cloud Codex 等产品边界。

## 下一轮研究任务

- 重点阅读 `codex-rs/` 中命令执行、sandbox、approval、config、project docs 相关代码。
- 整理 Codex 的本地 agent safety model 到 references。

## 沉淀判断

- 本轮只完成 L1 理解，不直接迁入 concepts、references、workflow 或 skills。
- 只有经过 L2 源码阅读、实验验证或交叉对照后的结论，才进入稳定层。