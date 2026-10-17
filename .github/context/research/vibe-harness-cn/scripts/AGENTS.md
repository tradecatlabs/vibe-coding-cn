# scripts 目录

`scripts/` 只保存可重跑的薄自动化入口，优先组合标准库与成熟依赖，不拥有领域契约。

```text
scripts/
├── AGENTS.md
├── sync_upstreams.sh         # 同步官方 GitHub Harness checkout 并刷新 revision lock
├── validate_harness.py        # Harness、Operator Pack/Runtime Core 与参考库 Profile 的统一 CLI
├── validate_operator_library.py # 校验 Core Schema、Profile 精确覆盖、引用和路径
├── validate_harness.py.lock   # uv 生成的完整依赖闭包与 artifact hash
└── verify_project.py          # 执行 capability registry 声明的确定性门禁
```

脚本上游是 `contracts/`，当前下游是本地开发准入。错误必须清晰并以
非零状态退出；输出不得包含凭据或完整 prompt/tool 内容。

存在性：JSON Schema 不适合清晰表达跨文件精确覆盖、唯一 ID 和引用解析，因此保留一个直接模块；最低阶梯为
`jsonschema` + 本地函数，不增加 framework、service 或 plugin。`uv` 官方 script lock 固定完整
运行依赖，验证入口是 `uv run --locked --script scripts/validate_harness.py --self-test`。

`validate_operator_library.py` 不提供第二套 CLI；它由既有入口导入。`--operator-pack` 只检查公共
Pack Core，`--operator-library` 检查本仓库 Reference Profile，`--operator-runtime` 检查 Binding、
RunRequest 与 RunRecord 的公共信封。验证只读取本地 JSON，不联网、不执行条目或 Binding，也不根据自然语言自报通过。

`verify_project.py` 只把既有命令归一化为稳定 artifact；capability、风险 profile 和 artifact
路径的真相源在 `governance/control-plane/`，脚本不得自行降低门禁。

`sync_upstreams.sh` 只消费 `research/upstreams.sources.json` 登记的官方 GitHub HTTPS origin；同一
registry 同时驱动 checkout 与 lock，重复名称/URL、不安全路径或非法字段必须 fail closed。已有
checkout 必须干净并能证明 fast-forward；浅历史不足时有界深化，origin 不匹配、detached HEAD、
真实历史改写或本地改动均 fail closed，不自动 reset 或覆盖研究现场。手工负面可见性结论必须
绑定 commit；revision 变化后统一降级为 `requires-manual-review`，不得继承旧结论。
