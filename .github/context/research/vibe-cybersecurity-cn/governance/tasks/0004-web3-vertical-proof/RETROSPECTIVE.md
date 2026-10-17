# Engineering Retrospective (0004 Web3 纵向闭环)

状态：本地 sealed draft；未获得受信外部 review，未签发 canonical handoff。

## 做对了什么

- 事实：先定切片（EVM/Solidity + 本地靶场）再动手，闭环一次性跑通；
  Foundry 攻击测试 4/4 复现，Slither 命中 2 项、Echidna 找到溢出反例。
- 证据：`web3-lab/evidence/`（forge-test 日志、slither JSON、echidna 反例、findings 账本）。
- 为什么有效：用 ground truth 靶场先行，把"工具召回率"与"实证结论"解耦，
  静态候选无法冒充实证。
- 可复制条件：工具固定版本、命令写入 README、证据校验器强制 artifact 存在。
- 不适用边界：教学级合约，不代表真实协议复杂度。

## 做错了什么

- 事实：首次 Slither 运行失败（forge 不在 PATH、solc 0.8.35 未安装），
  首次 Echidna JSON 输出为空文件。
- 影响：多花了约两次工具调用；证据目录曾出现 0 字节文件。
- 根因：工具链前置条件（PATH、solc-select 版本安装）未在首次运行前收敛；
  echidna 的 `--format json` 实际把文本日志和 JSON 都写到 stdout。
- 为什么没有提前发现：未先读 echidna 输出契约文档，依赖了旧版行为假设。
- 是否重复发生：未重复；后续以版本输出和真实 artifact 为准。

## 重新来一遍怎么做

- 行动：写工具链运行脚本（PATH/venv/solc-select 一次性收敛）并固定版本清单。
  Owner：工程组。Due：下一任务开始前。验证：脚本可从头复跑闭环。
- 行动：任何新工具接入先跑 `--help` 与最小样例，验证输出契约再进入证据链。
  Owner：工程组。Due：持续。验证：证据校验器拒绝空 artifact。

## 经验寿命

- 适用范围：本项目 Web3 工具链接入与证据归档。
- 失效条件：工具输出契约变更或校验器升级。
- 复查日期：2026-09-14。
