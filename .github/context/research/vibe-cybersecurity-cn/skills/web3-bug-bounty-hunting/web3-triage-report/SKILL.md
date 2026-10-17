---
name: web3-triage-report
description: Bug triage validation system, Immunefi report format, and 20 real paid bounty examples dissected. Use this when validating a finding before submitting, writing an Immunefi report, checking if a bug is actually valid, or studying real examples of paid vulnerabilities.
---

# TRIAGE, REPORT WRITING & REAL EXAMPLES

---

## PART 1: TRIAGE

### THE 7-QUESTION GATE

Ask these IN ORDER before writing a single word of your report.
ONE wrong answer = STOP and move on.

---

#### Q1: Can an attacker use this RIGHT NOW, step by step?

Complete this template:
```
1. Setup:   [what I need]
2. Call:    [exact function, exact params]
3. Result:  [what I have that I didn't have before]
4. Cost:    [gas + capital]
5. ROI:     [profit / cost ratio]
```

If you cannot complete steps 2 and 3 with specific function calls: **KILL IT.**

---

#### Q2: Is the impact in the program's accepted impact list?

Go to the Immunefi program page. Find "Impacts in Scope."
Match your bug to one of these EXACTLY.

Example impact tiers:
- "Direct theft of any user funds" — Critical
- "Permanent freezing of funds" — Critical
- "Protocol insolvency" — Critical
- "Theft of unclaimed yield" — High
- "Permanent freezing of unclaimed yield" — High
- "Temporary freezing of funds" — High
- "Smart contract unable to operate due to lack of token funds" — Medium
- "Griefing (no profit motive, but damage to users)" — Medium
- "Contract fails to deliver promised returns, but doesn't lose value" — Low

If your bug does not match any impact in scope: **KILL IT.**

---

#### Q3: Is the root cause in an in-scope contract?

Confirm the exact deployed address is in scope on the program page.

If the bug is in Aave, Uniswap, OpenZeppelin, or any external dependency: **KILL IT.**

---

#### Q4: Does it require admin/privileged access?

"Admin can drain funds" = centralization risk = **KILL IT.**
"Admin can set parameter X which under condition Y creates DoS" = borderline.

Salvage path: can the bug trigger WITHOUT the admin doing anything unusual?
- If yes: valid
- If no: likely invalid (requires admin mistake — almost always out of scope)

---

#### Q5: Is this already known/acknowledged in prior audits?

Find the audit reports for the protocol. Search for "Risk Accepted," "Acknowledged," "Won't Fix."

If your bug matches a known finding: **KILL IT.**

Edge case: if acknowledged finding + NEW code around it creates a new attack path → that is a new bug, not the acknowledged one. Must prove the new path.

---

#### Q6: Is the economic attack viable?

```
Attacker spends: gas + capital
Attacker gains: tokens stolen or protocol damaged

If profit < cost: KILL IT.
```

Example:
- DoS via dust harvest: costs 1 wei USDC + gas, disables yield for $81K TVL → VIABLE.
- Withdraw-fee arbitrage: fee (0.1%) > diluted yield from attack → NOT profitable → KILL IT.

---

#### Q7: Is this already public?

- Is it on social media or in a disclosed report?
- Was it previously submitted and disclosed?
- Is the "sensitive" data visible in the UI already?

If yes: **KILL IT.**

---

### THE SEVERITY MATRIX

Score = Impact × Likelihood × Exploitability (each 1–3)

| | Impact=1 (info leak) | Impact=2 (partial) | Impact=3 (theft/freeze) |
|--|--|--|--|
| L=1 E=1 | 1 (Info) | 2 (Low) | 3 (Low) |
| L=2 E=2 | 4 (Medium) | 8 (High) | 12 (High) |
| L=3 E=3 | 9 (High) | 18 (Critical) | 27 (Critical) |

**Rule: When borderline, round DOWN. Over-classification destroys credibility.**

---

### THINK LIKE AN ATTACKER TEMPLATE

