# Skills：既有指令与流程

## 字多不看

当前只保留1个自有Skill：`skill`。`auto-tmux`及16个官方引用入口已从当前树移除，没有新增业务Skill。
指令属于Skills，程序实现属于[Extensions](../extensions/README.md)，规则和知识参考属于[Context](../context/README.md)。

<a id="当前保留"></a>

## 快速导航

| 来源 | 既有Skill | 职责 |
|---|---|---|
| 自有 | [skill](skill/SKILL.md) | 将资料整理为可复用Skill，维护结构与质量 |

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

本集合不再提供官方Skill引用入口。Claude锁定上游源码仍在Extensions；独立初始化脚本软链接已移至`.github/init_skill.py`，不属于当前Skills发现集合。Skill Seekers源码已按用户要求从当前树退役，历史来源仍留在FaQi资料中。
此前官方入口清理只删除16个软引用，没有删除、复制或改写上游源码；auto-tmux及原33个自有封装脚本已从当前树退役。

当前skill只提供原生工具和规范指令。历史封装参考不再是执行手册，不把实现复制回Skills，也不新增包装程序、资源加载器或管理框架。

### 发现与信任边界

集合根不放`SKILL.md`，README和AGENTS不含Skill frontmatter；否则Pi可能停止向下发现或把治理文档当Skill。
不要递归加载Context研究材料里的嵌套Skill，也不要把整个Extensions交给`-e`。
WSL/Linux引用经当前环境核对；原生Windows链接权限与发现行为须单独验证，不能从UNC可访问推断兼容。
