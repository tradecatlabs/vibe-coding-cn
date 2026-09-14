# Vibe Mathing 公共具体问题索引

本页把本仓库与 `https://github.com/vibemathing` 的公开问题生态接起来，但**不复制远端研究仓库**。远端内容、仓库状态和题面可能变化；公共 ProblemContract catalog 的数量与列表是基于 `LIBRARY_SNAPSHOT.json` / `catalog/canonical-index.json` 在 **2026-09-07** 的观察，赏金仓库排名是基于 Project #2 View 3 在 **2026-09-09** 的独立快照。开始研究前必须重新读取远端入口。

## 公开入口

| 入口 | 作用 | 是否是本仓库的本地真相源 |
| --- | --- | --- |
| [问题仓库总览 · GitHub Project #1](https://github.com/users/vibemathing/projects/1) | 跨仓库运营索引，集中导航公开单问题仓库 | 否；Project、字段、view 和卡片不是数学 Evidence 或 Result |
| [赏金问题地图 · GitHub Project #2 View 3](https://github.com/users/vibemathing/projects/2/views/3) | 带日期的赏金与问题仓库运营索引 | 否；金额、Award、字段、view 和卡片不是数学 Evidence 或 Result |
| [`Project #2 Top 146 快照`](BOUNTY_PROJECT_2_TOP146.md) | 146 个去重后的问题仓库及其原币种/来源元数据 | 否；只读 pointer-only 快照，不自动导入 ProblemContract |
| [`vibe-mathing-problem-library-public`](https://github.com/vibemathing/vibe-mathing-problem-library-public) | 问题总库：公开的 ProblemContract 发现与准入目录 | 否；它是外部来源，不能自动写入本仓库 canonical ledger |
| [`vibe-mathing-problem-public-template`](https://github.com/vibemathing/vibe-mathing-problem-public-template) | 单问题网页版研究模板，含固定 Web research Harness | 否；模板和 transport 不能自动产生 Result |
| [`vibemathing` 公开仓库列表](https://github.com/vibemathing?tab=repositories) | 具体 `problem-*` 研究仓库的导航入口 | 否；仓库名只是 locator，不是数学结论 |

## 关键问题快捷入口

下列链接是公开单问题仓库 locator，不是本仓库 canonical ledger 的副本。六个千禧年条目仍按未闭合开放问题处理；secp256k1 条目是独立的密码学复杂性审计问题，不属于千禧年问题。任何仓库、Issue、PR、CI、checkpoint 或候选文件都不能据此晋升为 Evidence、Result 或 Solution。

| 类别 | 问题 | 公开单问题仓库 |
| --- | --- | --- |
| 千禧年问题 | 黎曼猜想 | [`problem-millennium-riemann-hypothesis`](https://github.com/vibemathing/problem-millennium-riemann-hypothesis) |
| 千禧年问题 | P 与 NP 问题 | [`problem-millennium-p-vs-np`](https://github.com/vibemathing/problem-millennium-p-vs-np) |
| 千禧年问题 | Navier–Stokes 方程存在性与光滑性 | [`problem-millennium-navier-stokes`](https://github.com/vibemathing/problem-millennium-navier-stokes) |
| 千禧年问题 | Yang–Mills 理论存在性与质量间隙 | [`problem-millennium-yang-mills-mass-gap`](https://github.com/vibemathing/problem-millennium-yang-mills-mass-gap) |
| 千禧年问题 | 霍奇猜想 | [`problem-millennium-hodge-conjecture`](https://github.com/vibemathing/problem-millennium-hodge-conjecture) |
| 千禧年问题 | Birch–Swinnerton-Dyer 猜想 | [`problem-millennium-birch-swinnerton-dyer`](https://github.com/vibemathing/problem-millennium-birch-swinnerton-dyer) |
| 独立关键问题 | secp256k1 离散对数经典多项式时间性审计 | [`problem-secp256k1-ecdlog-polytime`](https://github.com/vibemathing/problem-secp256k1-ecdlog-polytime) |

### Project #2 高赏金问题仓库快照

[`BOUNTY_PROJECT_2_TOP146.md`](BOUNTY_PROJECT_2_TOP146.md) 是 Project #2 View 3 的人类可读排名，[`registry/bounty-project-2-top146.v1.json`](registry/bounty-project-2-top146.v1.json) 是同一快照的机器入口。选择依据是 View 3 的 `USD Equivalent DESC`、`Title ASC`，再按 Repository URL 去重，取前 146 个唯一仓库；同一仓库的多个 Award record 全部保留，不把金额相加。

本次回读得到 234 条 Award record、226 个唯一 Repository URL。严格 `USD Equivalent > 100` 的唯一仓库为 141 个；为满足“前 146 个唯一仓库”的目标，排名末端保留 USD 100.00 的边界行。原币种、FX 日期、来源状态、Award 状态和支付未知状态均为带日期的来源元数据，不是可领取余额、数学证据或 Result。`secp256k1` 如出现在赏金索引中，仍是独立密码学问题，不属于千禧年问题。

公共问题总库的机器入口：

- [`LIBRARY_PROFILE.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/LIBRARY_PROFILE.json)：声明该仓库只做问题发现和 ProblemContract catalog，不存数学 Result；
- [`LIBRARY_SNAPSHOT.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/LIBRARY_SNAPSHOT.json)：带文件摘要的来源快照；
- [`catalog/canonical-index.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/catalog/canonical-index.json)：canonical ProblemContract 索引；
- [`CATALOG.md`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/CATALOG.md)：人类可读目录。

该来源快照报告 10 个 canonical ProblemContract、0 个 draft contract 和 10 个 repository locator。它是远端快照事实，不等于本仓库已有 10 个 canonical Problem；本仓库的 [`problem-library/records/canonical-problems.jsonl`](records/canonical-problems.jsonl) 仍保持空白。

## 快照中的 canonical 问题

以下表格是远端 `catalog/canonical-index.json` 的稳定 locator 摘要；题面、生命周期、digest 和具体仓库都要在使用时从远端重新核对。

| Problem ID | 远端合同 | 对应具体仓库 |
| --- | --- | --- |
| `problem:opg-37271-star-chromatic-index-cubic` | [`catalog/problems/opg-37271-star-chromatic-index-cubic.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/catalog/problems/opg-37271-star-chromatic-index-cubic.json) | [`problem-opg-37271-star-chromatic-index-cubic`](https://github.com/vibemathing/problem-opg-37271-star-chromatic-index-cubic) |
| `problem:opg-401-circular-coloring-subcubic-planar` | [`catalog/problems/opg-401-circular-coloring-subcubic-planar.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/catalog/problems/opg-401-circular-coloring-subcubic-planar.json) | [`problem-opg-401-circular-coloring-subcubic-planar`](https://github.com/vibemathing/problem-opg-401-circular-coloring-subcubic-planar) |
| `problem:opg-46613-cubic-p3-partition` | [`catalog/problems/opg-46613-cubic-p3-partition.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/catalog/problems/opg-46613-cubic-p3-partition.json) | [`problem-opg-46613-cubic-p3-partition`](https://github.com/vibemathing/problem-opg-46613-cubic-p3-partition) |
| `problem:opg-1808-monochromatic-reachability` | [`catalog/problems/opg-1808-monochromatic-reachability.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/catalog/problems/opg-1808-monochromatic-reachability.json) | [`problem-opg-1808-monochromatic-reachability`](https://github.com/vibemathing/problem-opg-1808-monochromatic-reachability) |
| `problem:opg-500-geodesic-cycles` | [`catalog/problems/opg-500-geodesic-cycles.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/catalog/problems/opg-500-geodesic-cycles.json) | [`problem-opg-500-geodesic-cycles`](https://github.com/vibemathing/problem-opg-500-geodesic-cycles) |
| `problem:opg-37357-obstacle-number` | [`catalog/problems/opg-37357-obstacle-number.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/catalog/problems/opg-37357-obstacle-number.json) | [`problem-opg-37357-obstacle-number`](https://github.com/vibemathing/problem-opg-37357-obstacle-number) |
| `problem:erdos-81-chordal-clique-partition` | [`catalog/problems/erdos-81-chordal-clique-partition.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/catalog/problems/erdos-81-chordal-clique-partition.json) | [`problem-erdos-81-chordal-clique-partition`](https://github.com/vibemathing/problem-erdos-81-chordal-clique-partition) |
| `problem:opg-169-two-color-conjecture` | [`catalog/problems/opg-169-two-color-conjecture.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/catalog/problems/opg-169-two-color-conjecture.json) | [`problem-opg-169-two-color-conjecture`](https://github.com/vibemathing/problem-opg-169-two-color-conjecture) |
| `problem:opg-434-weak-pentagon` | [`catalog/problems/opg-434-weak-pentagon.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/catalog/problems/opg-434-weak-pentagon.json) | [`problem-opg-434-weak-pentagon`](https://github.com/vibemathing/problem-opg-434-weak-pentagon) |
| `problem:opg-37364-matching-cut-girth` | [`catalog/problems/opg-37364-matching-cut-girth.json`](https://github.com/vibemathing/vibe-mathing-problem-library-public/blob/main/catalog/problems/opg-37364-matching-cut-girth.json) | [`problem-opg-37364-matching-cut-girth`](https://github.com/vibemathing/problem-opg-37364-matching-cut-girth) |

以 `problem-um-*` 开头的公开仓库在公开元数据中标为 candidate-only/web-research。它们是发现输入，不应因为仓库存在、Issue/PR 合并或来源标记为 `solved` 就被提升为本仓库的 Problem、Result 或 Solution。

## 开始方法

### A. 只查目录元数据（推荐第一步）

该命令只读 GitHub 公共 API 的仓库元数据，不 clone、不执行远端代码、不写入本地问题记录：

```bash
python3 scripts/query_vibemathing_public.py --kind library
python3 scripts/query_vibemathing_public.py --kind template
python3 scripts/query_vibemathing_public.py --kind concrete --limit 20
python3 scripts/query_vibemathing_public.py --catalog
```

离线阅读入口则直接打开上方的 catalog 链接。脚本失败时必须保留失败语义，不能把网络不可达解释成“没有问题”。

### B. 选择一个具体问题

1. 从 `catalog/canonical-index.json` 选定 `problem_id`；
2. 重新读取合同 JSON，核对 `lifecycle=active`、statement、domain、quantifiers、sources、acceptance 和 contract digest；
3. 核对对应 GitHub 仓库的 database identity、默认分支和可见性；
4. 不把这个远端合同自动写入本仓库 `canonical-problems.jsonl`，除非另行完成来源、许可和陈述忠实性审查。

### C. 启动网页版研究套件

具体问题仓库是由 [`vibe-mathing-problem-public-template`](https://github.com/vibemathing/vibe-mathing-problem-public-template) 生成的单问题研究仓库。进入已选仓库后，按远端模板规定的顺序阅读：

1. `AGENTS.md`；
2. `WEB_BOOTSTRAP.md`；
3. `WEB_CHANNEL_PROFILE.json`；
4. `HARNESS_SNAPSHOT.json`；
5. `WEB_CONTEXT_BUNDLE.md`；
6. `WEB_ACTIVE_SKILLS.json`；
7. `problem-library/records/canonical-problems.jsonl`；
8. `research/records/failed-routes.jsonl`；
9. Issue 指定的当前 route/obligation；
10. `WEB_OUTPUT_CONTRACT.json`。

网页版套件的候选写入范围是 `research/artifacts/web-inbox/**`、`research/artifacts/candidates/**` 和 `research/artifacts/source-notes/**`。Issue、branch、commit、PR、review、merge、CI 和 checkpoint 是候选传输/活动记录，不是 Evidence、Result 或 Solution 准入。

### D. 回到本仓库的验证边界

本仓库负责公共 Problem/Attempt/Result schema、候选隔离、验证规则和派生解库门禁。远端问题库和网页版 Harness 是外部输入/运输层；它们不能绕过本仓库的 ProblemContract、独立验证、evidence 能力和 statement-faithfulness 规则。当前本仓库 canonical Problem、Attempt、Result 和 Solution index 仍为空。

## 机器入口

机器可读登记见 [`registry/vibemathing-public-source.v1.json`](registry/vibemathing-public-source.v1.json)；其中的 `bounty_project_index` 指向 Project #2 及 Top 146 快照。它们是 pointer-only registry/snapshot，不是远端仓库镜像；修改上游地址、模板版本、快照数量或导入策略时，必须更新观察日期并重新运行公共边界检查。