Before writing your report, fill in this attack scenario:

```
Protocol: [name]
Target contract: [address + function]
Preconditions: [what state must exist?]
Attack sequence:
  1. Attacker calls [exact function] with [exact params]
  2. [What happens in the contract]
  3. [What state changes]
  4. Attacker ends up with: [X more tokens / broken state / DoS]
Total cost: [gas estimate + capital requirement]
Total gain: [$X stolen / $Y TVL frozen]
Viable? [yes/no + reason]
```

If you can't fill in steps 1–4 with specific values, the bug is not ready to submit.

---

### THINK LIKE A TRIAGER CHECKLIST

A triager reviewing your report will immediately check:

- [ ] Does the title match an accepted impact?
- [ ] Is the vulnerable function clearly identified (file + line)?
- [ ] Is the root cause explained (not just "there is a bug")?
- [ ] Is there comparison evidence ("function A has this, function B doesn't")?
- [ ] Does the PoC run without errors?
- [ ] Is the severity appropriate to the actual impact?
- [ ] Is the bug already in the known issues list?
- [ ] Does the fix make sense (proves you understand the root cause)?

If your report can't pass this checklist: revise before submitting.

---

### SEVERITY DOWNGRADE TRIGGERS

| Condition | Severity drops |
|-----------|---------------|
| Requires specific admin configuration | -1 level |
| Impact limited to a small subset of users | -1 level |
| Requires long time window (>24h) to exploit | -1 level |
| Protocol can detect and pause before loss | -1 level |
| Impact is yield loss, not principal loss | -1 level |
| Bug is theoretical with no practical attack | Down to Info |
| Attack costs more than attacker gains | Invalid |

---

### VALID vs INVALID COMPARISON TABLE

| Bug | Valid? | Reason |
|-----|--------|--------|
| DISTRIBUTOR_ROLE never granted → claimFor() permanently uncallable | **Valid (Medium)** | Deployment bug, not admin action, real impact on users |
| `- 1` strands 1 wei per harvest | **Valid (Low/Info)** | Real, quantified, honest about minor impact |
| Front-run harvest (acknowledged in prior audit) | **Invalid** | Known issue = instant rejection |
| Admin can change fee to 100% | **Invalid** | Centralization risk = almost always OOS |
| Harvest DoS via dust (requires admin misconfiguration) | **Borderline** | Must prove it triggers without unusual admin action |
| ecrecover returns address(0) = anyone can pass | **Valid (Critical)** | No preconditions, direct theft |
| Contract uses spot price oracle | **Valid (High/Critical)** | Flash loan manipulation, well-documented impact |
| Missing slippage parameter | **Valid (Medium)** | MEV sandwich possible, quantifiable loss |
| GraphQL introspection enabled | **Invalid** | Info disclosure only, no exploitation path |
| Missing HSTS header | **Invalid** | Always rejected |

---

### THE VALIDITY RATIO

Immunefi tracks your submission:triage ratio.
High invalid submission rate → your future reports get lower priority.

**Target: 70%+ valid submissions.**

Better to submit 3 valid bugs than 10 invalid ones.
A low-severity honest submission is better for your ratio than an overclaimed invalid one.

---

## PART 2: REPORT WRITING

### THE WINNING FORMULA

1. **Title** = [Exact function] + [root cause] + [quantified impact]
2. **Comparison evidence** = "Function A has X, Function B doesn't"
3. **Attack path** = numbered steps, each with exact function call
4. **Quantified impact** = "$X stolen" or "X% yield diluted"
5. **PoC output** = actual console.log numbers, not just "test passes"
6. **1-line fix** = proves you understand the root cause

---

### IMMUNEFI REPORT TEMPLATE (Complete)

