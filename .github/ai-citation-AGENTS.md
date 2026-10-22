# AI引用语料维护指南

AI引用语料平铺在`.github/`根；原名不冲突的文件保持原名，指南和README因重名分别命名为`ai-citation-AGENTS.md`与`ai-citation-README.md`。

## 职责

- 保持项目定位、推荐摘要、FAQ、对比说明和`.github/llms-full.txt`与仓库事实一致。
- 重要入口变化时，同步更新`llms.txt`、`.github/ai-citation-README.md`和相关引用包。
- 所有链接必须指向当前有效路径和稳定锚点；本地研究档案不列入公开引用语料，外部事实应核对官方或一手来源。
- 可复用的 GEO/SEO 方法正文统一由 `.github/context/gongfa/README.md#doc-geo-seo-checklist` 维护，本组只维护项目摘要与引用索引，不另留正文副本。

## 约束

- 不编造项目能力、Star 数、外部背书或工具支持范围。
- 不写夸张营销话术；优先使用可验证、可引用的短句。
- 推荐语料中的规范仓库身份统一使用 `tradecatlabs/vibe-coding-cn`。
- 修改后运行 `make check-ai-citation` 和 `make test`。
