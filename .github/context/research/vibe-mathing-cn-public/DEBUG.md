# Debug：初次项目门禁失败

## Bug

首次运行项目验证时：

- `scripts/smoke_math.py` 在高斯积分 `1e-30` 误差阈值断言失败。
- `validate-skill.sh --strict` 报告 6 个 active skill 都缺少 `## References`。

## Environment

- Python 3.12.3
- SymPy 1.14.0
- mpmath 使用进程默认精度
- auto-skill strict validator：当前本机版本

## Reproduction

```bash
python3 scripts/smoke_math.py
for d in .codex/skills/*; do
  "$CODEX_HOME/skills/auto-skill/scripts/validate-skill.sh" "$d" --strict
done
```

## Observations

- 符号积分结果已经精确等于 `sqrt(pi)`，失败只发生在 mpmath 数值交叉检查。
- 断言要求 30 位精度，但脚本没有把 mpmath 工作精度提升到 30 位以上。
- skill 已有 `references/` 文件，但 `SKILL.md` 缺少 strict schema 要求的导航标题。

## Hypotheses

- H1（ROOT，confirmed）：mpmath 默认精度低于断言阈值，导致正确计算也无法满足 `1e-30`。
- H2（confirmed）：strict validator 按章节契约要求 `## References`，文件存在不能替代入口导航。
- H3（rejected）：SymPy 高斯积分实现错误；精确结果已经证明不是该路径。

## Experiments

1. RED：原样运行 `python3 scripts/smoke_math.py`，AssertionError。
2. 修复 H1：用 `mpmath.workdps(80)` 包住高精度积分与比较。
3. 修复 H2：给每个 active skill 增加指向现有 source-map/pressure-tests 的 `## References`。
4. GREEN：原样重跑 Reproduction 命令和项目 validator。

## Root Cause

测试阈值和数值后端精度契约未对齐；同时 active skill 的引用资产存在，但入口文档没有满足 strict validator 的导航契约。

## Fix

- 显式固定 mpmath 80 位工作精度。
- 补齐 6 个 skill 的 References 导航，不改变运行行为。

## Regression Evidence

最终同源 GREEN 命令及结果记录在本轮终态验证输出；若任一命令非零退出，本调试项保持未关闭。

---

# Debug：Wikipedia 问题列表解析为空

## Bug

首次运行 `python3 scripts/fetch_problem_library.py --refresh --delay 0.15` 时，Wikipedia API 请求成功并保存原始 JSON，但解析阶段返回 0 条并以非零状态终止：

```text
ERROR: Wikipedia 解析结果为空；页面结构可能已变化。
```

## Environment

- Python 3.12.3
- BeautifulSoup 4.12.3 + lxml 6.0.2
- 原始证据：`problem-library/raw/wikipedia/list-of-unsolved-problems.json`

## Reproduction

```bash
python3 scripts/fetch_problem_library.py --refresh --delay 0.15
```

## Observations

- API 快照约 1.2 MB，包含 `Unsolved_problems`、`Algebra` 等预期章节。
- BeautifulSoup 顶层是 `html`，`body` 只有一个直接子节点：`div.mw-content-ltr.mw-parser-output`。
- 原解析器在 `body` 的直接子节点中寻找章节，因此看不到该 `div` 内部的 `h2/h3/h4` 和列表。

## Hypotheses

- H1（ROOT，confirmed）：章节遍历根定位高了一层，应遍历 `.mw-parser-output` 的直接子节点。
- H2（rejected）：Wikipedia 章节 ID 已变化；快照中仍存在 `Unsolved_problems`。
- H3（rejected）：API 返回空正文；快照大小及章节内容证明正文完整存在。

## Experiments

1. RED：原样执行抓取器，稳定得到“Wikipedia 解析结果为空”。
2. 结构探针：打印 `body` 直接子节点和 `Unsolved_problems` 的祖先链，确认唯一额外容器。
3. 最小修复：优先选择 `.mw-parser-output` 作为遍历根，保留 `body/soup` 回退。
4. GREEN：原样重跑后从 Wikipedia 原始 JSON 解析 586 条；离线 validator 与原始快照回归测试均通过。

## Root Cause

解析器把 MediaWiki 返回片段的 `body` 错当成章节列表容器；真实章节统一位于其下的 `.mw-parser-output`，导致直接子节点迭代永远无法进入章节状态机。

## Fix

把解析根从 `soup.body` 收敛为 `soup.select_one(".mw-parser-output")`，并保留无该类时的兼容回退。没有放宽空结果或结构完整性门禁。