```markdown
## [Exact function in ContractName] — [root cause in 10 words] leads to [quantified impact]

### Example title:
"_performHarvest() in Ern.sol subtracts hardcoded 1 wei causing reward token
permanent lockup across all harvests"

---

## Summary

[2-3 sentences maximum. What is the bug, where is it, what does it enable.]

The `_performHarvest()` function in `Ern.sol` subtracts a hardcoded `1` from
`userRewards` without distributing or accounting for the remainder. This causes
1 wei of reward token to be permanently locked in the contract after every
harvest, and — more critically — causes a revert when Uniswap returns 0 output
for dust-amount swaps, permanently freezing the harvest function.

---

## Vulnerability Details

**Contract:** `Ern.sol`
**Function:** `_performHarvest()`, line 187
**Type:** Arithmetic error / Incomplete path

**Vulnerable Code:**
```solidity
uint256 protocolFee = (rewardReceived * harvestFee) / 10000;
uint256 userRewards = rewardReceived - protocolFee - 1;  // ← BUG: hardcoded -1
if (protocolFee > 0) REWARD_TOKEN.safeTransfer(owner(), protocolFee);
if (totalSharesSupply > 0) {
    cumulativeRewardPerShare += (userRewards * 1e18) / totalSharesSupply;
}
```

**Comparison Evidence:**
Function `claimYield()` at line 120 correctly handles zero-amount cases.
`_performHarvest()` at line 187 does not account for the stranded `1 wei`
remainder, creating a silent fund loss on every harvest.

**Root Cause:**
The `- 1` subtraction creates a permanent accounting gap. The 1 wei:
- Is NOT sent to the protocol fee recipient (owner)
- Is NOT distributed to users via `cumulativeRewardPerShare`
- Remains locked in the contract indefinitely with no recovery mechanism

**Attack Path (numbered, each step is a specific function call):**
1. Owner sets `minYieldAmount` to minimum (1 * 10^6 = 1 USDC)
2. `harvestTimePeriod` passes (24 hours by default)
3. Yield accrued: 1 wei of aUSDC above totalSupply
4. `canHarvest()` returns `true` (time condition satisfied)
5. Harvester calls `harvest(0)` with `minOut = 0`
6. `yieldAmount = 1` → Aave withdraws 1 wei USDC
7. Uniswap `exactInputSingle(1 wei USDC → WBTC)` returns `0` output
8. `rewardReceived = 0`
9. `userRewards = 0 - 0 - 1 = type(uint256).max` ← ARITHMETIC UNDERFLOW
10. Transaction reverts. All future harvests permanently blocked.

---

## Impact

**Severity:** High
**Category:** Temporary freezing of funds

**Quantified Impact:**
- ernUSDC TVL: $69,300
- ernUSDT TVL: $12,000
- All accrued wBTC yield frozen for all depositors
- Recovery requires owner intervention or protocol upgrade

**Preconditions:**
[list any setup conditions required]

---

## Proof of Concept

[Working Foundry test that runs with forge test -vvv]
[Must include console.log output showing actual numbers]
[Must compile and pass cleanly]

**Expected Output:**
```
[PASS] testHarvestDoS()
Logs:
  canHarvest: true
  yieldAmount: 1
  harvest() REVERTS: arithmetic underflow confirmed
  All future harvests blocked until owner intervenes
```

---

## Recommended Fix

**Option 1 — Remove the unexplained `-1`:**
```solidity
// Before:
uint256 userRewards = rewardReceived - protocolFee - 1;

// After:
uint256 userRewards = rewardReceived - protocolFee;
```

**Option 2 — Guard against zero rewardReceived:**
```solidity
if (rewardReceived == 0) {
    lastHarvest = block.timestamp;
    return;
}
```

---

## References

- Vulnerable code: `ContractName.sol` line X (deployed at `0x...`)
- Related prior audit finding (if relevant): [explain why yours is DIFFERENT]
- CWE/weakness class: [e.g., CWE-191: Integer Underflow]
```

---

### TITLE FORMULA

```
[ROOT CAUSE] in [function name] allows [WHO] to [IMPACT]
```

