---
name: web3-hunt-foundation
description: Hunter mindset, recon setup, and target scoring for Web3 bug bounty. Use at the START of any new protocol hunt - scoring targets, setting up environment, understanding architecture.
Contains: attack/triage mental models, 10-point scorecard (score ≥6 to proceed), crown jewels approach, static analysis setup, recon checklist.
---

# WEB3 HUNT FOUNDATION
> Mindset + Recon + Setup. Read this before touching any new target's code.
> Replaces: 01-mindset, 02-recon-setup, 20-chain-complete

---

## PART 1: THE HUNTER MINDSET

### The Core Mental Shift

You are NOT looking for "vulnerabilities" in the abstract.
You are looking for **specific actions an attacker can take TODAY that result in profit**.

Everything flows from one question: **"What can I STEAL, FREEZE, or DESTROY — and what do I END UP WITH?"**

### The Bug Validation Template

Apply to every finding before writing a single line:

```
I am an attacker. I will:
1. SETUP:   What do I need? (wallet, capital, any whitelisted permissions?)
2. CALL:    Exact transactions, exact order, exact function names
3. RESULT:  What do I end up with that I didn't start with?
4. COST:    Gas + capital + flash loan fee + any other expense
5. DETECT:  Can anyone stop or reverse this?
6. NET ROI: I gained X at cost of Y. Is Y << X?
```

If you can't fill in steps 2 and 3 with specific function calls → **it's not a real bug. Stop. Move on.**

### 10 Attacker Questions (Ask For Every External Function)

1. What if `amount = 0`? Does anything revert or silently pass?
2. What if I call this function twice in the same block?
3. What if I call this before `initialize()` is called?
4. What if I front-run this transaction?
5. What if the external call fails? Does state get half-updated?
6. What if the token has fee-on-transfer? Does `amount received ≠ amount sent`?
7. What if I pass `address(0)` or a malicious contract as an address param?
8. What if I pass `type(uint256).max` as a numeric param?
9. Can I combine this with a flash loan? (zero-cost capital changes the math)
10. **Does a sibling function lack the same modifier this function has?**

> Question #10 explains 19% of all Critical findings. If `vote()` has `onlyRole(VOTER)`, check `poke()`, `reset()`, `harvest()` — the missing modifier on the sibling IS the bug.

### 6 Triager Counter-Questions (Disprove Your Own Finding)

Before spending time on a PoC, try to KILL the finding:

1. Is there an upstream check I missed that actually prevents this?
2. Is this documented intended behavior (whitepaper, NatSpec, design decision)?
3. Does exploitation require admin/privileged access? (Usually invalid if yes)
4. Is the economic cost to exploit greater than the gain? (Not viable if yes)
5. Was this flagged in a prior audit as "acknowledged" or "risk accepted"?
6. Is the "sensitive" data already publicly visible to anyone in the web UI?

**One YES = KILL. Move on.**

### 5-Minute Rule

If you've been on the same function for 5 minutes with no clear attack path → **STOP.**
Add it to a low-priority list. Move to the next function.
Top hunters: 95% fast-reject + 5% deep dives on confirmed leads.

### Depth Over Breadth

Don't review 10 protocols in one week. Pick ONE. Spend 3-5 days becoming the expert.
Protocol-specific knowledge compounds. The Curve expert found 5 bugs. The 10-protocol tourist found 0.

### Inconsistency Is Proof

If `functionA()` has a security check, and `functionB()` doesn't — **that IS the report.**
You don't need to fully understand why. The inconsistency proves the developer intended the check.

---

## PART 2: TARGET SCORING — GO / NO-GO

Before touching any code: score the target. **Score < 6 → skip.**

### Target Scorecard

| Criterion | Points | How to Check |
|-----------|--------|-------------|
| Max bounty ≥ $50K | +2 | Immunefi program page |
| TVL > $1M | +2 | DeFiLlama |
| Program launched < 30 days ago | +2 | Immunefi "new" filter |
| Custom math (AMM/vault/lending) | +1 | Read scope contracts |
| Recent code changes | +1 | `git log --oneline -20` |
| Prior audits available | +1 | Program page / GitHub |
| In-scope includes smart contracts | +1 | Scope section |
| Protocol type you know well | +1 | Your specialization |
| Source code public/readable | +1 | GitHub / Etherscan verified |

**< 4:** Skip — too small, too audited, wrong fit
**4-5:** Only if nothing better available
**6-8:** Good — spend 1-3 days
**≥ 9:** Excellent — spend up to 1 week

---

## PART 3: RECON METHODOLOGY (30-Minute Protocol)

### Step 1 — Read Immunefi Page (5 min)

```
Note:
- All in-scope contract addresses + GitHub links
- Out-of-scope list (DO NOT report these)
- Primacy of Impact: YES/NO (YES = more forgiving on novel impacts)
- Max bounty amounts by severity
- Time on Immunefi (newer = fewer duplicates)
```

### Step 2 — Clone + Setup (5 min)

```bash
git clone <target-repo>
cd <target-repo>
git log --oneline -20       # Recent changes = freshest bugs here
forge build                 # Must compile clean (fix if not)
forge test                  # Note failures — may indicate known issues
forge coverage              # Untested code = priority review target
```

