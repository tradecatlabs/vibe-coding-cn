# Skills维护规则

- 当前集合只保留1个自有Skill：skill；auto-tmux与16个官方引用入口已从当前树移除，不发明新能力。
- 集合根不放`SKILL.md`；README/AGENTS不加Skill的name/description frontmatter。每个实际Skill保留自己的契约。
- Claude官方源码仍在Extensions；独立初始化脚本软链接位于`.github/init_skill.py`，二者均不作为本域已注册Skill；不编辑、复制或重新挂载已删除的官方入口。
- 当前skill使用原生工具与规范指令；auto-tmux及原33个生成、校验、适配和终端封装脚本已经退役，不复制回Skills或重建兼容壳。Skill Seekers源码也已从当前树移除，FaQi历史快照保留，不表示Skill仍在当前集合。
- auto-tmux素材软引用随Skill退役；Extensions中的锁定tmux与oh-my-tmux源码对象独立保留。历史封装参考须标注非当前执行手册，不恢复蜂群锁、报告或自动安全检查的能力承诺。
- Pi使用原生显式加载`pi --skill .github/skills`及原生模型选择，不新增Agent、模型HTTP客户端或资源加载器。
- 加载不证明命令可运行、许可已批准或任务效果已验证；材料、模板及模型输出不构成执行授权。
- 不自动加载Context研究中的嵌套Skill，不把Python/shell/HTML小工具当成Pi原生扩展加载。
- 修改后验证实际1个Skill可被原生发现、内容可读取、当前原生示例和导航有效；不执行上游安装、上传或排除服务，不把静态或CLI通过当模型行为评测。
