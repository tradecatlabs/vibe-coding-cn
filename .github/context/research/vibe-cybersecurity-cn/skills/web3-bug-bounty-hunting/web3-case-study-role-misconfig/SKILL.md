---
name: web3-case-study-role-misconfig
description: Case study - role misconfiguration bug class applied to a yield aggregator protocol. Use as a template for applying all 10 bug classes to a single target.
Contains: architecture walkthrough, all bug class verdicts, 2 findings (DISTRIBUTOR_ROLE never granted, dust harvest DoS), complete PoC templates, report drafts, validation steps.
---

# CASE STUDY: ROLE MISCONFIGURATION IN A YIELD AGGREGATOR
> Bug Class: Access Control | Severity: Critical/Medium | Payout Range: $10K–$50K
> This file shows how to apply the full 10-class methodology to a real yield aggregator target.

---

## TARGET PROFILE (Anonymized)

| Field | Value |
|-------|-------|
| Protocol Type | Yield aggregator — stablecoin → lending protocol → harvest → DEX → reward token |
| Max Bounty | $50K (Critical) |
| TVL | Low (fresh program, under $100K) |
| Core Contracts | Vault.sol, RewardsDistributor.sol |
| Program Age | ~5 days when hunted (fresh = low competition) |
| Prior Audits | Firm A (16 findings, all Risk Accepted) + Firm B (18 findings, all Risk Accepted) |

**Scorecard:** Max bounty (+2) + custom math (+1) + recent code (+1) + known prior audits (+1) + public source (+1) + program new (+2) = **8/10 → HUNT**

**Why this scores high:** Fresh program on a live bounty platform + prior audits that accepted all risk = team is aware of issues but hasn't patched them. Hunt for what auditors missed or flagged but accepted.

---

## ARCHITECTURE + FUND FLOW

```
User deposits Stablecoin
    ↓ deposit(uint256 amount)
Vault.sol stores:
  - deposits[user] += amount
  - totalDeposited += amount
  - depositTimestamp[user] = block.timestamp
    ↓ safeTransferFrom(user, address(this), amount)
    ↓ lendingProtocol.supply(stablecoin, amount, address(this), 0)
  Interest-bearing token accrues in Vault.sol balance
    ↓ (periodic) _performHarvest()
  aToken balance > totalDeposited + DUST_THRESHOLD
    ↓ lendingProtocol.withdraw(stablecoin, harvestAmount - 1, address(this))
    ↓ dex.exactInputSingle(stablecoin → rewardToken)
    ↓ RewardsDistributor.distribute(rewardToken, amount)
  RewardsDistributor tracks:
  - cumulativeRewardPerShare updates
  - users can call claimFor(user) to collect rewardToken

User withdraws:
    ↓ withdraw(uint256 amount)
  if block.timestamp < depositTimestamp[user] + LOCK_PERIOD:
    withdrawFee applies (e.g. 0.5%)
  lendingProtocol.withdraw(stablecoin, amount, user)
```

**Key state variables:**
- `deposits[user]` — user principal (stablecoin)
- `totalDeposited` — sum of all principals
- `depositTimestamp[user]` — last deposit time (affects withdrawal fee)
- `cumulativeRewardPerShare` — reward index in RewardsDistributor
- `lastClaimedReward[user]` — user's last reward index

---

## KNOWN ISSUES (Risk Accepted by Team — Do NOT Submit)

### Firm A Findings (16 total, all Risk Accepted)
All standard: missing events, gas optimizations, reentrancy guards present (CEI followed), centralization risks (owner can pause), single oracle (DEX swap is operational, not security-critical).

### Firm B Findings (18 total, all Risk Accepted)
Including:
- HAL-01: withdrawFee can be changed by owner (centralization)
- HAL-05: deposit() resets depositTimestamp even on partial top-ups → **extends lock period for existing deposits**
- HAL-08: Missing check for DISTRIBUTOR_ROLE being set *(flagged but did NOT verify it was never granted)*
- Various gas and event issues

**Pattern:** Firm B flagged "missing check" but didn't verify the role was actually ungranted. This is the gap to exploit.

---

## BUG CLASS VERDICTS

### 1. Accounting Desync — 2 FINDINGS

**Finding 1: The `-1` Stranding Pattern**
```solidity
// In _performHarvest():
harvestAmount = aToken.balanceOf(address(this)) - totalDeposited - 1; // strands 1 wei
```
The hardcoded `-1` strands 1 wei of stablecoin per harvest permanently. Over thousands of harvests, this accumulates. Severity: LOW/INFORMATIONAL (no user loss, just protocol dust accumulation).

**Finding 2: Dust Harvest DoS** ← VALID MEDIUM
```
Scenario: Accumulated harvest amount is very tiny (< DEX minimum swap)
1. harvest() calls dex.exactInputSingle(stablecoin → rewardToken)
2. DEX returns 0 (amount too small to produce any output)
3. RewardsDistributor.distribute(0) is called
4. If distribute() reverts on 0 amount → harvest is permanently frozen
5. Users can still withdraw principal but all future yield is lost

Verification: Check if distribute(0) reverts. Check DEX minimum swap threshold.
```

