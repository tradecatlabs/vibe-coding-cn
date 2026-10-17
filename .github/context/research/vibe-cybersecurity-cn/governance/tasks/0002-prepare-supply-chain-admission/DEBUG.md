# 准入校验器临时目录血缘测试失败

## Observe

- 命令：`python3 -m unittest governance/tasks/0002-prepare-supply-chain-admission/test_validate_admission_candidates.py`
- RED-1：active-high 负例先命中“非 MVP”，说明最初 fixture 同时改变了两个变量。
- RED-2：改为只把真实 MVP `subfinder` 改成 active-high 后，预期异常仍未出现。

## Hypotheses

- H1（ROOT）：研究目录相对路径绑定全局 `ROOT`，忽略测试替换后的 `ADMISSION_PATH`。
- H2：测试修改没有写入临时 source JSON；写入逻辑和 JSON 均为非空，证据不支持。
- H3：active-high 分支顺序被其他门禁遮蔽；第二个 fixture 只改变网络级别，证据不支持。

## Experiment

- 预测：如果 H1 成立，把 source path owner 从 `ROOT` 改为 `ADMISSION_PATH.parent` 后，同一个负例会命中 active-high，其他五个测试继续通过。
- 最小改动：只替换相对路径解析基准，不改变生产目录的实际解析结果。

## Root Cause

`validate()` 读取准入 JSON 时允许替换 `ADMISSION_PATH`，但解析 `source_catalog` 却固定使用模块 `ROOT`；测试和未来迁移目录无法让准入目录与其研究血缘一起移动。

## Fix

相对 `ADMISSION_PATH.parent` 解析 `source_catalog`，使配置文件拥有自身相对引用的生命周期。

## Regression Evidence

- Pre-fix RED：6 tests 中 active-high 负例未触发，`FAILED (failures=1)`。
- Post-fix GREEN：重新运行同一命令，必须得到 6 tests `OK`。
- 敏感性：`test_active_high_research_candidate_is_rejected` 只修改真实 MVP 的 `network_effect`；若恢复旧 `ROOT` 解析，它会再次失败。
