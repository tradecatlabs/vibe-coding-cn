---
name: web3-start-here
description: Master index for the web3 smart contract security knowledge base. Use this to navigate the skill chain. Read files in order — each ends with NEXT.
---

# WEB3 SKILLS — MASTER INDEX

> Built from: 2,749 Immunefi reports + 100+ paid writeups + DeFiHackLabs (681 hacks) + ConsenSys + SlowMist + Trail of Bits + Foundry + Nethermind + Lido + AI agent research + live hunt experience

---

## THE CHAIN (read in this exact order)

```
00-START-HERE.md              ← YOU ARE HERE
01-foundation.md              ← Mindset, target selection, recon setup
02-bug-classes.md             ← All 10 bug classes with patterns + real examples
03-grep-arsenal.md            ← Master grep patterns for every class
04-poc-and-foundry.md         ← Foundry PoC writing, cheatcodes, 18 exploit templates
05-triage-report-examples.md  ← 7-Question Gate, report format, 20 real paid examples
06-methodology-research.md    ← ToB, SlowMist, ConsenSys, Immunefi, Cyfrin, Lido, Nethermind
07-live-hunt-ern.md           ← Completed hunt: Ern protocol (2 findings)
09-live-hunt-zksync.md        ← Completed hunt: ZKsync Era (0 findings — defense study)
08-ai-tools.md                ← Shannon, LuaN1ao, SmartGuard, CAI Framework, AI code hunting
36-solidity-audit-mcp.md      ← MCP server: Slither+Aderyn+SWC in Claude Code
```

---

## HOW TO USE THIS

1. Read one file fully — every section
2. At the bottom: follow → NEXT
3. **After file 05**: you can hunt independently
4. **Files 06-08**: advanced tools + active work
5. **File 36**: MCP integration for live scanning

---

## QUICK STATS

| Metric | Number |
|--------|--------|
| Immunefi reports analyzed | 2,749 |
| Protocols covered | 51 |
| Critical reports | 406 |
| High reports | 616 |
| Total paid by Immunefi | $100M+ |
| Avg critical payout | $50K–$2M |
| Nethermind reports analyzed | 166 |
| DeFiHackLabs hacks reproduced | 681 |

---

## THE ONE RULE

> "Read ALL sibling functions. If `vote()` has a modifier, check `poke()`, `reset()`, `harvest()`. The missing modifier on the sibling IS the bug."

This single rule explains 19% of all Critical findings.

---

→ NEXT: [01-foundation.md](01-foundation.md)