### 2. Access Control — 1 FINDING (CRITICAL/HIGH)
**Finding: DISTRIBUTOR_ROLE Never Granted** ← MAIN FINDING

```solidity
// RewardsDistributor.sol
bytes32 public constant DISTRIBUTOR_ROLE = keccak256("DISTRIBUTOR_ROLE");

function claimFor(address user) external {
    require(hasRole(DISTRIBUTOR_ROLE, msg.sender), "Not distributor");
    // ... distribute rewardToken to user
}
```

**Problem:** `DISTRIBUTOR_ROLE` is defined but NEVER granted in the constructor or any initialization function. No address holds this role. `claimFor()` can never succeed — all reward tokens are permanently locked.

**How Firm B missed it:** They flagged "missing check for whether role is set" — but their fix recommendation was "add a require that checks the role exists." They didn't verify that `getRoleMemberCount(DISTRIBUTOR_ROLE) == 0` on the live deployment.

**Severity Assessment:**
- If harvest HAS already happened: CRITICAL (funds locked forever)
- If harvest never happened yet: HIGH (permanent lock when it does happen)
- Impact × Likelihood × Exploitability: 3 × 3 × 3 = 27 → CRITICAL

**Verification commands:**
```bash
# Check if any address has DISTRIBUTOR_ROLE (replace with actual address)
cast call <REWARDS_DISTRIBUTOR_ADDR> \
  "getRoleMemberCount(bytes32)(uint256)" \
  "$(cast keccak 'DISTRIBUTOR_ROLE')"
# Expected: 0 = confirmed bug

# Alternative: Etherscan → Events → filter "RoleGranted"
# If no RoleGranted events with DISTRIBUTOR_ROLE hash = confirmed
```

### 3. Incomplete Path — Known (Risk Accepted)
Firm B HAL-05: `deposit()` resets `depositTimestamp[user]` even on partial top-ups, extending the lock period for all existing deposits. Risk Accepted by team.

### 4. Off-by-One — CLEAN
All boundary operators (`>=`, `<`) in Vault.sol and RewardsDistributor.sol are correct.

### 5. Oracle Price — CLEAN
Protocol does NOT use price oracles for security decisions (no lending, no liquidation, no collateral). The DEX swap is operational (converting yield), not security-critical. MEV/sandwich risk exists but is a griefing/efficiency issue, not a theft vulnerability.

### 6. ERC4626 Vaults — NOT APPLICABLE
Uses a custom 1:1 share model, NOT ERC4626:
- `deposits[user]` tracks exact principal
- No share price, no share-based rounding
- Transfers between users are blocked
- First depositor inflation attack does NOT apply

### 7. Reentrancy — CLEAN
Follows CEI (Checks-Effects-Interactions) correctly:
- `deposits[user] += amount` BEFORE `lendingProtocol.supply()`
- `deposits[user] -= amount` BEFORE `lendingProtocol.withdraw()`
- Missing `nonReentrant` guard, but CEI makes it safe. Not submittable without PoC.

### 8. Flash Loan — CLEAN (Economically)
Flash loan attack would attempt: deposit → dilute harvest → withdraw to steal yield.
The `withdrawFee` makes this unprofitable:
- Attacker deposits $1M → harvest dilutes → attacker gains $0 extra yield
- But: attacker pays withdrawal fee to exit
- Net: negative expected value → NOT PROFITABLE

### 9. Signature Replay — NOT APPLICABLE
No signature-based functions, no EIP-2612 permit, no meta-transactions.

### 10. Proxy/Upgrade — NOT APPLICABLE
Not upgradeable proxies. No proxy pattern.

---

## WHAT TO SUBMIT

### SUBMIT (2 findings):

**Finding 1 — CRITICAL/HIGH:**
```
Title: DISTRIBUTOR_ROLE never granted in RewardsDistributor.sol,
       permanently locking all reward tokens

Root Cause: DISTRIBUTOR_ROLE is defined but grantRole() is never called
            in constructor or initialization. No address holds this role.

Impact: All rewards distributed by harvest() are permanently locked —
        claimFor() always reverts.
        Users receive zero yield despite depositing and paying withdrawFee.

Attack Path: Not an attack — passive failure. Any harvest → rewards locked forever.

Severity: Critical (if harvest has occurred) / High (if not yet)
```

**Finding 2 — MEDIUM:**
```
Title: _performHarvest() dust harvest causes permanent DoS on yield distribution

Root Cause: When accumulated yield rounds to < DEX minimum swap amount,
            exactInputSingle() returns 0 output. distribute(0) may revert or
            permanently advance the reward index with no rewards.

Impact: After a dust harvest, all subsequent harvests may fail permanently.

Severity: Medium (requires specific conditions but permanently impacts yield)
```

### DO NOT SUBMIT:
- The `-1` stranding (informational, design choice)
- depositTimestamp reset (Risk Accepted by team)
- Missing nonReentrant (CEI is followed; no PoC = no submission)
- Owner centralization (excluded by design in Immunefi SC programs)
- Any of the already-acknowledged findings from prior audits