## Regression Evidence

已关闭：`scripts/validate_problem_library.py`、`scripts/test_problem_library.py` 与查询 smoke 在最终代码上全部通过。

---

# Debug：UnsolvedMath 源 ID/URL 一对多冲突

## Bug

109 页共解析出站点声明的 5,426 行，但旧门禁发现只有 5,375 个唯一 `source_native_id` / 详情 URL，因而拒绝生成问题库。

## Environment

- 原始证据：`problem-library/raw/unsolvedmath/page-001.html` 至 `page-109.html`
- 全量抓取：109/109 页，5,426 行

## Reproduction

```bash
python3 scripts/fetch_problem_library.py --delay 0.15
```

## Observations

- 重复不是单纯的相邻分页重叠；同一源 ID 在相隔多页的卡片上对应不同标题。
- 例如 `COMB-001` 对应 “The Hadwiger-Nelson Problem” 和两个版本的 “1/3–2/3 Conjecture”。
- 共 5,426 个目录行、5,375 个不同源 ID，源 ID 不能作为数据库主键。

## Hypotheses

- H1（ROOT，confirmed）：UnsolvedMath 导入数据复用了公开 ID/slug；源 ID 是展示字段，不是可靠唯一键。
- H2（rejected）：抓取过程中分页整体漂移；冲突集中在特定早期导入 ID，且多数不在相邻页。
- H3（rejected）：解析器选中了同一卡片的嵌套重复链接；每页已按 href 去重，页内稳定为 50 条（末页 26 条）。

## Experiments

1. RED：全量抓取完成后唯一 ID/URL 门禁失败。
2. 对 109 个缓存页离线重算并输出全部冲突的页码、标题和 URL。
3. 最小修复：本地 ID 改为“源 ID + 卡片内容 SHA-1 指纹”；完全相同重复行追加出现序号。
4. 将所有冲突组、不同源 ID 数和超额行数固化进 manifest，并由 validator 反算验证。

## Root Cause

抓取器错误地假设第三方站点展示的 `source_native_id` 和详情 URL 满足唯一键约束；来源实际包含一对多冲突，完整镜像必须把它们当作数据质量异常而不是删除条件。

## Fix

保留全部目录行，使用内容指纹作为本地主键，并增加可机械核验的 `identity_anomalies` 账本。查询结果仍展示原始 ID 和 URL，避免伪造来源身份。

## Regression Evidence

已关闭：缓存重建生成 6,012 条唯一本地记录；validator 证明 UnsolvedMath 5,426/5,426 条、109/109 页；原始证据回归重算出 35 组冲突源 ID 和 51 个超额行。

---

# Debug：治理质量门缺少固定章节

## Bug

首次运行新的统一 `make check` 时，数学、数据和成果晋升检查全部通过，但 governance strict validator 阻止交付：PROJECT_OPERATING_MODEL 缺“工具链模型”，TOOLCHAIN_MODEL 缺“成熟工具优先”和“工具链变更流程”；ADR 使用了 validator 不支持的 `accepted` 状态。

## Environment

- Python 3.12
- 本项目新初始化的 minimal governance package
- `governance/tools/validate_governance_package.py --strict`

## Reproduction

```bash
make check
```

## Observations

- 产品/数学检查均 PASS，失败只来自治理文档固定契约。
- validator 明确列出三个缺失章节和一个未知状态。
- validator 支持 `current`，不支持 `accepted`。

## Hypotheses

- H1（ROOT，confirmed）：项目化重写治理文档时删掉了模板要求的固定章节标题，内容存在但结构契约不完整。
- H2（confirmed）：ADR 状态使用了通用术语 `accepted`，与当前 owner validator 的枚举不一致。
- H3（rejected）：研究空间校验或 CI 实现失败；它们在同一命令中已先行 PASS。

## Experiments

1. RED：原样 `make check`，稳定报告三个缺失章节和未知状态。
2. 最小修复：补回三个 owner-required 章节，将 ADR 状态改为 `current`，不改研究逻辑。
3. GREEN：原样重跑 `make check` 与 `make check-full`。

## Root Cause

治理内容定制时只保留了语义，没有保留 owner validator 要求的固定文档结构与状态枚举。

## Fix

补齐固定章节，将 ADR 状态对齐为 `current`；统一质量门继续 fail-closed，不降低 validator 严格度。

## Regression Evidence

本节以修复后原样运行 `make check` 和 `make check-full` 的新鲜输出为准；任一非零退出则保持未关闭。
