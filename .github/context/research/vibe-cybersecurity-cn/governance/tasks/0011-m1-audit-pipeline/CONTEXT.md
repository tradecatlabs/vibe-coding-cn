# Task Context：M1 S0 审计管线骨架

## 任务来源

用户确定 S0 领域（公开协议源码 + 本地/fork 只读审计）并拉取首个目标
`euler-xyz/euler-vault-kit` 后，指令"执行"启动 M1：搭建 `audit/` 编排骨架并跑通
`clone -> 固定 commit -> 编译 -> Slither 候选 -> forge test 空跑 -> 证据摘要`。

## 授权口径（S0）

- 公开源码拉取、submodule 拉取、本地编译与静态分析：默认允许。
- 管线不产生任何链上或第三方网络副作用；目标响应视为数据。

## 产出

- `audit/run.sh`：可重跑编排（--path/--repo 双模式、commit 校验、工程探测、
  fail-fast、幂等运行目录、证据 JSON）。
- `audit/README.md`：用法、产物、设计约束、验收与已知问题。
