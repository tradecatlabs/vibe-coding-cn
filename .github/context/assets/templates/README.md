# .github/context/assets/templates

本目录用于存放可复用模板附件。

稳定知识正文放在 `.github/context/`，模板文件放在本目录；引用模板时应在对应文档中给出入口。

## 模板登记

| 模板 | 版本 | 状态 | 范围 |
|---|---|---|---|
| [工具解释模板](tool-explanation-template-v0.md) | `v0` | 历史模板，仅供追溯 | 法器与功法旧说明；15项原名原序 |
| [工具解释模板](tool-explanation-template-v1.md) | `v1` | 当前使用 | 保留v0的15项，新增第16–18项“结论、连接规则、依据”；每个对象独立使用一张严格Markdown表格 |

模板正文仅在链接目标中维护。功法与法器的唯一活动说明载荷为`data.json.explanations_v1`，绑定v1模板SHA；v0不作为活动或兼容载荷。
