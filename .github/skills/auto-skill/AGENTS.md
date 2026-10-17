# auto-skill维护规则

本Skill保留既有元技能：将文档、API、代码或规格整理为可复用Skill，并校验激活条件、边界、示例和质量。领域资料不是本Skill自身的新能力。

## 文件职责

- `SKILL.md`：原触发、交付、工作流和质量门禁。
- `assets/template-minimal.md`、`assets/template-complete.md`：原通用模板；不改写官方Skill标准或把模板样例当已实现工具。
- `references/index.md`、`references/README.md`：本Skill导航和原参考说明。
- `references/skill-spec.md`、`quality-checklist.md`、`anti-patterns.md`：原规格、检查清单和常见反模式。
- `references/skill-seekers.md`：现有Skill Seekers工作流与副作用边界。

本目录不再放执行脚本或重复源码别名。单一实现位于`.github/extensions/`：
`create-skill.sh`、`validate-skill.sh`、`skill-seekers.sh`、`skill-seekers-bootstrap.sh`、
`skill-seekers-import.sh`、`skill-seekers-update.sh`；固定源码在同域`Skill_Seekers-development/`。

## 契约

- 保留可判定触发、MUST/SHOULD/NEVER边界、简短Quick Reference、可复验示例及references导航。
- 不编造资料外的事实；不确定时说明缺口与查证路径。具体领域知识归相应Skill或Context，不塞进本元技能。
- 新Skill遵循原name/description规范；通用模板可有可选scripts样例，本仓实际执行实现仍遵循统一Extensions归属。
- bootstrap会安装依赖，抓取/增强/上传可能联网；需要具体任务授权，不为本次迁移自动执行。
- update适配器禁止覆盖固定来源，`--dry-run`仍下载和解压，不是零副作用。Gitlink更新单独核对修订、来源和旧记录。
- 修改后先运行对应`validate-skill.sh --strict`及真实调用相关测试；最终完整`make test`按根AGENTS时机执行。