Examples:
- `Missing access control in setPassword() allows anyone to change the stored password`
- `Reentrancy in refund() enables attacker to drain all ETH before state update`
- `Spot price oracle in getPrice() enables flash loan manipulation of exchange rates`
- `_performHarvest() subtracts hardcoded 1 wei causing permanent harvest DoS when Uniswap returns 0`

---

### IMPACT SELECTION GUIDE

Match your finding to one of these Immunefi tiers (program-specific — always verify):

| Impact | Tier | Typical payout range |
|--------|------|---------------------|
| Direct theft of user funds (no limit) | Critical | $50K–$10M |
| Permanent freezing of funds | Critical | $50K–$10M |
| Protocol insolvency | Critical | $50K–$10M |
| Theft of unclaimed yield | High | $10K–$100K |
| Permanent freezing of unclaimed yield | High | $10K–$100K |
| Temporary freezing of funds (>1 hour) | High | $5K–$50K |
| Contract can't operate due to lack of funds | Medium | $2K–$10K |
| Griefing (damage, no profit motive) | Medium | $2K–$10K |
| Contract fails to deliver promised returns | Low | $500–$2K |

---

### PoC REQUIREMENTS

A PoC that wins bounties must:
1. Be a working Foundry test (`forge test -vvv` passes)
2. Fork mainnet at a specific block number
3. Use real deployed contract addresses
4. Show console.log output with actual dollar amounts or token counts
5. Be reproducible by the triager with a single command

A PoC that gets rejected:
- "Test passes" with no meaningful assertion
- Compilation errors
- Wrong mainnet addresses
- No fork — just unit tests with mocks
- No quantification of impact

---

### COMMON REJECTION REASONS

1. **Vague impact:** "Could potentially cause loss of funds" → Always quantify in USD
2. **No comparison evidence:** "This is missing" without showing what sibling function has it
3. **PoC that doesn't run:** Compilation errors, wrong addresses → test before submitting
4. **Wrong severity:** Overclassifying → damages credibility for future reports
5. **Known issue not checked:** Submitting what's already in the audit report → instant reject
6. **No fix provided:** Shows you don't fully understand root cause
7. **Multiple variants of same bug:** Submit ONE report per root cause
8. **Missing preconditions:** Listing an admin action as if it's freely exploitable

---

### WHAT TRIAGERS ACTUALLY WANT TO SEE

From analyzing winning reports across Immunefi competitions:

- **Comparison evidence is the #1 differentiator.** "Function X has guard Y, Function Z doesn't" is more compelling than just saying "Function Z is missing guard Y."
- **Numbers matter more than words.** "$69,300 TVL frozen" > "significant funds at risk."
- **The fix proves understanding.** A 1-line fix that addresses root cause > a 10-line defensive patch.
- **Attack cost matters.** "1 wei USDC + gas" > "substantial capital required."
- **Preconditions must be honest.** Triagers will test the scenario. If you omit that it requires admin action, they will find it and reject.

---

## PART 3: REAL EXAMPLES

20 paid bounty reports dissected — pattern, technique, key insight.

---

### 1. Wormhole — $10M (Uninitialized Proxy)

**Protocol:** Wormhole bridge
**Payout:** $10,000,000
**Bug class:** Upgrade patterns / Access control

**Root cause:** UUPS proxy implementation contract missing `_disableInitializers()` in constructor. Attacker called `initialize()` directly on the implementation, became guardian, upgraded proxy to malicious contract.

**What the hunter did:** Called `implementation()` on the UUPS proxy → got impl address → called `initialize()` directly on impl → became guardian → upgraded proxy.

**Key insight:** `_disableInitializers()` was missing from the impl constructor. Always check the IMPL contract directly, not the proxy.

**Grep to replicate:**
```bash
grep -rn "function initialize\b" contracts/ -A3
grep -rn "_disableInitializers()" contracts/
# If initialize has no protection on implementation → CRITICAL
```

---

### 2. ZeroLend — Existence vs. Ownership Check

**Bug class:** Access control / Logic error

