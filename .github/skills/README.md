# Skills：既有指令与流程

## 字多不看

现有18个Skill统一放在这里：2个自有Skill和16个官方既有Skill；本次没有新增业务Skill。
指令属于Skills，程序实现属于[Extensions](../extensions/README.md)，规则和知识参考属于[Context](../context/README.md)。

<a id="当前保留"></a>

## 快速导航

| 来源 | 既有Skill |
|---|---|
| 自有 | [auto-skill](auto-skill/SKILL.md)、[auto-tmux](auto-tmux/SKILL.md) |
| 官方 | [algorithmic-art](algorithmic-art/SKILL.md)、[brand-guidelines](brand-guidelines/SKILL.md)、[canvas-design](canvas-design/SKILL.md)、[doc-coauthoring](doc-coauthoring/SKILL.md) |
| 官方 | [docx](docx/SKILL.md)、[frontend-design](frontend-design/SKILL.md)、[internal-comms](internal-comms/SKILL.md)、[mcp-builder](mcp-builder/SKILL.md) |
| 官方 | [pdf](pdf/SKILL.md)、[pptx](pptx/SKILL.md)、[skill-creator](skill-creator/SKILL.md)、[slack-gif-creator](slack-gif-creator/SKILL.md) |
| 官方 | [theme-factory](theme-factory/SKILL.md)、[web-artifacts-builder](web-artifacts-builder/SKILL.md)、[webapp-testing](webapp-testing/SKILL.md)、[xlsx](xlsx/SKILL.md) |

<details>
<summary><strong>完整细粒度目录（点击展开/收起）</strong></summary>

- [使用方式](#使用方式)
- [正文](#正文)
- [来源与单一实现](#来源与单一实现)
- [发现与信任边界](#发现与信任边界)

</details>

## 使用方式

Pi默认不会发现`.github/skills/`。从仓库根使用原生显式资源加载：

```bash
pi --skill .github/skills
```

加载前检查当前Pi版本、项目信任、技能来源、依赖、许可及适用范围；模型通过Pi原生选择使用已授权的OpenAI GPT，不随仓保存授权配置。
显式加载是让原生加载器发现Skill，不等于安装依赖、执行其中命令或验证任务效果。

## 正文

### 来源与单一实现

16个官方入口指向同一个固定[上游树](../extensions/claude-official-skills/README.md)，不复制或修改官方源。
`theme-factory`仍是原内容设计Skill，不是新增Pi界面主题。现有官方初始化脚本入口在`../extensions/init_skill.py`，也是对原上游的引用。

自有Skill保留原有assets与references；执行脚本分别在Extensions域根和`../extensions/auto-tmux/`。
创建和校验仍使用原`create-skill.sh`、`validate-skill.sh`，没有增加资源加载器或管理框架。

### 发现与信任边界

集合根不放`SKILL.md`，README和AGENTS不含Skill frontmatter；否则Pi可能停止向下发现或把治理文档当Skill。
不要递归加载Context研究材料里的嵌套Skill，也不要把整个Extensions交给`-e`。
WSL/Linux引用经当前环境核对；原生Windows链接权限与发现行为须单独验证，不能从UNC可访问推断兼容。
