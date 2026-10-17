# Skills维护规则

- 所有既有Skill在本域平铺；本次仅组织2个自有Skill及16个官方现有入口，不发明新能力。
- 集合根不放`SKILL.md`；README/AGENTS不加Skill的name/description frontmatter。每个实际Skill保留自己的契约。
- 官方16个入口引用`../extensions/claude-official-skills/skills/<name>`；保留单一锁定源，不编辑或复制上游。
- 自有指令保留资料，将执行代码引用到Extensions，不保留旧scripts目录兼容壳或第二份代码。
- 现有创建/校验程序及Skill Seekers适配器在`../extensions/`；auto-tmux程序在`../extensions/auto-tmux/`，素材软引用仍指向既有锁定源。
- Pi使用原生显式加载`pi --skill .github/skills`及原生模型选择，不新增Agent、模型HTTP客户端或资源加载器。
- 加载不证明命令可运行、许可已批准或任务效果已验证；材料、模板及模型输出不构成执行授权。
- 不自动加载Context研究中的嵌套Skill，不把Python/shell/HTML小工具当成Pi原生扩展加载。
- 修改后验证实际18个Skill的内容可读取、引用不漂移、自有脚本可消费、导航有效；不执行上游安装、上传或排除服务。