**Root cause:** `split()` called `_requireOwned(tokenId)` which only checks the token exists — not that `msg.sender` owns it. Any caller could split any token.

**What the hunter did:** Read `split()`. Noticed `_requireOwned`. Looked up what it does. Found it only checks existence, not ownership. Called `split(victimTokenId, 1)`.

**Key insight:** `_requireOwned` ≠ `_checkAuthorized`. Always verify what the access control function ACTUALLY validates, not just what its name implies.

**Grep:**
```bash
grep -rn "_requireOwned\|ownerOf\b" contracts/ -B5 -A5
# Read the implementation: does it check msg.sender == owner? Or just: does owner exist?
```

---

### 3. Alchemix — Missing `onlyNewEpoch` on `poke()`

**Bug class:** Missing guard on sibling function

**Root cause:** `vote()` and `reset()` had `onlyNewEpoch(tokenId)` modifier. `poke()` did not. Called `poke()` unlimited times per epoch to drain FLUX tokens.

**What the hunter did:** Listed all functions in the vote/veNFT system. Saw `vote()` and `reset()` had `onlyNewEpoch`. Checked `poke()` — it didn't. Called poke unlimited times per epoch.

**Key insight:** When you see a modifier on 2 out of 3 sibling functions, the 3rd is the bug. This is the "missing guard on sibling function" pattern — one of the most common Critical findings.

**Grep:**
```bash
grep -rn "function vote\|function poke\|function reset" contracts/ -A2
# Compare: do all have the same set of modifiers?
```

---

### 4. Yeet — `startUnstake()` Phantom Rewards

**Bug class:** Accounting desync

**Root cause:** `startUnstake()` decremented `totalSupply` but `balanceOf(this)` didn't change. `harvest()` computed `yieldAmount = balanceOf(this) - totalSupply` — now larger than real. Phantom yield created from the desync.

**What the hunter did:** Traced the flow. `startUnstake()` decrements `totalSupply`. `harvest()` computes yield from the difference. After `startUnstake`, the difference is now artificially inflated.

**Key insight:** Always trace what `balanceOf(this) - totalSupply` equals in each state transition.

**Grep:**
```bash
grep -rn "balanceOf(address(this)).*-.*total\|total.*-.*balanceOf(address(this))" contracts/
# Then: does totalSupply change without balanceOf changing?
```

---

### 5. Folks Finance — Zero-Amount Array Push

**Bug class:** Missing validation before array push

**Root cause:** `increaseCollateral()` called `colPools.push(pool)` BEFORE checking `amount > 0`. Depositing 0 pushed the pool entry. Call 5 times → 5 entries for same pool → `getLoanLiquidity` counted it 5×, inflating collateral.

**What the hunter did:** Read `increaseCollateral()`. Found `colPools.push(pool)` before the amount check. Deposited 0 five times to inflate collateral count.

**Key insight:** Check that array push operations have amount validation BEFORE the push — not after.

**Grep:**
```bash
grep -rn "\.push(" contracts/ -B5
# Is there: require(amount > 0) or if (amount == 0) return; BEFORE the push?
```

---

### 6. VeChain Stargate — `>` vs `>=` Infinite Drain

**Bug class:** Off-by-one / boundary condition

**Root cause:** `if (endPeriod > nextClaimablePeriod)` — the equal case (`==`) fell through to the active rewards branch instead of the completed branch. After exiting, attacker could claim infinite rewards.

**What the hunter did:** Read the delegation period claiming function. Found `>` comparison. Asked "what when equal?" Traced: equal case triggers infinite reward claim loop.

**Key insight:** At EVERY `>` comparison, ask "what when equal?" Boundary conditions are the most common source of off-by-one criticals.

**Grep:**
```bash
grep -rn "endPeriod\|exitPeriod\|lastPeriod" contracts/ | grep "[<>][^=]"
# For every strict comparison on period/epoch boundaries: test the equal case
```

---

### 7. Flare FAssets — Tautology in Proof Verification

