# Public release review

## Scope

本次公开仓审查覆盖：

- ProblemContract v1、CandidateObservation 隔离、ResearchBundle 只读派生和 failed-route schema；
- 可移植 active skills、41-family 工具成熟度 registry、两列工具目录、bounded canary 与 SMT/SymPy fixture；
- 文献 provider registry、固定供应链 reference、候选路径/artifact digest 校验和公开边界门。

公开仓不携带候选 raw、动态快照、研究 records、运行报告、prompt/reasoning、凭据、机器身份、私有路径或内部供应链报告。

## 结论

`make check`、公开边界校验、Python 编译检查、治理 strict/health 和新增攻击回归通过。当前 canonical Problem、Attempt、Result 和 Solution View 业务记录保持为空；这表示没有发布未经验证的数学成果，不表示开放问题已经解决。

工具 registry 的成熟度是公开契约状态，不是某台机器的安装报告。没有公开运行证据的工具保持 `surveyed` 或 `source_locked`；canary 只测试合成 bounded runtime 行为，不创建数学 Result。

## 已知边界

- `make check-full` 需要调用者本地提供被忽略的来源缓存、候选 raw 或电子书；缺少这些材料时应保持失败，不能用空目录伪造完整性。
- `Lean kernel check` 只覆盖固定 fixture，仍需公理/逃逸和 statement-faithfulness 审查。
- `answered`、`resolved`、`solved` 等来源标签不映射为数学结论；CandidateObservation 不得创建 Attempt、Result 或 Solution。
- 外部 solver、CAS、Git、HTTP 和 canary 任务必须设置 timeout、预算、停止条件、输出/响应上限和失败语义。

## Recheck

```bash
make check
python3 scripts/validate_public_boundary.py --project-root .
python3 scripts/validate_math_tool_maturity.py
python3 governance/tools/validate_governance_package.py --project-root . --strict
```

发布地址：[vibemathing/vibe-mathing-cn-public](https://github.com/vibemathing/vibe-mathing-cn-public)。
