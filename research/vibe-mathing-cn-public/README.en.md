# vibe-mathing-cn: Trusted AI Mathematics Research and Verification Workbench

[![CI](https://github.com/vibemathing/vibe-mathing-cn-public/actions/workflows/ci.yml/badge.svg)](https://github.com/vibemathing/vibe-mathing-cn-public/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB)](requirements.txt)
[![Lean fixture](https://img.shields.io/badge/Lean-fixture-4B69FF)](fixtures/lean-proof/README.md)
[![License](https://img.shields.io/badge/license-MIT-0B7A75)](LICENSE)
[![Solution index](https://img.shields.io/badge/solutions-empty-orange)](result-library/indexes/solutions.json)
[![GEO](https://img.shields.io/badge/GEO-fact--bounded-7C3AED)](GEO.md)
[![Metamodel](https://img.shields.io/badge/metamodel-Point--Line--Face--Body-0B7A75)](governance/standards/POINT-LINE-FACE-BODY-METAMODEL-v0.1.md)

> **Untrusted candidate generation + trusted verification: construct candidates from a problem space, then derive a solution view only after verification.**

> **Current public status (verified 2026-09-09):** the canonical Problem, Attempt, and Result ledgers are empty; `result-library/indexes/solutions.json` has no result IDs; this repository does not claim to solve any open mathematics problem.

Canonical public repository: <https://github.com/vibemathing/vibe-mathing-cn-public>

### Public entrypoint index

| Entrypoint | Purpose |
| --- | --- |
| [Problem repository fleet · GitHub Project #1](https://github.com/users/vibemathing/projects/1) | Browse public single-problem repositories; Project fields and cards are operational indexes, not mathematical evidence |
| [Bounty problem map · GitHub Project #2 View 3](https://github.com/users/vibemathing/projects/2/views/3) | Browse the dated bounty ranking; amounts and Project states are source metadata, not mathematical evidence or payable balance |
| [Top-146 bounty repository snapshot](problem-library/BOUNTY_PROJECT_2_TOP146.md) | Read the deduplicated public repository list and its machine-readable snapshot |
| [Public ProblemContract library](https://github.com/vibemathing/vibe-mathing-problem-library-public) | Discover public problem contracts, the catalog, and repository locators |
| [Single-problem research template](https://github.com/vibemathing/vibe-mathing-problem-public-template) | Inspect the fixed Web research Harness, candidate-write boundary, and bootstrap files |
| [All public `vibemathing` repositories](https://github.com/vibemathing?tab=repositories) | Find concrete `problem-*` repositories and other public engineering repositories |
| [Detailed public problem index in this repository](problem-library/VIBEMATHING_PUBLIC_INDEX.md) | Read the catalog, template, query commands, and admission boundary |

### Key problem repositories and bounty map

> These are ProblemContract/candidate-research entrypoints only. A repository, Issue, PR, CI run, or checkpoint does not mean that a problem has been solved and does not automatically create Evidence, a Result, or a Solution. The secp256k1 entry is not a Millennium Prize Problem.

The dated [`Project #2 View 3 snapshot`](problem-library/BOUNTY_PROJECT_2_TOP146.md) contains the first 146 unique repository URLs in the USD-equivalent bounty view, with original currency, source status, Award status, and provenance preserved. The [`machine-readable snapshot`](problem-library/registry/bounty-project-2-top146.v1.json) is pointer-only metadata: it does not import ProblemContracts or add amounts together. Because the requested unit is 146 repositories, the snapshot retains the USD 100.00 boundary rows; it is not a claim that every row is strictly greater than USD 100.

The six Millennium entries remain a separate category. The cryptographic `secp256k1` entry is an independent complexity-audit problem and is not part of the Millennium Problems.

The table first pins `secp256k1` as an independent research focus, then lists the first 146 unique problem repositories in Project #2 View 3 order. `secp256k1` is not listed in Project #2's bounty ranking, so no bounty amount is inferred for it. The added bounty column preserves the original currency and includes the USD-equivalent value from this snapshot. Amounts use compact `M=millions` and `k=thousands` notation; exact values remain in the machine snapshot. Related Award records are preserved but not added; Project, repository, Issue, PR, CI, and checkpoint activity is not mathematical Evidence, Result, or Solution.

| Rank | Category | Problem / Problem Key | Bounty (original; USD reference) | Public single-problem repository |
| ---: | --- | --- | ---: | --- |
| Featured | Independent cryptographic focus | `secp256k1`: classical polynomial-time audit of discrete-log inversion | Bounty not listed in Project #2 | [vibemathing/problem-secp256k1-ecdlog-polytime](https://github.com/vibemathing/problem-secp256k1-ecdlog-polytime) |
| 1 | Project #2 bounty problem | `eternity-ii`：Eternity II puzzle | USD 2M | [vibemathing/problem-eternity-ii](https://github.com/vibemathing/problem-eternity-ii) |
| 2 | Project #2 bounty problem | `beal-million`：Beal猜想 | USD 1M | [vibemathing/problem-um-nt-078-beal-s-conjecture-c75e225d](https://github.com/vibemathing/problem-um-nt-078-beal-s-conjecture-c75e225d) |
| 3 | Millennium problem | `clay-bsd`：Birch–Swinnerton-Dyer猜想 | USD 1M | [vibemathing/problem-millennium-birch-swinnerton-dyer](https://github.com/vibemathing/problem-millennium-birch-swinnerton-dyer) |
| 4 | Millennium problem | `clay-hodge`：霍奇猜想 | USD 1M | [vibemathing/problem-millennium-hodge-conjecture](https://github.com/vibemathing/problem-millennium-hodge-conjecture) |
| 5 | Millennium problem | `clay-navier-stokes`：Navier–Stokes存在性与光滑性 | USD 1M | [vibemathing/problem-millennium-navier-stokes](https://github.com/vibemathing/problem-millennium-navier-stokes) |
| 6 | Millennium problem | `clay-p-vs-np`：P vs NP | USD 1M | [vibemathing/problem-millennium-p-vs-np](https://github.com/vibemathing/problem-millennium-p-vs-np) |
| 7 | Historical Millennium problem | `clay-poincare`：庞加莱猜想（历史已解决） | USD 1M | [vibemathing/problem-clay-poincare](https://github.com/vibemathing/problem-clay-poincare) |
| 8 | Millennium problem | `clay-riemann`：黎曼猜想 | USD 1M | [vibemathing/problem-millennium-riemann-hypothesis](https://github.com/vibemathing/problem-millennium-riemann-hypothesis) |
| 9 | Millennium problem | `clay-yang-mills`：Yang–Mills存在性与质量间隙 | USD 1M | [vibemathing/problem-millennium-yang-mills-mass-gap](https://github.com/vibemathing/problem-millennium-yang-mills-mass-gap) |
| 10 | Project #2 bounty problem | `collatz-original`：Collatz猜想：Bakuage日元奖 | JPY 120M ≈ USD 775.44k; also EUR 1k ≈ USD 1.16k; not added | [vibemathing/problem-um-nt-002-collatz-conjecture-4d39f1ab](https://github.com/vibemathing/problem-um-nt-002-collatz-conjecture-4d39f1ab) |
| 11 | Project #2 bounty problem | `eff-prime-1000000000`：首次发现至少1,000,000,000位十进制素数 | USD 250k | [vibemathing/problem-eff-prime-1000000000](https://github.com/vibemathing/problem-eff-prime-1000000000) |
| 12 | Project #2 bounty problem | `eff-prime-100000000`：首次发现至少100,000,000位十进制素数 | USD 150k | [vibemathing/problem-eff-prime-100000000](https://github.com/vibemathing/problem-eff-prime-100000000) |
| 13 | Project #2 bounty problem | `eff-prime-10000000-awarded`：First ten-million-digit prime | USD 100k | [vibemathing/problem-eff-prime-10000000-awarded](https://github.com/vibemathing/problem-eff-prime-10000000-awarded) |
| 14 | Project #2 bounty problem | `eff-prime-1000000-awarded`：First one-million-digit prime | USD 50k | [vibemathing/problem-eff-prime-1000000-awarded](https://github.com/vibemathing/problem-eff-prime-1000000-awarded) |
| 15 | Project #2 bounty problem | `gimps-eff-100m-share`：EFF 100-million-digit prime discoverer share | USD 50k | [vibemathing/problem-gimps-eff-100m-share](https://github.com/vibemathing/problem-gimps-eff-100m-share) |
| 16 | Project #2 bounty problem | `erdosproblems:142`：Erdős Problem #142 | USD 10k | [vibemathing/problem-um-ep-142-erd-s-problem-142-c2a5cdac](https://github.com/vibemathing/problem-um-ep-142-erd-s-problem-142-c2a5cdac) |
| 17 | Project #2 bounty problem | `erdosproblems:4`：Erdős Problem #4 | USD 10k | [vibemathing/problem-erdosproblems-4](https://github.com/vibemathing/problem-erdosproblems-4) |
| 18 | Project #2 bounty problem | `rule30-1`：Rule30中央列非最终周期性 | USD 10k | [vibemathing/problem-rule30-1](https://github.com/vibemathing/problem-rule30-1) |
| 19 | Project #2 bounty problem | `rule30-2`：Rule30中央列0/1极限频率 | USD 10k | [vibemathing/problem-rule30-2](https://github.com/vibemathing/problem-rule30-2) |
| 20 | Project #2 bounty problem | `rule30-3`：Rule30计算不可约性 | USD 10k | [vibemathing/problem-rule30-3](https://github.com/vibemathing/problem-rule30-3) |
| 21 | Project #2 bounty problem | `erdosproblems:3`：Erdős Problem #3 | USD 5k | [vibemathing/problem-um-ep-3-erd-s-problem-3-f41c4104](https://github.com/vibemathing/problem-um-ep-3-erd-s-problem-3-f41c4104) |
| 22 | Project #2 bounty problem | `sun-prime-fibonacci-proof`：Prime plus Fibonacci/Lucas sums conjecture: positive solution | USD 5k | [vibemathing/problem-sun-prime-fibonacci-proof](https://github.com/vibemathing/problem-sun-prime-fibonacci-proof) |
| 23 | Project #2 bounty problem | `talagrand-bernoulli-awarded`：Bernoulli conjecture | USD 5k | [vibemathing/problem-talagrand-bernoulli-awarded](https://github.com/vibemathing/problem-talagrand-bernoulli-awarded) |
| 24 | Project #2 bounty problem | `krenn-leitner-graph`：Krenn–Gu图论问题 | EUR 3k ≈ USD 3.49k | [vibemathing/problem-krenn-leitner-graph](https://github.com/vibemathing/problem-krenn-leitner-graph) |
| 25 | Project #2 bounty problem | `gimps-new-mersenne`：Each qualifying new Mersenne prime | USD 3k | [vibemathing/problem-gimps-new-mersenne](https://github.com/vibemathing/problem-gimps-new-mersenne) |
| 26 | Project #2 bounty problem | `sun-2468-proof`：2-4-6-8 conjecture first proof | USD 2.47k | [vibemathing/problem-sun-2468-proof](https://github.com/vibemathing/problem-sun-2468-proof) |
| 27 | Project #2 bounty problem | `sun-24`：24-conjecture: restricted four-square representation | USD 2.4k | [vibemathing/problem-sun-24](https://github.com/vibemathing/problem-sun-24) |
| 28 | Project #2 bounty problem | `kcik-1`：KCIK Problem 1: Infinite sequence of dimensions with SIC POVM family | EUR 2.03k ≈ USD 2.35k | [vibemathing/problem-kcik-1](https://github.com/vibemathing/problem-kcik-1) |
| 29 | Project #2 bounty problem | `kcik-2`：KCIK Problem 2: At least 4 MUBs in dimension 6 or no 7 MUBs | EUR 2.03k ≈ USD 2.35k | [vibemathing/problem-kcik-2](https://github.com/vibemathing/problem-kcik-2) |
| 30 | Project #2 bounty problem | `kcik-3`：KCIK Problem 3: AME state for four six-level systems / quantum Euler officers | EUR 2.03k ≈ USD 2.35k | [vibemathing/problem-kcik-3](https://github.com/vibemathing/problem-kcik-3) |
| 31 | Project #2 bounty problem | `kcik-4`：KCIK Problem 4: Existence of NPT bound entangled states | EUR 2.03k ≈ USD 2.35k | [vibemathing/problem-kcik-4](https://github.com/vibemathing/problem-kcik-4) |
| 32 | Project #2 bounty problem | `kcik-5`：KCIK Problem 5: Whether a specified two-ququart state is 2-copy distillable | EUR 2.03k ≈ USD 2.35k | [vibemathing/problem-kcik-5](https://github.com/vibemathing/problem-kcik-5) |
| 33 | Project #2 bounty problem | `sun-135`：1-3-5 conjecture | USD 1.35k | [vibemathing/problem-sun-135](https://github.com/vibemathing/problem-sun-135) |
| 34 | Project #2 bounty problem | `boyer-enigma-1-main`：3x3 magic square with at least 7 distinct squared integers | EUR 1k ≈ USD 1.16k | [vibemathing/problem-boyer-enigma-1-main](https://github.com/vibemathing/problem-boyer-enigma-1-main) |
| 35 | Project #2 bounty problem | `boyer-enigma-2-main`：5x5 bimagic square with distinct positive integers | EUR 1k ≈ USD 1.16k | [vibemathing/problem-boyer-enigma-2-main](https://github.com/vibemathing/problem-boyer-enigma-2-main) |
| 36 | Project #2 bounty problem | `boyer-enigma-3-main`：3x3 semi-magic square of distinct positive cubes | EUR 1k ≈ USD 1.16k | [vibemathing/problem-boyer-enigma-3-main](https://github.com/vibemathing/problem-boyer-enigma-3-main) |
| 37 | Project #2 bounty problem | `boyer-enigma-4-main`：4x4 magic square of distinct positive cubes | EUR 1k ≈ USD 1.16k | [vibemathing/problem-boyer-enigma-4-main](https://github.com/vibemathing/problem-boyer-enigma-4-main) |
| 38 | Project #2 bounty problem | `boyer-enigma-5-awarded`：4x4 multiplicative magic cube with distinct positive integers <364 | EUR 1k ≈ USD 1.16k | [vibemathing/problem-boyer-enigma-5-awarded](https://github.com/vibemathing/problem-boyer-enigma-5-awarded) |
| 39 | Project #2 bounty problem | `boyer-enigma-6-main`：5x5 additive-multiplicative magic square | EUR 1k ≈ USD 1.16k | [vibemathing/problem-boyer-enigma-6-main](https://github.com/vibemathing/problem-boyer-enigma-6-main) |
| 40 | Project #2 bounty problem | `krenn-quantum-graph-best-paper`：Quantum-Graph Best-Paper Award | EUR 1k ≈ USD 1.16k | [vibemathing/problem-krenn-quantum-graph-best-paper](https://github.com/vibemathing/problem-krenn-quantum-graph-best-paper) |
| 41 | Project #2 bounty problem | `erdosproblems:1191`：Erdős Problem #1191 | USD 1k | [vibemathing/problem-erdosproblems-1191](https://github.com/vibemathing/problem-erdosproblems-1191) |
| 42 | Project #2 bounty problem | `erdosproblems:139`：Erdős Problem #139 | USD 1k | [vibemathing/problem-erdosproblems-139](https://github.com/vibemathing/problem-erdosproblems-139) |
| 43 | Project #2 bounty problem | `erdosproblems:20`：Erdős Problem #20 | USD 1k | [vibemathing/problem-um-ep-20-erd-s-problem-20-9f5c5ebf](https://github.com/vibemathing/problem-um-ep-20-erd-s-problem-20-9f5c5ebf) |
| 44 | Project #2 bounty problem | `erdosproblems:2`：Erdős Problem #2 | USD 1k | [vibemathing/problem-erdosproblems-2](https://github.com/vibemathing/problem-erdosproblems-2) |
| 45 | Project #2 bounty problem | `erdosproblems:30`：Erdős Problem #30 | USD 1k | [vibemathing/problem-um-ep-30-erd-s-problem-30-5e3bbb7e](https://github.com/vibemathing/problem-um-ep-30-erd-s-problem-30-5e3bbb7e) |
| 46 | Project #2 bounty problem | `erdosproblems:592`：Erdős Problem #592 | USD 1k | [vibemathing/problem-um-ep-592-erd-s-problem-592-d5601e42](https://github.com/vibemathing/problem-um-ep-592-erd-s-problem-592-d5601e42) |
| 47 | Project #2 bounty problem | `erdosproblems:625`：Erdős Problem #625 | USD 1k | [vibemathing/problem-erdosproblems-625](https://github.com/vibemathing/problem-erdosproblems-625) |
| 48 | Project #2 bounty problem | `erdosproblems:64`：Erdős Problem #64 | USD 1k | [vibemathing/problem-erdosproblems-64](https://github.com/vibemathing/problem-erdosproblems-64) |
| 49 | Project #2 bounty problem | `erdosproblems:687`：Erdős Problem #687 | USD 1k | [vibemathing/problem-um-ep-687-erd-s-problem-687-fae65f77](https://github.com/vibemathing/problem-um-ep-687-erd-s-problem-687-fae65f77) |
| 50 | Project #2 bounty problem | `erdosproblems:707`：Erdős Problem #707 | USD 1k | [vibemathing/problem-erdosproblems-707](https://github.com/vibemathing/problem-erdosproblems-707) |
| 51 | Project #2 bounty problem | `hou-zeng-fibonacci-catalan-proof`：Prime plus Fibonacci plus Catalan sums conjecture: positive solution | USD 1k | [vibemathing/problem-hou-zeng-fibonacci-catalan-proof](https://github.com/vibemathing/problem-hou-zeng-fibonacci-catalan-proof) |
| 52 | Project #2 bounty problem | `sun-prime-triangular-proof`：Prime plus triangular-number conjecture: positive solution | USD 1k | [vibemathing/problem-sun-prime-triangular-proof](https://github.com/vibemathing/problem-sun-prime-triangular-proof) |
| 53 | Project #2 bounty problem | `sun-secondary-d-problem-1000`：Some New Diophantine Problems prize lead | USD 1k | [vibemathing/problem-sun-secondary-d-problem-1000](https://github.com/vibemathing/problem-sun-secondary-d-problem-1000) |
| 54 | Project #2 bounty problem | `sun-secondary-representation-1000`：Sun representation riddle prize lead B | USD 1k | [vibemathing/problem-sun-secondary-representation-1000](https://github.com/vibemathing/problem-sun-secondary-representation-1000) |
| 55 | Project #2 bounty problem | `talagrand-convolution`：Regularization from L1 by convolution | USD 1k | [vibemathing/problem-talagrand-convolution](https://github.com/vibemathing/problem-talagrand-convolution) |
| 56 | Project #2 bounty problem | `talagrand-matchings`：Matching problem | USD 1k | [vibemathing/problem-talagrand-matchings](https://github.com/vibemathing/problem-talagrand-matchings) |
| 57 | Project #2 bounty problem | `talagrand-small`：Are many small sets explicitly small? | USD 1k | [vibemathing/problem-talagrand-small](https://github.com/vibemathing/problem-talagrand-small) |
| 58 | Project #2 bounty problem | `topp-p30`：Thrackles problem | USD 1k | [vibemathing/problem-topp-p30](https://github.com/vibemathing/problem-topp-p30) |
| 59 | Project #2 bounty problem | `topp-p57`：Plane coloring number problem | USD 1k | [vibemathing/problem-topp-p57](https://github.com/vibemathing/problem-topp-p57) |
| 60 | Project #2 bounty problem | `althofer-3`：Collatz双人±1游戏 | EUR 500 ≈ USD 581.1 | [vibemathing/problem-althofer-3](https://github.com/vibemathing/problem-althofer-3) |
| 61 | Project #2 bounty problem | `boyer-enigma-1-partial`：Impossibility of 8 or 9 distinct squares in a 3x3 magic square | EUR 500 ≈ USD 581.1 | [vibemathing/problem-boyer-enigma-1-partial](https://github.com/vibemathing/problem-boyer-enigma-1-partial) |
| 62 | Project #2 bounty problem | `boyer-enigma-4a`：5x5 magic square of cubes | EUR 500 ≈ USD 581.1 | [vibemathing/problem-boyer-enigma-4a](https://github.com/vibemathing/problem-boyer-enigma-4a) |
| 63 | Project #2 bounty problem | `boyer-enigma-4b`：6x6 magic square of cubes | EUR 500 ≈ USD 581.1 | [vibemathing/problem-boyer-enigma-4b](https://github.com/vibemathing/problem-boyer-enigma-4b) |
| 64 | Project #2 bounty problem | `boyer-enigma-6a`：6x6 additive-multiplicative magic square | EUR 500 ≈ USD 581.1 | [vibemathing/problem-boyer-enigma-6a](https://github.com/vibemathing/problem-boyer-enigma-6a) |
| 65 | Project #2 bounty problem | `erdosproblems:107`：Erdős Problem #107 | USD 500 | [vibemathing/problem-erdosproblems-107](https://github.com/vibemathing/problem-erdosproblems-107) |
| 66 | Project #2 bounty problem | `erdosproblems:1135`：Erdős Problem #1135 | USD 500 | [vibemathing/problem-erdosproblems-1135](https://github.com/vibemathing/problem-erdosproblems-1135) |
| 67 | Project #2 bounty problem | `erdosproblems:113`：Erdős Problem #113 | USD 500 | [vibemathing/problem-erdosproblems-113](https://github.com/vibemathing/problem-erdosproblems-113) |
| 68 | Project #2 bounty problem | `erdosproblems:138`：Erdős Problem #138 | USD 500 | [vibemathing/problem-um-ep-138-erd-s-problem-138-58e3679f](https://github.com/vibemathing/problem-um-ep-138-erd-s-problem-138-58e3679f) |
| 69 | Project #2 bounty problem | `erdosproblems:140`：Erdős Problem #140 | USD 500 | [vibemathing/problem-erdosproblems-140](https://github.com/vibemathing/problem-erdosproblems-140) |
| 70 | Project #2 bounty problem | `erdosproblems:143`：Erdős Problem #143 | USD 500 | [vibemathing/problem-um-ep-143-erd-s-problem-143-17ecf620](https://github.com/vibemathing/problem-um-ep-143-erd-s-problem-143-17ecf620) |
| 71 | Project #2 bounty problem | `erdosproblems:146`：Erdős Problem #146 | USD 500 | [vibemathing/problem-erdosproblems-146](https://github.com/vibemathing/problem-erdosproblems-146) |
| 72 | Project #2 bounty problem | `erdosproblems:147`：Erdős Problem #147 | USD 500 | [vibemathing/problem-erdosproblems-147](https://github.com/vibemathing/problem-erdosproblems-147) |
| 73 | Project #2 bounty problem | `erdosproblems:161`：Erdős Problem #161 | USD 500 | [vibemathing/problem-um-ep-161-erd-s-problem-161-20d0e99f](https://github.com/vibemathing/problem-um-ep-161-erd-s-problem-161-20d0e99f) |
| 74 | Project #2 bounty problem | `erdosproblems:19`：Erdős Problem #19 | USD 500 | [vibemathing/problem-erdosproblems-19](https://github.com/vibemathing/problem-erdosproblems-19) |
| 75 | Project #2 bounty problem | `erdosproblems:1`：Erdős Problem #1 | USD 500 | [vibemathing/problem-erdosproblems-1](https://github.com/vibemathing/problem-erdosproblems-1) |
| 76 | Project #2 bounty problem | `erdosproblems:21`：Erdős Problem #21 | USD 500 | [vibemathing/problem-erdosproblems-21](https://github.com/vibemathing/problem-erdosproblems-21) |
| 77 | Project #2 bounty problem | `erdosproblems:220`：Erdős Problem #220 | USD 500 | [vibemathing/problem-erdosproblems-220](https://github.com/vibemathing/problem-erdosproblems-220) |
| 78 | Project #2 bounty problem | `erdosproblems:28`：Erdős Problem #28 | USD 500 | [vibemathing/problem-um-ep-28-erd-s-problem-28-dc057856](https://github.com/vibemathing/problem-um-ep-28-erd-s-problem-28-dc057856) |
| 79 | Project #2 bounty problem | `erdosproblems:39`：Erdős Problem #39 | USD 500 | [vibemathing/problem-um-ep-39-erd-s-problem-39-80ff208f](https://github.com/vibemathing/problem-um-ep-39-erd-s-problem-39-80ff208f) |
| 80 | Project #2 bounty problem | `erdosproblems:40`：Erdős Problem #40 | USD 500 | [vibemathing/problem-um-ep-40-erd-s-problem-40-2165a6ea](https://github.com/vibemathing/problem-um-ep-40-erd-s-problem-40-2165a6ea) |
| 81 | Project #2 bounty problem | `erdosproblems:41`：Erdős Problem #41 | USD 500 | [vibemathing/problem-um-ep-41-erd-s-problem-41-94e7f426](https://github.com/vibemathing/problem-um-ep-41-erd-s-problem-41-94e7f426) |
| 82 | Project #2 bounty problem | `erdosproblems:500`：Erdős Problem #500 | USD 500 | [vibemathing/problem-um-ep-500-erd-s-problem-500-51162c03](https://github.com/vibemathing/problem-um-ep-500-erd-s-problem-500-51162c03) |
| 83 | Project #2 bounty problem | `erdosproblems:564`：Erdős Problem #564 | USD 500 | [vibemathing/problem-um-ep-564-erd-s-problem-564-81ecbc0a](https://github.com/vibemathing/problem-um-ep-564-erd-s-problem-564-81ecbc0a) |
| 84 | Project #2 bounty problem | `erdosproblems:593`：Erdős Problem #593 | USD 500 | [vibemathing/problem-um-ep-593-erd-s-problem-593-81c4ffa7](https://github.com/vibemathing/problem-um-ep-593-erd-s-problem-593-81c4ffa7) |
| 85 | Project #2 bounty problem | `erdosproblems:601`：Erdős Problem #601 | USD 500 | [vibemathing/problem-um-ep-601-erd-s-problem-601-cfedd609](https://github.com/vibemathing/problem-um-ep-601-erd-s-problem-601-cfedd609) |
| 86 | Project #2 bounty problem | `erdosproblems:604`：Erdős Problem #604 | USD 500 | [vibemathing/problem-um-ep-604-erd-s-problem-604-704bf90a](https://github.com/vibemathing/problem-um-ep-604-erd-s-problem-604-704bf90a) |
| 87 | Project #2 bounty problem | `erdosproblems:66`：Erdős Problem #66 | USD 500 | [vibemathing/problem-um-ep-66-erd-s-problem-66-f5174838](https://github.com/vibemathing/problem-um-ep-66-erd-s-problem-66-f5174838) |
| 88 | Project #2 bounty problem | `erdosproblems:67`：Erdős Problem #67 | USD 500 | [vibemathing/problem-erdosproblems-67](https://github.com/vibemathing/problem-erdosproblems-67) |
| 89 | Project #2 bounty problem | `erdosproblems:712`：Erdős Problem #712 | USD 500 | [vibemathing/problem-um-ep-712-erd-s-problem-712-3bd4ae9c](https://github.com/vibemathing/problem-um-ep-712-erd-s-problem-712-3bd4ae9c) |
| 90 | Project #2 bounty problem | `erdosproblems:713`：Erdős Problem #713 | USD 500 | [vibemathing/problem-um-ep-713-erd-s-problem-713-59a90fa0](https://github.com/vibemathing/problem-um-ep-713-erd-s-problem-713-59a90fa0) |
| 91 | Project #2 bounty problem | `erdosproblems:74`：Erdős Problem #74 | USD 500 | [vibemathing/problem-erdosproblems-74](https://github.com/vibemathing/problem-erdosproblems-74) |
| 92 | Project #2 bounty problem | `erdosproblems:83`：Erdős Problem #83 | USD 500 | [vibemathing/problem-erdosproblems-83](https://github.com/vibemathing/problem-erdosproblems-83) |
| 93 | Project #2 bounty problem | `erdosproblems:89`：Erdős Problem #89 | USD 500 | [vibemathing/problem-um-ep-89-erd-s-problem-89-34644bf2](https://github.com/vibemathing/problem-um-ep-89-erd-s-problem-89-34644bf2) |
| 94 | Project #2 bounty problem | `erdosproblems:90`：Erdős Problem #90 | USD 500 | [vibemathing/problem-erdosproblems-90](https://github.com/vibemathing/problem-erdosproblems-90) |
| 95 | Project #2 bounty problem | `erdosproblems:92`：Erdős Problem #92 | USD 500 | [vibemathing/problem-erdosproblems-92](https://github.com/vibemathing/problem-erdosproblems-92) |
| 96 | Project #2 bounty problem | `erdosproblems:95`：Erdős Problem #95 | USD 500 | [vibemathing/problem-erdosproblems-95](https://github.com/vibemathing/problem-erdosproblems-95) |
| 97 | Project #2 bounty problem | `sun-secondary-unit-fraction-500`：Unit-fraction conjecture prize lead | USD 500 | [vibemathing/problem-sun-secondary-unit-fraction-500](https://github.com/vibemathing/problem-sun-secondary-unit-fraction-500) |
| 98 | Project #2 bounty problem | `topp-p39-distinct-distance`：Distinct-distance problem | USD 500 | [vibemathing/problem-topp-p39-distinct-distance](https://github.com/vibemathing/problem-topp-p39-distinct-distance) |
| 99 | Project #2 bounty problem | `topp-p39-unit-distance`：Unit-distance problem | USD 500 | [vibemathing/problem-topp-p39-unit-distance](https://github.com/vibemathing/problem-topp-p39-unit-distance) |
| 100 | Project #2 bounty problem | `sun-secondary-191o-480`：Bernoulli-polynomial identity prize lead | USD 480 | [vibemathing/problem-sun-secondary-191o-480](https://github.com/vibemathing/problem-sun-secondary-191o-480) |
| 101 | Project #2 bounty problem | `sun-2468-counterexample`：2-4-6-8 conjecture first explicit counterexample | CNY 2.47k ≈ USD 367.75 | [vibemathing/problem-sun-2468-counterexample](https://github.com/vibemathing/problem-sun-2468-counterexample) |
| 102 | Project #2 bounty problem | `de-caen-turan`：de Caen Turan-system conjecture | CAD 500 ≈ USD 361.79 | [vibemathing/problem-de-caen-turan](https://github.com/vibemathing/problem-de-caen-turan) |
| 103 | Project #2 bounty problem | `althofer-0`：Collatz随机±1变体 | EUR 300 ≈ USD 348.66 | [vibemathing/problem-althofer-0](https://github.com/vibemathing/problem-althofer-0) |
| 104 | Project #2 bounty problem | `kimberling-2`：Kimberling #2: Kimberling sequence contains every positive integer | USD 300 | [vibemathing/problem-kimberling-2](https://github.com/vibemathing/problem-kimberling-2) |
| 105 | Project #2 bounty problem | `shallit-18`：Shallit BC4 Open Problem 18: Shortest word outside Fact(S*) upper bound | GBP 200 ≈ USD 270.61 | [vibemathing/problem-shallit-18](https://github.com/vibemathing/problem-shallit-18) |
| 106 | Project #2 bounty problem | `shallit-19`：Shallit BC4 Open Problem 19: Pierce expansion bound improvement | GBP 200 ≈ USD 270.61 | [vibemathing/problem-shallit-19](https://github.com/vibemathing/problem-shallit-19) |
| 107 | Project #2 bounty problem | `shallit-7`：Shallit BC4 Open Problem 7: Are binary primitive words context-free? | GBP 200 ≈ USD 270.61 | [vibemathing/problem-shallit-7](https://github.com/vibemathing/problem-shallit-7) |
| 108 | Project #2 bounty problem | `okhotin-boolean-ambiguity`：Boolean grammars inherent ambiguity | CAD 360 ≈ USD 260.49 | [vibemathing/problem-okhotin-boolean-ambiguity](https://github.com/vibemathing/problem-okhotin-boolean-ambiguity) |
| 109 | Project #2 bounty problem | `erdosproblems:114`：Erdős Problem #114 | USD 250 | [vibemathing/problem-um-ep-114-erd-s-problem-114-b32b9bfc](https://github.com/vibemathing/problem-um-ep-114-erd-s-problem-114-b32b9bfc) |
| 110 | Project #2 bounty problem | `erdosproblems:123`：Erdős Problem #123 | USD 250 | [vibemathing/problem-erdosproblems-123](https://github.com/vibemathing/problem-erdosproblems-123) |
| 111 | Project #2 bounty problem | `erdosproblems:126`：Erdős Problem #126 | USD 250 | [vibemathing/problem-erdosproblems-126](https://github.com/vibemathing/problem-erdosproblems-126) |
| 112 | Project #2 bounty problem | `erdosproblems:128`：Erdős Problem #128 | USD 250 | [vibemathing/problem-erdosproblems-128](https://github.com/vibemathing/problem-erdosproblems-128) |
| 113 | Project #2 bounty problem | `erdosproblems:135`：Erdős Problem #135 | USD 250 | [vibemathing/problem-erdosproblems-135](https://github.com/vibemathing/problem-erdosproblems-135) |
| 114 | Project #2 bounty problem | `erdosproblems:144`：Erdős Problem #144 | USD 250 | [vibemathing/problem-erdosproblems-144](https://github.com/vibemathing/problem-erdosproblems-144) |
| 115 | Project #2 bounty problem | `erdosproblems:165`：Erdős Problem #165 | USD 250 | [vibemathing/problem-um-ep-165-erd-s-problem-165-cd71c3ca](https://github.com/vibemathing/problem-um-ep-165-erd-s-problem-165-cd71c3ca) |
| 116 | Project #2 bounty problem | `erdosproblems:166`：Erdős Problem #166 | USD 250 | [vibemathing/problem-erdosproblems-166](https://github.com/vibemathing/problem-erdosproblems-166) |
| 117 | Project #2 bounty problem | `erdosproblems:183`：Erdős Problem #183 | USD 250 | [vibemathing/problem-erdosproblems-183](https://github.com/vibemathing/problem-erdosproblems-183) |
| 118 | Project #2 bounty problem | `erdosproblems:18`：Erdős Problem #18 | USD 250 | [vibemathing/problem-erdosproblems-18](https://github.com/vibemathing/problem-erdosproblems-18) |
| 119 | Project #2 bounty problem | `erdosproblems:50`：Erdős Problem #50 | USD 250 | [vibemathing/problem-um-ep-50-erd-s-problem-50-8c337fab](https://github.com/vibemathing/problem-um-ep-50-erd-s-problem-50-8c337fab) |
| 120 | Project #2 bounty problem | `erdosproblems:52`：Erdős Problem #52 | USD 250 | [vibemathing/problem-um-ep-52-erd-s-problem-52-7a5bbe61](https://github.com/vibemathing/problem-um-ep-52-erd-s-problem-52-7a5bbe61) |
| 121 | Project #2 bounty problem | `erdosproblems:55`：Erdős Problem #55 | USD 250 | [vibemathing/problem-erdosproblems-55](https://github.com/vibemathing/problem-erdosproblems-55) |
| 122 | Project #2 bounty problem | `erdosproblems:590`：Erdős Problem #590 | USD 250 | [vibemathing/problem-erdosproblems-590](https://github.com/vibemathing/problem-erdosproblems-590) |
| 123 | Project #2 bounty problem | `erdosproblems:591`：Erdős Problem #591 | USD 250 | [vibemathing/problem-erdosproblems-591](https://github.com/vibemathing/problem-erdosproblems-591) |
| 124 | Project #2 bounty problem | `erdosproblems:595`：Erdős Problem #595 | USD 250 | [vibemathing/problem-um-ep-595-erd-s-problem-595-75882921](https://github.com/vibemathing/problem-um-ep-595-erd-s-problem-595-75882921) |
| 125 | Project #2 bounty problem | `erdosproblems:607`：Erdős Problem #607 | USD 250 | [vibemathing/problem-erdosproblems-607](https://github.com/vibemathing/problem-erdosproblems-607) |
| 126 | Project #2 bounty problem | `erdosproblems:671`：Erdős Problem #671 | USD 250 | [vibemathing/problem-um-ep-671-erd-s-problem-671-37a0c2dc](https://github.com/vibemathing/problem-um-ep-671-erd-s-problem-671-37a0c2dc) |
| 127 | Project #2 bounty problem | `erdosproblems:703`：Erdős Problem #703 | USD 250 | [vibemathing/problem-erdosproblems-703](https://github.com/vibemathing/problem-erdosproblems-703) |
| 128 | Project #2 bounty problem | `erdosproblems:77`：Erdős Problem #77 | USD 250 | [vibemathing/problem-um-ep-77-erd-s-problem-77-b05a9e88](https://github.com/vibemathing/problem-um-ep-77-erd-s-problem-77-b05a9e88) |
| 129 | Project #2 bounty problem | `sun-prime-fibonacci-counterexample`：Prime plus Fibonacci/Lucas sums conjecture: explicit counterexample | USD 250 | [vibemathing/problem-sun-prime-fibonacci-counterexample](https://github.com/vibemathing/problem-sun-prime-fibonacci-counterexample) |
| 130 | Project #2 bounty problem | `boyer-enigma-4c-awarded`：7x7 magic square of cubes | EUR 200 ≈ USD 232.44 | [vibemathing/problem-boyer-enigma-4c-awarded](https://github.com/vibemathing/problem-boyer-enigma-4c-awarded) |
| 131 | Project #2 bounty problem | `boyer-enigma-6b-awarded`：7x7 additive-multiplicative magic square | EUR 200 ≈ USD 232.44 | [vibemathing/problem-boyer-enigma-6b-awarded](https://github.com/vibemathing/problem-boyer-enigma-6b-awarded) |
| 132 | Project #2 bounty problem | `hou-zeng-fibonacci-catalan-counterexample`：Prime plus Fibonacci plus Catalan sums conjecture: explicit counterexample | USD 200 | [vibemathing/problem-hou-zeng-fibonacci-catalan-counterexample](https://github.com/vibemathing/problem-hou-zeng-fibonacci-catalan-counterexample) |
| 133 | Project #2 bounty problem | `kimberling-1`：Kimberling #1: Oldenburger-Kolakoski sequence | USD 200 | [vibemathing/problem-kimberling-1](https://github.com/vibemathing/problem-kimberling-1) |
| 134 | Project #2 bounty problem | `mse-triangulation`：Triangulation of a polygon cash reward | USD 200 | [vibemathing/problem-mse-triangulation](https://github.com/vibemathing/problem-mse-triangulation) |
| 135 | Project #2 bounty problem | `sun-prime-triangular-counterexample`：Prime plus triangular-number conjecture: explicit counterexample | USD 200 | [vibemathing/problem-sun-prime-triangular-counterexample](https://github.com/vibemathing/problem-sun-prime-triangular-counterexample) |
| 136 | Project #2 bounty problem | `sun-secondary-representation-200`：Sun representation riddle prize lead A | USD 200 | [vibemathing/problem-sun-secondary-representation-200](https://github.com/vibemathing/problem-sun-secondary-representation-200) |
| 137 | Project #2 bounty problem | `shallit-12`：Shallit BC4 Open Problem 12: Letter frequencies in Oldenburger–Kolakoski word | GBP 100 ≈ USD 135.31 | [vibemathing/problem-shallit-12](https://github.com/vibemathing/problem-shallit-12) |
| 138 | Project #2 bounty problem | `shallit-1`：Shallit BC4 Open Problem 1: Improve Robson upper bound for separating words | GBP 100 ≈ USD 135.31 | [vibemathing/problem-shallit-1](https://github.com/vibemathing/problem-shallit-1) |
| 139 | Project #2 bounty problem | `shallit-6`：Shallit BC4 Open Problem 6: Context-free interpolation between nested languages | GBP 100 ≈ USD 135.31 | [vibemathing/problem-shallit-6](https://github.com/vibemathing/problem-shallit-6) |
| 140 | Project #2 bounty problem | `shallit-8`：Shallit BC4 Open Problem 8: Three-real sequence with all Hankel determinants nonzero | GBP 100 ≈ USD 135.31 | [vibemathing/problem-shallit-8](https://github.com/vibemathing/problem-shallit-8) |
| 141 | Project #2 bounty problem | `boyer-enigma-3a-awarded`：7x7 semi-magic square of cubes | EUR 100 ≈ USD 116.22 | [vibemathing/problem-boyer-enigma-3a-awarded](https://github.com/vibemathing/problem-boyer-enigma-3a-awarded) |
| 142 | Project #2 bounty problem | `erdosproblems:101`：Erdős Problem #101 | USD 100 | [vibemathing/problem-um-ep-101-erd-s-problem-101-b444cc11](https://github.com/vibemathing/problem-um-ep-101-erd-s-problem-101-b444cc11) |
| 143 | Project #2 bounty problem | `erdosproblems:1029`：Erdős Problem #1029 | USD 100 | [vibemathing/problem-um-ep-1029-erd-s-problem-1029-0fa54302](https://github.com/vibemathing/problem-um-ep-1029-erd-s-problem-1029-0fa54302) |
| 144 | Project #2 bounty problem | `erdosproblems:104`：Erdős Problem #104 | USD 100 | [vibemathing/problem-um-ep-104-erd-s-problem-104-15bd3bf4](https://github.com/vibemathing/problem-um-ep-104-erd-s-problem-104-15bd3bf4) |
| 145 | Project #2 bounty problem | `erdosproblems:1123`：Erdős Problem #1123 | USD 100 | [vibemathing/problem-erdosproblems-1123](https://github.com/vibemathing/problem-erdosproblems-1123) |
| 146 | Project #2 bounty problem | `erdosproblems:119`：Erdős Problem #119 | USD 100 | [vibemathing/problem-erdosproblems-119](https://github.com/vibemathing/problem-erdosproblems-119) |
`vibe-mathing-cn` organizes mathematical problems, literature, derivations, computations, proofs, and formal checks into a traceable workflow. It is not a promise to solve arbitrary open problems: an honest `open` disposition is a valid outcome.

The repository's original code and documentation are released under the [MIT License](LICENSE); third-party material under `vendor/` remains subject to its own license and source lock.

## Start here

- [Architecture at a glance](#architecture-at-a-glance)
- [Quick start](#quick-start)
- [Core contract](#core-contract)
- [Single conceptual root](#single-conceptual-root-pointlinefacebody)
- [Top-level lifecycle](#top-level-lifecycle-project-workflow-task-step-job)
- [Method-layer map](#method-layer-map)
- [Candidate isolation](#candidate-isolation)
- [Public problem index](#public-problem-index)
- [Public capability boundaries](#public-capability-boundaries)
- [FAQ](#faq)
- [Machine-readable entrypoints](#machine-readable-entrypoints)
- [GEO facts and citation guide](#geo-facts-and-citation-guide)

## Quick start

From a clean public checkout:

```bash
git clone https://github.com/vibemathing/vibe-mathing-cn-public.git
cd vibe-mathing-cn-public
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
make check
```

To exercise the deterministic SymPy fixture:

```bash
python3 scripts/vibe_mathing_cli.py register-problem \
  --file fixtures/sympy-counterexample/problem.json
python3 scripts/vibe_mathing_cli.py run \
  --problem-id problem:sympy-counterexample-fixture
```

This is a synthetic engineering fixture, not an open-problem solver or a new mathematical result. The fixed Lean/Mathlib fixture is documented in [`fixtures/lean-proof/README.md`](fixtures/lean-proof/README.md).

## Public problem index

The public concrete-problem namespace is indexed in [`problem-library/VIBEMATHING_PUBLIC_INDEX.md`](problem-library/VIBEMATHING_PUBLIC_INDEX.md). It points to:

- [`vibe-mathing-problem-library-public`](https://github.com/vibemathing/vibe-mathing-problem-library-public), the external ProblemContract catalog;
- [`vibe-mathing-problem-public-template`](https://github.com/vibemathing/vibe-mathing-problem-public-template), the fixed Web research Harness template;
- the [`vibemathing` repository list](https://github.com/vibemathing?tab=repositories), which locates concrete `problem-*` repositories.

Read-only metadata queries:

```bash
make index-public-problems
python3 scripts/query_vibemathing_public.py --kind library
python3 scripts/query_vibemathing_public.py --kind concrete --limit 20
python3 scripts/query_vibemathing_public.py --catalog
```

Select a canonical catalog contract first, re-check its identity, lifecycle, statement, and digest, then enter the matching single-problem repository and follow `WEB_BOOTSTRAP.md`. Remote catalogs, Issues/PRs, and Web Harness transport do not automatically admit a local Problem, Attempt, Result, or Solution. A copyable local draft is [`problem-library/templates/problem-contract.template.json`](problem-library/templates/problem-contract.template.json); it remains `lifecycle=draft` until separately reviewed.

## Architecture at a glance

![vibe-mathing-cn two-layer architecture overview](assets/architecture.svg)

This static diagram is also a reading and routing model: PLFB is the single conceptual root; F05/PWTSJ organizes execution, F04/OSPS maintains outcome space, and F09/F10 adjudicates evidence and Results. Faces meet through explicit Lines but cannot close one another's state. Plain-text clients should start with [`POINT-LINE-FACE-BODY-METAMODEL-v0.1.md`](governance/standards/POINT-LINE-FACE-BODY-METAMODEL-v0.1.md); see [`RESEARCH-LIFECYCLE-MODEL-v0.1.md`](governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md) for F05 details.

## Core contract

The public workflow is:

```text
ProblemContract -> Attempt -> candidate/evidence -> Result
                                                    ├─> ResearchBundle (derived view)
                                                    └─> Solution View (derived index)
```

`ProblemContract` freezes the exact statement, domain, quantifiers, definitions, assumptions, allowed axioms, acceptance policy, and bounded runtime constraints. Only an active contract may create an Attempt. `ResearchBundle` is a read-only view derived from a consistent snapshot; it is not a fourth writable truth table.

The result state is two-dimensional:

- `outcome`: `undetermined | supported | established | refuted | inconclusive | withdrawn`;
- `evidence`: capabilities such as numeric, symbolic, human review, kernel check, counterexample check, axiom/escape audit, and statement faithfulness.

A finite computation, a Lean build, or a model self-review does not by itself establish a mathematical result. A proof and a counterexample that both pass closure for the same problem are a fail-closed conflict, not a choice between answers.

## Single conceptual root: Point–Line–Face–Body

Vibe Math uses **Point–Line–Face–Body (PLFB)** as its single conceptual metamodel root: stable objects are Points, typed directed relations are Lines, bounded knowledge or operation dimensions are Faces, and a reference-only Body composes Faces and cross-face Lines. PWTSJ, OSPS, Formal Methods, ProblemContract, Evidence, and Result are Faces or face-local models, not parallel top-level roots.

See [`POINT-LINE-FACE-BODY-METAMODEL-v0.1.md`](governance/standards/POINT-LINE-FACE-BODY-METAMODEL-v0.1.md) for the public Face map, cross-face bindings, four graphs plus one ledger, and Body boundary. This release defines a conceptual standard; it does not claim an implemented PLFB registry service, Body runtime, OSPS orchestrator, or unified Observation Ledger.

## Top-level lifecycle: Project → Workflow → Task → Step → Job

PWTSJ belongs to PLFB Face F05. `Project` defines the complete goal, `Workflow` defines the task network, `Task` defines an input/output work unit, `Step` defines an operation and its method, and `Job` records one bounded execution. A Step may create multiple Jobs for parameter variants, bounded retries, or independent verification; recovering one Job requires a verified checkpoint, while rerunning creates a new Job.

This execution structure is orthogonal to F04 Outcome Space, F09 Evidence, and F10 Result:

```text
Project → Workflow → Task → Step → Job

ProblemContract → Attempt → candidate/evidence → Result → Solution View
```

`Job succeeded ≠ Step accepted ≠ Obligation closed ≠ OutcomeNode closed ≠ Result admitted ≠ Project solved`. The public repository treats this as the F05 architecture and routing language; it does not claim to provide a general scheduler, five persistent lifecycle schemas, an OSPS runtime, or multi-worker production capability. See [`RESEARCH-LIFECYCLE-MODEL-v0.1.md`](governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md).

## Method-layer map

The project uses a two-level map rather than treating a Lean tutorial index as the whole field:

```text
Specification & Semantics
  -> Deductive Verification / Theorem Proving (Lean's main territory)
  -> Model Checking / Abstract Interpretation / SAT-SMT-Symbolic Reasoning (including Symbolic Execution)
  -> Refinement & Synthesis

Lean stack: Type Theory & Kernel -> Language & Elaboration -> Proof Engineering
  -> Automation & Decision Procedures -> Library Engineering -> Applications
```

`ProblemContract` freezes specification and semantics; `math-proof` handles proof obligations; `math-formalization` separates Lean statements, proof terms, kernel checks, axiom/escape audits, and statement faithfulness; `math-computation` handles bounded computation and horizontal automation. Lean is a dependent-type-theory theorem-proving platform, not a synonym for all formal methods. See the full [`FORMAL-METHODS-MAP.md`](governance/standards/FORMAL-METHODS-MAP.md) for the taxonomy, learning order, and source map.

## Candidate isolation

A `CandidateObservation` is a discovery record, not a canonical ProblemContract. It remains `research_eligible=false` and cannot create an Attempt, Result, or Solution. Source labels such as `open`, `answered`, `resolved`, and `solved` are preserved as source metadata only; they are not mathematical outcomes.

The default problem query collection is `admitted`. Candidate queries must explicitly use `--collection candidates` or `--collection all`.

```bash
python3 scripts/query_problem_library.py --collection admitted --text Riemann --limit 10
python3 scripts/query_problem_library.py --collection candidates --limit 20
python3 scripts/build_candidate_observations.py
python3 scripts/validate_candidate_problem_library.py --verify-raw
```

Raw source responses, candidate snapshots, research records, runtime logs, credentials, private paths, and machine identities are not distributed in the public repository.

## Public capability boundaries

The 41-family tool registry uses:

```text
surveyed -> source_locked -> installed -> smoke_checked -> evidence_capable -> verifier_admitted
```

This is an evidence state machine, not an installation report. The public catalog is [`governance/tools/MATH_TOOL_CATALOG.md`](governance/tools/MATH_TOOL_CATALOG.md); the machine registry is [`governance/control-plane/math-tool-maturity.v1.json`](governance/control-plane/math-tool-maturity.v1.json). Families without public runtime evidence remain surveyed or source-locked.

Bounded canaries cover positive, negative, error, and timeout behavior. They test runtime protocol only and never create mathematical Results. Every computation, solver, CAS, external command, HTTP request, and canary subprocess must have a timeout, resource budget, output/response bound, stop condition, termination receipt, and explicit failure semantics.

## Verification

```bash
make check
python3 scripts/audit_public_status.py --format json --expect-empty
python3 scripts/validate_math_tool_maturity.py
python3 scripts/check_math_tools.py --profile portable --strict
MATH_CANARY_SOURCE_SHA256="$(sha256sum scripts/run_math_tool_canaries.py | awk '{print $1}')" \
  python3 scripts/run_math_tool_canaries.py --tools T13,T15,T16 --json --strict
```

For the complete model and Chinese documentation, see [`README.md`](README.md), [`problem-library/README.md`](problem-library/README.md), [`research/README.md`](research/README.md), and [`result-library/README.md`](result-library/README.md).

## Status

The repository publishes reusable schemas, owner skills, governance rules, bounded fixtures, source locks, and validation code. It does not claim a complete solution to any Millennium Prize problem or any other open mathematical problem.

## FAQ

### How should current status and external catalog information be verified?

Use the three canonical ledgers and `solutions.json` for local status. Treat external counts and repository states as dated snapshots, and re-read the remote contract, index, and digest before research. A verification date does not guarantee future freshness.

### Does this project solve an open mathematics problem?

No. The canonical Problem, Attempt, and Result ledgers are empty, the public solution index has no result IDs, and no open-problem solution is claimed.

### Why is a passing test not a proof?

A test checks code or a bounded input. It does not automatically establish a universal statement, natural-language statement faithfulness, independence, or novelty.

### What is the difference between a CandidateObservation and a Result?

A CandidateObservation is source-discovery input and remains outside research admission. A Result is a scoped atomic claim with outcome and evidence; a discovery record or proof draft cannot skip that boundary.

### What does the Lean fixture show?

It checks a fixed formal statement, proof term, and axiom/escape audit path. It does not automatically formalize or validate arbitrary natural-language mathematics.

### Why is `solutions.json` empty?

It is a derived read-only index. Only a proof or counterexample Result that passes direct verification, independence, and statement-faithfulness gates can enter it.

## Machine-readable entrypoints

- [`llms.txt`](llms.txt): concise retrieval context;
- [`GEO.md`](GEO.md): canonical facts, citation targets, and negative-boundary guide for humans and generative engines;
- [`assets/ai-citation/retrieval-contract.v1.json`](assets/ai-citation/retrieval-contract.v1.json): machine-readable intents, citations, and non-inference rules;
- [`scripts/query_ai_citation.py`](scripts/query_ai_citation.py): read-only rendering of fixed intent answers and stable citation URLs;
- [`scripts/audit_public_status.py`](scripts/audit_public_status.py): read-only status and SHA-256 snapshot audit for the canonical ledgers and solution index; it creates no Result;
- [`assets/ai-citation/schema-org-software.v1.json`](assets/ai-citation/schema-org-software.v1.json): Schema.org software-entity metadata for discovery and citation, not mathematical evidence;
- [`assets/ai-citation/`](assets/ai-citation/): summaries, terminology, bilingual answer matrix, GEO evaluation protocol, and report template;
- [`governance/publication/public-claims.v1.json`](governance/publication/public-claims.v1.json): public claims and evidence references;
- [`governance/control-plane/plfb-metamodel.v0.1.json`](governance/control-plane/plfb-metamodel.v0.1.json) and [`plfb-metamodel.schema.json`](governance/control-plane/plfb-metamodel.schema.json): conceptual types, F01–F13, B0–B4, and capability boundaries without business instances;
- [`scripts/validate_plfb_metamodel.py`](scripts/validate_plfb_metamodel.py): rejects duplicates, dangling references, wrong Face ownership, PWTSJ/OSPS misplacement, and false runtime capability claims;
- [`problem-library/VIBEMATHING_PUBLIC_INDEX.md`](problem-library/VIBEMATHING_PUBLIC_INDEX.md): external concrete-problem catalog, repositories, and Web research template entrypoint;
- [`governance/standards/POINT-LINE-FACE-BODY-METAMODEL-v0.1.md`](governance/standards/POINT-LINE-FACE-BODY-METAMODEL-v0.1.md): the single PLFB conceptual root and cross-face/Body boundaries;
- [`governance/standards/FORMAL-METHODS-MAP.md`](governance/standards/FORMAL-METHODS-MAP.md): the formal-methods taxonomy and Lean positioning;
- [`governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md`](governance/standards/RESEARCH-LIFECYCLE-MODEL-v0.1.md): the Project → Workflow → Task → Step → Job lifecycle model;
- [`CITATION.cff`](CITATION.cff) and [`codemeta.json`](codemeta.json): citation and software metadata;
- [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`SECURITY.md`](SECURITY.md): contribution and security boundaries.

Here, GEO means Generative Engine Optimization for accurate entity identification, status, evidence, and boundaries. It measures documentation understanding and citation accuracy, not ranking, recommendation, or mathematical correctness.

## GEO facts and citation guide

For a compact, citation-ready description, start with [`GEO.md`](GEO.md), then cite the nearest first-party source: `solutions.json` and the three ledgers for current status, the Problem/Attempt/Result schemas for the workflow, [`FORMAL-METHODS-MAP.md`](governance/standards/FORMAL-METHODS-MAP.md) for method positioning, and [`VIBEMATHING_PUBLIC_INDEX.md`](problem-library/VIBEMATHING_PUBLIC_INDEX.md) for external problem pointers. Preserve the empty-ledger, Lean-position, pointer-only, and external-snapshot-revalidation boundaries.
