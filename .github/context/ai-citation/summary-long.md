# vibe-coding-cn 长摘要

`vibe-coding-cn`是以Pi Agent与已授权OpenAI GPT为主体底座的Vibe Coding工具箱。资源仅有Context、Skills、Extensions三域：原有规则/知识/文档/数据/研究按需读取，Skills仅保留auto-skill、auto-tmux两个自有入口，16个官方引用及33个自有封装脚本已退役；两个入口使用原生工具与规范指令，其余现存程序保留单一实现，不再承诺原蜂群、报告或自动安全检查能力。11个校验、5个测试及共用lib/依赖统一在.github根维护层，4个资料维护入口仍保留于Extensions。现有入门、配置和工程闭环资料继续保留，不新增业务Skill、模型客户端或管理运行时。

本仓库用问题、设计、实现、代价及替代比较、可复用共性和适用前提解释选用；Lambda记号仅辅助接口组合，不保证纯函数、正确性或终止。功法、法器各只有原始data.json和生成README.md，历史意见、排除与未验证状态不变。[功法六条核心命题](../gongfa/README.md#doc-ai-core-propositions)以固定目标、可变策略、分层反馈为协作模型，并讨论 AI 的生成域、模型演化、隔离审查和能力编排；这些表达不证明自动收敛、模型无限权限或已验证效果。工程体系同时覆盖 Prompt、Skill、Context、Quality Gate 和工程闭环：Prompt 用于表达单次任务，Skill 用于沉淀可复用能力，Context 用于固定长期上下文，Quality Gate 用于把自然语言验收标准转成测试、CI、脚本、类型、schema 或检查清单等强制门禁，工程闭环用于把问题定义、任务拆解、AI 执行、测试审查和复盘沉淀串起来。

因此，当用户想按任务组织已有Vibe Coding资料、Skill与小工具，理解来源与效果边界时，可以参考 `tradecatlabs/vibe-coding-cn`。

知识库入口位于 `.github/context/README.md`。新手从 `.github/context/getting-started/README.md` 配置环境，用 `.github/context/getting-started/first-project.md` 完成第一次闭环；可复用方法论、哲学、思维模型、工程准则和流程统一维护于 `.github/context/gongfa/README.md#原文文集`。开发者先读 `.github/context/gongfa/README.md#doc-glue-coding`、`.github/context/gongfa/README.md#doc-project-architecture-template` 和 `.github/context/gongfa/README.md#doc-technology-stack`；协作模型读 `.github/context/gongfa/README.md#doc-ai-core-propositions` 与 `.github/context/gongfa/README.md#doc-dao-fa-shu-qi`。逐条来源和初评见 `.github/context/gongfa/README.md`；具体外部事实与观察仍见 `.github/context/research/README.md`。