### Step 3 — Read ALL Prior Audit Reports (15 min)

For each finding, note its status:
- **Fixed:** Skip
- **Acknowledged / Risk Accepted:** ⚡ **START HERE** ⚡
  - Developer knows about it but chose not to fix it
  - Variants, escalations, related attack paths = in-scope and uncovered
- **Partially Fixed:** Verify fix actually closes ALL attack paths

Find audits: GitHub repo, protocol docs, Immunefi page, Google "[protocol] audit report"

### Step 4 — Crown Jewels (2 min)

Ask: **"Worst thing an attacker could do to users of this protocol?"**

Work backward from impact to code:
- "Steal deposits" → find: withdrawal functions, access control on transfer
- "Mint infinite tokens" → find: mint functions, who calls them, what checks
- "Freeze all funds" → find: emergency functions, time locks, role assignments
- "Steal all rewards" → find: reward distribution, distributor role, harvest functions

### Step 5 — Architecture + Fund Flow (3 min)

Draw the money flow (even mentally):
```
User USDC
   ↓ deposit()
[Protocol Vault] ──→ External Protocol (Aave/Compound/Uniswap)
   ↓ yield accumulates
[Reward Distributor] ──→ Users via claim/harvest
```

Find WHERE VALUE ACCUMULATES. That contract = highest priority.

Key state variables to map:
- Total deposited / total assets / total shares
- Per-user balance tracking (how is it updated?)
- Reward accumulator (index, per-share, per-second?)
- Role assignments (owner, admin, governance, distributor)
- Time locks (timestamps, epochs, cooldowns)

### Step 6 — Static Analysis (5 min)

```bash
# Slither — 93 detectors, fast
slither . --exclude-low --filter-paths "test|lib|node_modules"
slither . --detect reentrancy-eth,unprotected-upgrade,arbitrary-send-eth

# Aderyn — Rust-based, Foundry-native
aderyn . --output report.md

# Read output → note HIGH/CRITICAL only
# Tools catch ~30-40% of bugs. Human review finds the rest.
```

---

## PART 4: RECON CHECKLIST

Run through this before any deep review:

```
PROGRAM:
[ ] Max bounty noted per severity
[ ] ALL in-scope contracts listed (name + address)
[ ] Out-of-scope list read — nothing to falsely report
[ ] Primacy of Impact: YES/NO noted
[ ] Program launch date noted (new = good)

PRIOR AUDITS:
[ ] All audit PDFs downloaded and scanned
[ ] Each finding: status noted (Fixed/Ack/Risk Accepted)
[ ] Acknowledged items in notes as starting points

CODEBASE:
[ ] git clone + forge build passes
[ ] git log checked — recent commits noted
[ ] forge coverage run — untested functions noted
[ ] Slither + Aderyn run — high/critical noted

ARCHITECTURE:
[ ] Fund flow drawn
[ ] Crown jewels identified (where value lives)
[ ] External dependencies mapped (Chainlink, Uniswap, Aave, etc.)
[ ] ALL privileged roles found (onlyOwner, onlyRole, etc.)
[ ] Proxy/upgradeable pattern identified (if any)

ATTACK SURFACE:
[ ] All external/public non-view functions listed
[ ] Mint/burn functions located
[ ] Withdraw/emergencyWithdraw functions located
[ ] Upgrade/migration functions located
[ ] Oracle dependencies found
[ ] Signature/permit usage found
[ ] Cross-contract interactions mapped
```

---

## ATTACK SURFACE BY PROTOCOL TYPE

```
DEX / AMM:
- Oracle manipulation (getReserves, slot0 = flash-loan manipulable)
- Rounding in pool math (1-wei attacks × flash swap)
- Missing slippage protection (sandwich vector)
- Fee-on-transfer token handling

LENDING / BORROWING:
- Collateral valuation (oracle → overborrow)
- Liquidation logic (bad debt creation, self-liquidation)
- Interest accrual rounding (favors borrower or protocol?)
- Flash loan → inflate collateral → borrow → repay

VAULT / YIELD:
- First depositor share inflation (ERC4626)
- Donation attack via direct balanceOf transfer
- Strategy rug (malicious strategy contract)
- Reward accounting timing (enter/exit attacks)

BRIDGE / CROSS-CHAIN:
- Message replay (missing nonce/nullifier)
- Signature replay (no chainId)
- Validator set manipulation
- Destination execution reentrancy

STAKING / RESTAKING:
- Reward distribution timing attacks
- Slashing logic errors
- Role never granted → permanent lock
- Withdrawal queue multi-field desync
```

---

## WHEN TO RE-READ THIS CHAIN

| Situation | File to Read |
|-----------|-------------|
| Starting new hunt | **This file** |
| Need specific grep commands | 03-grep-arsenal |
| Found a bug, building PoC | 04-poc-and-foundry |
| Ready to validate + submit | 05-triage-report |
| Need all bug class patterns | 02-bug-classes |
| Want external research depth | 06-methodology |
| Hunting Ern protocol | 07-live-hunt-ern |
| Want AI tool automation | 08-ai-tools |

---

→ NEXT: [02-bug-classes.md](02-bug-classes.md)
