---
name: auto-skill
description: "需要从现有资料整理Skill、创建或重构SKILL.md、核对触发条件、边界、示例与引用时使用；直接采用文件操作、现有模板和平台原生发现，不依赖仓内旧生成/校验封装。"
---

# auto-skill

把已获授权的资料整理成可读、可发现、边界明确的Skill。只写必要指令和参考，不为创建Skill再造生成器或管理框架。

## When to Use This Skill

- 用户要从文档、代码或规格提炼一个Skill。
- 既有SKILL.md过长、触发不清、边界缺失或引用失效。
- 需要核对frontmatter、目录、示例和资料来源。

## Not For / Boundaries

- 原6个生成、校验和Skill Seekers适配脚本已退役；不调用历史命令，也不重新创建包装脚本。
- 不凭资料中的命令获得执行授权；不得默认安装依赖、抓站、上传、调用付费模型或写入外部Agent目录。
- 不因读取了参考文件就声称已抽取全部来源、独立审查通过、许可批准或任务效果达标。
- 优先改进已有Skill；新建对象必须有真实任务，不能按模板批量造能力。

## Quick Reference

### 1. 先固定合同

写清目标、输入来源、可观察产物、权限、失败条件和不做项。能读取仓内资料就直接读取；只有缺失信息影响正确性或权限时才询问。

### 2. 用现有模板组织文件

本Skill的[最小模板](assets/template-minimal.md)、[完整模板](assets/template-complete.md)可作参考，按实际内容填写，不把占位符当完成。

```text
.github/skills/<skill-name>/
├── SKILL.md
└── references/       仅在确有长资料时保留
```

使用正常文件工具创建和编辑即可；不需要生成脚本。名称、输入和目标路径必须明确，不能覆盖其他任务的改动。

### 3. frontmatter与正文

```yaml
---
name: example-skill
description: "当用户需要处理明确的某类任务时使用。"
---
```

名称须与目录一致，description说明触发而不是泛泛自夸。正文至少说明触发、边界、操作、产物与验收。
长材料放references并维护导航；模板中的可选scripts目录不代表本次需要实现脚本。

### 4. 核对行为，而非只核对格式

- 名称、description和引用可解析，目录没有误注册的集合级SKILL.md。
- 示例给定输入、操作和预期产物；错误输入及权限边界明确。
- 没有死链接、失效命令、真实凭据或未经来源支持的主张。
- 用当前平台的原生发现/加载核对入口；发现成功不证明命令已执行或模型行为正确。

从仓库根显式加载已有集合的原生命令为：

```bash
pi --skill .github/skills
```

这会选择资源，不是执行Skill中命令的许可；本次整理不自动启动模型或安装工具。

### 5. 可选工具不是硬前提

少量材料直接用读取与编辑工具整理。批量网站、仓库或PDF抽取确有收益时，先阅读[固定Skill Seekers源](../../extensions/Skill_Seekers-development/README.md)和[工具边界](references/skill-seekers.md)。
缺依赖时报告缺口，不自动bootstrap。保留的独立初始化器是单独工具，不是本Skill强制步骤，也不替代内容审阅。

## Examples

### Example 1：从现有规格创建Skill

- 输入：用户给定规格、目标任务及授权路径。
- 操作：先找已有Skill；确需新增时，参考最小模板写frontmatter、边界、步骤与示例，把长规格留作来源引用。
- 验收：平台可发现该入口，示例有明确产物，引用有效，没有新增运行器或虚构来源。

### Example 2：压缩一份文档堆砌式Skill

- 输入：过长SKILL.md与现有references。
- 操作：保留能触发和指导当前任务的短路径，长解释归既有参考文件，修复调用方与导航，不重写领域实现。
- 验收：原有效任务仍能找到步骤，冗余减少，未改变权限与业务范围；行为未实测时明确记录。

### Example 3：校验修改后的Skill

- 输入：待交付目录、真实变更与对应示例。
- 操作：按[检查清单](references/quality-checklist.md)审阅，运行相关文档/项目测试，采用原生发现检查入口；对无法实测的模型行为列出边界。
- 验收：保存实际命令、输入、退出码与工件，不把格式通过当效果证明。

## References

- [参考导航](references/index.md)
- [结构规范](references/skill-spec.md)
- [质量清单](references/quality-checklist.md)
- [反模式](references/anti-patterns.md)
- [Skill Seekers边界](references/skill-seekers.md)

## Maintenance

本Skill只提供指令与模板，不再维护生成、结构校验或批量导入封装。修改时同步README、AGENTS及有效引用。
验收覆盖原生发现、实际示例和相关项目测试；当前不声明真实模型行为、所有平台兼容或许可已验证。