**Bug class:** Logic error / Tautology

**Root cause:** `require(sourceAddressesRoot == sourceAddressesRoot)` — comparing a variable to itself. Always true. Non-payment proof verification was bypassed entirely.

**What the hunter did:** Read the non-payment proof validation. Found the tautological comparison. Recognized it as always-true.

**Key insight:** Run a tautology check on every codebase. Any variable compared against itself is a critical bypass.

**Grep:**
```bash
grep -rn "require\|assert" contracts/ | python3 -c "
import sys, re
for l in sys.stdin:
    if re.search(r'\b(\w{4,})\b.*==.*\b\1\b', l):
        print(l.strip())
"
```

---

### 8. Aurora — DelegateCall to Precompile ($6M)

**Bug class:** Non-standard EVM behavior

**Root cause:** On Aurora (custom EVM chain), `delegatecall` to precompile addresses caused balance deduction in the precompile's context — not the caller's. Attacker delegatecalled the precompile: ETH sent to NEAR, but caller's balance unchanged.

**What the hunter did:** On a custom EVM chain, tested `delegatecall` to precompile addresses. Found that balance accounting diverged from mainnet Ethereum behavior.

**Key insight:** On L2s and custom EVMs, test every opcode's behavior — it may differ from mainnet Ethereum. This is especially true for precompiles, gas mechanics, and storage.

**Replicable on:** Any chain with custom precompiles, EVM-Cosmos hybrids, Substrate-based EVMs.

---

### 9. Polygon MRC20 — Missing Balance Check on Gasless Transfer ($2.2M)

**Bug class:** Cryptography / Missing validation

**Root cause:** `transferWithSig()` did not check if `from` had sufficient balance. If `ecrecover` returned `address(0)` (invalid signature), `from = address(0)` and tokens were minted from the void.

**What the hunter did:** Read `transferWithSig()`. Checked: is `from` balance validated? No. Checked: if `ecrecover` returns `address(0)`, does it revert? No. Called with invalid signature → minted from zero address.

**Key insight:** Always test ecrecover with an invalid signature. The return value must be compared against `address(0)` and must revert.

**Grep:**
```bash
grep -rn "ecrecover\|ECDSA\.recover" contracts/ -A5
# Is the return value compared against address(0)?
# Is the from-balance verified before transfer?
```

---

### 10. Evmos — Read the Docs ($150K)

**Bug class:** Configuration / Logic error

**Root cause:** Cosmos SDK documentation specifies that `BlockedAddrs` map must include all module accounts. The module account was not in `BlockedAddrs`. Sending tokens to it corrupted chain state and caused a halt.

**What the hunter did:** Read the Cosmos SDK documentation. Found the requirement. Read `app.go`. Found the module account was missing from `BlockedAddrs`. Demonstrated the chain halt.

**Key insight:** READ THE DOCS. The documentation describes the correct behavior. If the code doesn't match, that's the bug. This is especially true for framework-specific requirements (Cosmos SDK, Anchor, Move runtime).

---

### 11. Plume — safeApprove Without Cleanup

**Bug class:** Token standards / Deprecated pattern

**Root cause:** DEX wrapper used `safeApprove(router, amountIn)` before a partial swap with no cleanup. Second swap failed with "approve from non-zero to non-zero." First amount locked in wrapper permanently.

**What the hunter did:** Read the DEX wrapper. Found `safeApprove`. Asked: "What happens to leftover approval?" No cleanup. Traced: second call reverts, amount locked.

**Key insight:** `safeApprove` is deprecated for a reason — it fails if there's a non-zero existing approval. Must call `safeApprove(spender, 0)` after every swap.

**Grep:**
```bash
grep -rn "safeApprove\b" contracts/ -A8
# Is there: safeApprove(spender, 0) cleanup after the swap?
```

---

### 12. Raydium — `remaining_accounts` Validation ($505K)

**Bug class:** Solana-specific / Missing account validation

