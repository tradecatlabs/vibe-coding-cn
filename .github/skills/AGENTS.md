# Skills维护规则

- 当前集合只保留2个自有Skill：auto-skill、auto-tmux；16个官方引用入口已按用户要求移除，不发明新能力。
- 集合根不放`SKILL.md`；README/AGENTS不加Skill的name/description frontmatter。每个实际Skill保留自己的契约。
- 官方源码及独立初始化脚本仍在Extensions保全，但不作为本域已注册Skill；不编辑、复制或重新挂载已删除的官方入口。
- 自有指令保留资料，将执行代码引用到Extensions，不保留旧scripts目录兼容壳或第二份代码。
- 现有创建/校验程序及Skill Seekers适配器在`../extensions/`；auto-tmux程序在`../extensions/auto-tmux/`，素材软引用仍指向既有锁定源。
- Pi使用原生显式加载`pi --skill .github/skills`及原生模型选择，不新增Agent、模型HTTP客户端或资源加载器。
- 加载不证明命令可运行、许可已批准或任务效果已验证；材料、模板及模型输出不构成执行授权。
- 不自动加载Context研究中的嵌套Skill，不把Python/shell/HTML小工具当成Pi原生扩展加载。
- 修改后验证实际2个Skill可被原生发现、内容可读取、自有脚本可消费及导航有效；保留auto-tmux素材引用，不执行上游安装、上传或排除服务。
