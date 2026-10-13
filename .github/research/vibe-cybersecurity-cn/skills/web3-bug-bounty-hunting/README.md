<div align="center">

# web3-bug-bounty-hunting-ai-skills

Smart contract bug bounty skills for Claude Code, Claude AI, and other AI tools.
Built from 2,749 Immunefi reports, 681 DeFiHack reproductions, and real hunts.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-11-blue)]()
[![Immunefi](https://img.shields.io/badge/Immunefi%20reports-2%2C749-orange)]()
[![DeFiHackLabs](https://img.shields.io/badge/DeFiHack%20reproductions-681-red)]()

</div>

---

Most hunters still do everything manually. Read contracts in a browser, grep from memory, rewrite Foundry templates each hunt, draft reports from scratch.

These skill files load into Claude Code (or any AI) and give it a complete smart contract security knowledge base — target scoring, bug patterns, grep arsenal, PoC templates, report format, and real case studies. One `claude` command, then start hunting.

Works with: **Claude Code**, **Claude.ai**, **Cursor**, **any AI that reads files**.

---

## Files

| File | Contents |
|------|----------|
| [`00-start-here.md`](./00-START-HERE.md) | Index + how to navigate |
| [`01-foundation.md`](./01-foundation.md) | Hunter mindset, target scoring (10-point scorecard), recon setup |
| [`02-bug-classes.md`](./02-bug-classes.md) | All 10 bug classes — patterns, Solidity examples, real Immunefi findings |
| [`03-grep-arsenal.md`](./03-grep-arsenal.md) | Grep/regex patterns for every bug class |
| [`04-poc-and-foundry.md`](./04-poc-and-foundry.md) | 18 Foundry PoC templates — fill in address, run `forge test` |
| [`05-triage-report-examples.md`](./05-triage-report-examples.md) | 7-question validation gate, Immunefi report format, 20 paid examples |
| [`06-methodology-research.md`](./06-methodology-research.md) | Trail of Bits, SlowMist, ConsenSys, Cyfrin, Nethermind methodology |
| [`07-case-study-role-misconfiguration.md`](./07-case-study-role-misconfiguration.md) | Full hunt walkthrough — role misconfiguration bug, real findings |
| [`08-ai-tools.md`](./08-ai-tools.md) | Shannon, SmartGuard, CAI Framework, LuaN1ao agent setup |
| [`09-case-study-hardened-l2-bridge.md`](./09-live-hunt-zksync.md) | Defense study — 25 attack vectors tested on a hardened L2 bridge |
| [`36-solidity-audit-mcp.md`](./36-solidity-audit-mcp.md) | MCP server — run Slither + Aderyn + SWC inside Claude Code |

Read in order. Each file ends with `→ NEXT`. After file 05 you can hunt on your own.

---

## The 10 Bug Classes

```
01  Accounting Desync    →  most common Critical (37% of all payouts)
02  Access Control       →  most common High
03  Incomplete Path      →  missing modifier on a sibling function
04  Off-by-One           →  boundary operators, index errors
05  Oracle Price         →  TWAP manipulation, stale prices
06  ERC4626 Vaults       →  share inflation, rounding attacks
07  Reentrancy           →  cross-function, cross-contract, read-only
08  Flash Loan           →  price manipulation, economic attacks
09  Signature Replay     →  cross-chain replay, missing nonce/chainId
10  Proxy/Upgrade        →  uninitialized implementation, storage collision
```

> Read ALL sibling functions. If `vote()` has a modifier, check `poke()`, `reset()`, `harvest()`.
> The missing modifier on the sibling is the bug. This one rule explains 19% of all Criticals.

---

## Setup

**Option 1 — drop into your existing project:**

```bash
git clone https://github.com/shuvonsec/web3-bug-bounty-hunting-ai-skills.git .claude/skills/web3
claude
```

Then in Claude Code:
```
Read all files in .claude/skills/web3/ starting from 00-START-HERE.md
```

**Option 2 — standalone workspace:**

```bash
git clone https://github.com/shuvonsec/web3-bug-bounty-hunting-ai-skills.git
cd web3-bug-bounty-hunting-ai-skills
claude
```

**Option 3 — just the essentials:**
```
Read 02-bug-classes.md and 04-poc-and-foundry.md
```

---

## Numbers

| | |
|---|---|
| Immunefi reports analyzed | 2,749 |
| Critical findings | 406 |
| High findings | 616 |
| Total paid by Immunefi | $100M+ |
| DeFiHackLabs reproductions | 681 |
| Nethermind audit reports | 166 |
| Protocols covered | 51 |

---

## Related

| Repo | What it does |
|------|-------------|
| [claude-bug-bounty](https://github.com/shuvonsec/claude-bug-bounty) | Point at a target → full attack surface map + Immunefi/Bugcrowd report |
| [public-skills-builder](https://github.com/shuvonsec/public-skills-builder) | Feed 500 public writeups → get skill files like these back out |

---

MIT License. Use it, fork it, build on it.