**Root cause:** `increase_liquidity.rs` used `remaining_accounts[0]` as `TickArrayBitmapExtension` with no validation that it was actually that account. Passing arbitrary account flipped tick bitmap, draining the pool.

**What the hunter did:** On Solana, read `increase_liquidity.rs`. Found `remaining_accounts[0]` used without validation. Passed arbitrary account to flip tick bitmap.

**Key insight:** On Solana, every `remaining_accounts[n]` must be validated with ownership check, discriminator check, or constraint attribute.

**Grep (Solana):**
```bash
grep -rn "remaining_accounts\[" src/ --include="*.rs" -A5
# Is there: AccountInfo constraint, owner check, discriminator check?
```

---

### 13. Shardeum — Duplicate Validator Signatures

**Bug class:** Cryptography / Missing deduplication

**Root cause:** `validSignatures++` incremented without deduplication. One malicious validator stuffed its own signature 100× → reached 66% threshold alone, bypassing consensus.

**What the hunter did:** Read the consensus code. Found `validSignatures++` with no deduplication check. Demonstrated one validator reaching threshold by repeating its signature.

**Key insight:** Any counter that increases per-signature must check for duplicate signers. `if (seen.has(signer)) continue; seen.add(signer)` is the fix pattern.

**Grep:**
```bash
grep -rn "validSignatures++\|signatureCount++" src/ -B5
# Is there: if (seen.has(signer)) continue; seen.add(signer)?
```

---

### 14. DFX Finance — 2-Decimal Token Rounding ($100K)

**Bug class:** Arithmetic / Precision loss

**Root cause:** Protocol supported EURS token (2 decimals). Deposit of 1 wei EURS: `viewRawAmount(1)` → division result rounds to 0 → deposit 0 underlying, receive non-zero LP shares.

**What the hunter did:** Noted the protocol supported EURS (2 decimals). Ran the calculation manually: 1 wei → 0 underlying after rounding → free LP shares.

**Key insight:** For any non-standard decimal token (2, 4, 6 decimals), test edge cases near 0. Division truncates toward zero, which creates deposit-with-0-cost attacks.

**Grep:**
```bash
grep -rn "\.decimals()\|EURS\|2.*decimal\|decimals.*2\b" contracts/
# For any non-standard decimal token: test edge cases near 0
```

---

### 15. Alchemix V3 — Fast Path Skips State Update

**Bug class:** Incomplete path / Fast path skip

**Root cause:** `claimRedemption()` had a fast path: if Transmuter already had funds, it transferred and burned NFT, then returned early. The slow path updated `cumulativeEarmarked`, `_redemptionWeight`, `totalDebt`. Fast path skipped all 3. Phantom debt + stranded collateral.

**What the hunter did:** Read `claimRedemption()`. Found `if (transmuter has funds) { transfer; burn; return; }`. Traced which state updates the slow path does that the fast path skips.

**Key insight:** For every early `return` or fast path: which state updates happen in normal flow but NOT here? The delta is the bug. This is the most common Critical pattern across Immunefi competition reports.

**Grep:**
```bash
grep -rn "if.*sufficient\|fast.*path\|return\b" contracts/ -B3 -A10
# For each early return: which state updates happen in normal flow but NOT here?
```

---

### 16. Belt Finance — Logic Error in Yield Aggregator ($1.05M)

**Bug class:** Oracle manipulation / Flash loan

**Root cause:** Vault's price per full share calculation included a temporary value before it was settled. Flash loan inflated the transient value → manipulated ppfs → borrow against inflated collateral.

**What the hunter did:** Read the vault's `pricePerFullShare` calculation. Found it included a value that could be temporarily inflated. Flash loaned to inflate it, then borrowed against the inflated collateral.

**Key insight:** Any vault with `pricePerFullShare` or `exchangeRate` that is readable AND writable in the same transaction is a flash loan oracle target. Check: can a single transaction inflate then read the rate?

---

### 17. Belong — ERC4626 First Depositor

