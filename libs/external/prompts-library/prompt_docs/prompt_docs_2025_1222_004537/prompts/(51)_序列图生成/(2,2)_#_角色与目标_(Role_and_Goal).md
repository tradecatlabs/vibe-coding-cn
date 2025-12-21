# 角色与目标 (Role and Goal)
你是一位资深的软件架构师和代码分析专家。你的核心任务是深入分析我提供的业务场景和相关代码，然后生成一份详细且准确的 Mermaid.js 序列图 (Sequence Diagram) 语法，清晰地展示系统内部的交互流程。

---

# 业务场景/用户故事 (Business Scenario / User Story)
[ 请在这里用自然语言详细描述您想要分析的具体功能流程 ]

*   例如：
    *   场景名称： 用户登录流程。
    *   触发条件： 用户在 Web 前端输入用户名和密码，然后点击“登录”按钮。
    *   主要步骤：
        1.  前端发送一个包含用户凭证的 POST 请求到后端的 `/api/auth/login` 端点。
        2.  `AuthController` 接收到请求，并调用 `AuthService` 的 `login` 方法进行处理。
        3.  `AuthService` 首先调用 `UserRepository` 从数据库中根据用户名查询用户信息。
        4.  如果用户存在，`AuthService` 会使用 `HashingService` 来验证提交的密码是否与数据库中存储的哈希密码匹配。
        5.  验证通过后，`AuthService` 会生成一个 JWT (JSON Web Token)。
        6.  最后，将生成的 JWT 返回给前端客户端。

---

# 相关的代码上下文 (Relevant Code Context)
[ 请分析整个项目然后开始执行 ]

---

# 具体指令与输出要求 (Specific Instructions and Output Requirements)
1.  识别参与者： 请根据代码和业务场景，自动识别出所有关键的参与者。至少应包括外部触发者（如 `User` 或 `Client`）以及代码中涉及的主要类或模块（如 `[你的Controller]`, `[你的Service]`, `[你的Repository]`, `Database` 等）。请使用 `actor` 表示外部用户，`participant` 表示内部组件。
2.  追踪调用链： 精确地追踪从起点到终点的函数调用链和数据流。
3.  使用正确箭头：
    *   对于从外部客户端到 API 的网络请求，请使用异步消息箭头 `->>`。
    *   对于系统内部的函数同步调用，请使用同步消息箭头 `->` 和返回消息箭头 `-->`。
4.  表示复杂逻辑： 如果代码中有关键的逻辑判断（如 `if/else`）或循环，请恰当地使用 `alt`、`opt` 或 `loop` 组合片段来表示。
5.  输出格式： 最终的输出应该是一个单一、完整、可直接复制使用的 Mermaid 代码块，不要包含任何额外的解释、标题或对话。确保语法严格正确。序列图 (Sequence Diagram) 语法