---

## COMPLETE POC TEMPLATE: ROLE NEVER GRANTED

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import "forge-std/console.sol";

interface IRewardsDistributor {
    function DISTRIBUTOR_ROLE() external view returns (bytes32);
    function hasRole(bytes32 role, address account) external view returns (bool);
    function getRoleMemberCount(bytes32 role) external view returns (uint256);
    function claimFor(address user) external;
}

contract RoleNeverGrantedTest is Test {
    // Replace with actual deployed address from target
    address constant REWARDS_DISTRIBUTOR = address(0xYOUR_TARGET_ADDRESS);

    IRewardsDistributor distributor;

    function setUp() public {
        // Fork at current block
        vm.createSelectFork(vm.envString("MAINNET_RPC_URL"));
        distributor = IRewardsDistributor(REWARDS_DISTRIBUTOR);
    }

    function testDistributorRoleNeverGranted() public {
        bytes32 DISTRIBUTOR_ROLE = distributor.DISTRIBUTOR_ROLE();

        uint256 memberCount = distributor.getRoleMemberCount(DISTRIBUTOR_ROLE);
        console.log("Addresses with DISTRIBUTOR_ROLE:", memberCount);

        // Should be 0 — proving no one can call claimFor()
        assertEq(memberCount, 0, "DISTRIBUTOR_ROLE has 0 members (confirmed bug)");

        // Verify claimFor() reverts for any user
        address testUser = address(0x1234);
        vm.expectRevert(); // "AccessControl: account does not have role"
        distributor.claimFor(testUser);

        console.log("CONFIRMED: claimFor() reverts for all users.");
        console.log("All rewards permanently locked.");
    }
}
```

**Run:**
```bash
forge test --match-test testDistributorRoleNeverGranted -vvvv \
  --fork-url $MAINNET_RPC_URL
```

**Expected output:**
```
Addresses with DISTRIBUTOR_ROLE: 0
CONFIRMED: claimFor() reverts for all users.
All rewards permanently locked.

[PASS] testDistributorRoleNeverGranted()
```

---

## REPORT TEMPLATE

**Title:** Missing DISTRIBUTOR_ROLE grant permanently locks all rewards for all users

**Bug Description:**
`RewardsDistributor.sol` defines `DISTRIBUTOR_ROLE` and requires it to call `claimFor()`. However, `grantRole(DISTRIBUTOR_ROLE, ...)` is never called in the constructor, any initialization function, or any privileged setter. No address holds this role. `claimFor()` always reverts.

The Vault contract calls `RewardsDistributor.distribute()` after each harvest, successfully depositing reward tokens into the distributor. However, these tokens can never be claimed — permanently locked.

**Root Cause:** Constructor is missing `grantRole(DISTRIBUTOR_ROLE, vaultContract)`.

**Impact:** All yield earned by all depositors is permanently locked in RewardsDistributor.sol. Users cannot receive any return from their deposits.

*Impact category:* **Permanent freezing of funds**

**Proof of Concept:** [Run PoC above against deployed contract]

**Remediation:** Add `grantRole(DISTRIBUTOR_ROLE, address(vault))` in RewardsDistributor constructor, OR add a `setDistributor(address)` function callable only by admin.

---

## VALIDATION CHECKLIST (7-Question Gate)

| Question | DISTRIBUTOR_ROLE | Dust Harvest DoS |
|----------|-----------------|-----------------|
| Can attacker use it NOW? | Yes (passive — already locked) | Yes (needs small harvest) |
| Impact in program's list? | Permanent freezing of funds ✓ | Temporary/permanent DoS ✓ |
| In-scope contract? | RewardsDistributor.sol ✓ | Vault.sol ✓ |
| Requires admin access? | No — passive ✓ | No — anyone can trigger ✓ |
| Already known/acknowledged? | No ✓ | No ✓ |
| Economically viable? | Yes — passive lock ✓ | Yes — dust accumulates ✓ |
| Already public? | No ✓ | No ✓ |
| **VERDICT** | **SUBMIT** | **SUBMIT** |

---

## LESSONS: WHAT TO LOOK FOR ON SIMILAR TARGETS

This pattern (role defined, never granted) appears frequently in:

1. **Any contract using OpenZeppelin AccessControl** — check every `bytes32 public constant *_ROLE` — verify each one has a corresponding `grantRole()` call in constructor
2. **Distributor/reward contracts** — these are often deployed separately and the grant is "supposed to happen" during deployment setup
3. **Contracts with multiple initialization steps** — if setup requires calling multiple functions in sequence, the grant is often missed

**Grep to find candidates:**
```bash
# Find all role definitions
grep -r "bytes32 public constant.*ROLE" ./src/

# Verify each role has a grantRole call
grep -r "grantRole" ./src/

# If roles > grantRole calls → investigate each missing grant
```

**Protocols to check for this pattern:** Any protocol where `RewardsDistributor`, `FeeDistributor`, `YieldDistributor`, or `Distributor` is a separate contract from the main vault.

---

→ NEXT: [08-ai-tools.md](08-ai-tools.md)
