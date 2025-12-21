# “声明式配置（declarative configuration）”。

解释
- 声明式：你只需要在一个 JSON（或 YAML、TOML 等）文件里 描述目标状态（比如 VS Code 的主题、快捷键、扩展、代码风格等），而不是写一堆命令去逐步告诉程序怎么做到。
- 配置即代码（Configuration as Code）：VS Code 把所有的自定义选项都集中在 settings.json、keybindings.json 等文件里，这样不仅能高度自定义，还能方便共享、版本控制。
- 优点：
  - 可读性和可维护性强（配置集中在文件中）
  - 跨设备同步方便（直接拷贝配置文件或用 git 管理）
  - 自动化（可以写脚本一键部署开发环境）

类似的叫法
- “基于 JSON 的配置系统”（强调格式）
- “配置即代码”（Configuration as Code, CaC）（强调可以管理和复用）
- “声明式配置”（强调描述目标而不是步骤）
