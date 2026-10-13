# Engineering Retrospective (0005 Web3 工具链准入与验证控制面)

状态：本地 sealed draft；未获得受信外部 review，未签发 canonical handoff。

## 做对了什么

- 事实：5 项工具 9 门禁全过并 admitted；Echidna 属性覆盖 4 漏洞全部找到反例；
  git 基线建立后验证控制面 enforce 一次通过。
- 证据：`ADMISSION_TABLE.md`、`web3-lab/evidence/echidna-*-2026-08-14.log`、
  `validate_task_verification.py` 输出（enforced=True, ready=True）。
- 为什么有效：先固定版本再准入，先建属性再升级门禁，证据先于状态声明。
- 可复制条件：门禁绑定真实命令输出；git digest 绑定当前提交。
- 不适用边界：admitted 只覆盖本地靶场验证，不涵盖真实协议审计效果。

## 做错了什么

- 事实：Echidna 的 `balanceContract` 配置导致部署失败，浪费多次试错；
  第一个预言机属性反例是属性模型缺陷（卖出未扣净投入）而非真实漏洞。
- 影响：约 6 次工具调用往返；属性基线一度不可信。
- 根因：未先验证 Echidna 配置契约（balanceContract 机制）就写完整配置；
  属性模型未先做守恒推演。
- 为什么没有提前发现：首次部署失败信息不完整，未立即查配置文档。
- 是否重复发生：未重复；后续以最小配置先跑通再扩展。

## 重新来一遍怎么做

- 行动：接入新工具先以最小配置验证部署与调用契约，再写完整配置。
  Owner：工程组。Due：持续。验证：Echidna 属性基线复跑一次通过。
- 行动：属性模型先做守恒推演（买入/卖出对净投入的影响）再编码。
  Owner：工程组。Due：下一属性任务前。验证：属性反例与 ground truth 语义一致。

## 经验寿命

- 适用范围：本项目 Echidna 属性与工具接入。
- 失效条件：Echidna 版本行为变更或属性模型重构。
- 复查日期：2026-09-14。