**Bug class:** Arithmetic / First depositor inflation

**Root cause:** `convertToShares` had no virtual offset. First depositor could inflate exchange rate: deposit 1 wei → donate 999,999 → next depositor gets 0 shares for 999,999 deposit.

**What the hunter did:** Read `convertToShares`. No `totalSupply() + 10**decimalsOffset()` virtual offset. Executed the classic first depositor inflation: deposit 1 → donate → victim gets 0.

**Key insight:** No virtual offset in ERC4626 = first depositor inflation possible. Fix: OpenZeppelin's implementation adds `totalSupply() + 10**_decimalsOffset()` to numerator.

**Grep:**
```bash
grep -rn "convertToShares\|_convertToShares" contracts/ -A5
# Is there: totalSupply() + 10**decimalsOffset() or totalAssets() + 1?
```

---

### 18. Paradex — Negative Value in Account Transfer

**Bug class:** Type system / Non-EVM chain specifics

**Root cause:** On Starknet (Cairo), `account_transfer_partial()` took `felt252` input (which can be negative). Validation `amount >= min_amount` passed even for negative values. `balance - (-X) = balance + X` → infinite balance.

**What the hunter did:** On Starknet, read `account_transfer_partial()`. Input type is `felt252`. Tested: does validation pass for negative felt252? Yes. `balance - (-X) = balance + X`.

**Key insight:** On Cairo/Starknet, `felt252` can represent negative values. Any amount validation must check `amount > 0` explicitly, not just `amount >= minimum`.

---

### 19. Anvil Protocol — uint256 → uint16 Truncation

**Bug class:** Arithmetic / Type truncation

**Root cause:** `uint16((bigValue * 10_000) / collateral)` — result cast to uint16 without range check. Value 65,537 truncates to 1. Collateral factor validation passed. Deposited $0.003, issued $10,000 LOC.

**What the hunter did:** Found `uint16(...)` cast in collateral factor calculation. Calculated: what input produces a value just above 65,535? That value truncates to 1. Passed that input.

**Key insight:** Any downcast (uint256 → uint16, uint128 → uint64) without a range check is a critical candidate if the result is used for security validation.

**Grep:**
```bash
grep -rn "uint16(\|uint8(\|as u16\|as u8" contracts/ src/
# Is there a range check before the downcast?
```

---

### 20. ResupplyFi — Near-Empty Vault Manipulation ($1.8M)

**Bug class:** Arithmetic / Exchange rate manipulation

**Root cause:** Protocol used virtual shares but with too-small virtual offset. Near-empty vault (1 existing share) still allowed exchange rate manipulation when total assets were very low.

**What the hunter did:** Found that virtual shares were present but the offset was small enough that with 1 existing share and very low TVL, the same inflation math still applied.

**Key insight:** Even WITH virtual shares, very low TVL vaults can still be vulnerable if the virtual offset is too small relative to the token's price. Test at TVL = 1 share.

---

### THE 3 UNIVERSAL PATTERNS (From All 20 Examples)

Almost every bug comes from one of three root causes:

**Pattern A: "I assumed function B was called, but it wasn't"**
- Fast path skip, early return, conditional execution
- The fix: ensure ALL paths update ALL state variables
- Examples: #15 (Alchemix V3 fast path), #4 (Yeet accounting desync)

**Pattern B: "I assumed the check meant X, but it actually means Y"**
- `_requireOwned` = existence not ownership
- `>` = doesn't include boundary
- Modifier = silent bypass when missing
- Examples: #2 (ZeroLend), #6 (VeChain), #3 (Alchemix poke)

**Pattern C: "I assumed this can't happen, but it can"**
- "ecrecover can't return address(0)" → it can
- "negative amounts can't be passed" → they can (felt252)
- "this function won't be called twice" → it will (no onlyNewEpoch)
- Examples: #9 (Polygon MRC20), #18 (Paradex), #3 (Alchemix)

---

→ NEXT: [06-methodology-research.md](06-methodology-research.md)
