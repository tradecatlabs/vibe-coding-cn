---
name: web3-grep-arsenal
description: Master grep command arsenal for Web3 smart contract auditing. Use when starting a new protocol scan, before deep code review, or when hunting specific vulnerability classes.
Contains: 10 grep blocks for all major vuln classes, tier ranking, protocol-specific patterns, 2025 new patterns, copy-paste ready blocks.
---

# GREP ARSENAL — MASTER REFERENCE
> All grep commands in one place. Run in the first 30 minutes of any new target.
> Replaces: 03-grep-surface-map, 14-grep-master-patterns + grep sections from 04-13

---

## HOW TO USE THE SURFACE MAP

**Process:**
1. Run ALL 10 blocks below (takes ~5 min)
2. Collect all results in a notes file
3. Tier-rank the hits (see Tier System below)
4. In pass 1: READ everything, DON'T investigate yet
5. In pass 2: Deep-dive on Tier 1 + 2 items

**Tier System:**
- **Tier 1** — Near privileged code, external calls, or state changes with no guards → Investigate first
- **Tier 2** — Interesting patterns that need context before judging → Investigate after Tier 1
- **Tier 3** — Informational only (documentation, test files, comments) → Skip unless Tier 1+2 exhausted

---

## THE 10 GREP BLOCKS (Copy-Paste Each)

### Block 1 — Access Control

```bash
echo "=== ACCESS CONTROL ===" && \
grep -rn "tx\.origin" src/ --include="*.sol" && \
grep -rn "msg\.sender == owner\b" src/ --include="*.sol" && \
grep -rn "modifier only" src/ --include="*.sol" -A5 && \
grep -rn "onlyOwner\|onlyAdmin\|onlyRole" src/ --include="*.sol" | wc -l && \
grep -rn "def admin_\|router\..*admin\|function.*[Aa]dmin" src/ --include="*.sol"
```

**Red flags:**
- `tx.origin` used for auth → Tier 1 (phishing vector)
- Modifier uses `if (condition) { _; }` without else → Tier 1 (silent bypass — function still executes for unauthorized callers)
- `onlyOwner` count << total external function count → likely missing guards on siblings

### Block 2 — Reentrancy

```bash
echo "=== REENTRANCY ===" && \
grep -rn "\.call{value\|\.call(" src/ --include="*.sol" && \
grep -rn "\.transfer(\|\.send(" src/ --include="*.sol" && \
grep -rn "safeTransfer\|safeTransferFrom" src/ --include="*.sol" && \
grep -rn "onERC721Received\|onERC1155Received\|tokensReceived" src/ --include="*.sol" && \
grep -rn "nonReentrant\|ReentrancyGuard" src/ --include="*.sol"
```

**Red flags:**
- `.call{value:}` or `safeTransfer` BEFORE state updates in same function → Tier 1 (CEI violation)
- `onERC721Received`/`onERC1155Received` hooks present → check for reentrancy path
- External calls present but `nonReentrant` missing → verify CEI is followed

### Block 3 — Oracle / Price

```bash
echo "=== ORACLE / PRICE ===" && \
grep -rn "slot0\b" src/ --include="*.sol" && \
grep -rn "getReserves()" src/ --include="*.sol" && \
grep -rn "latestRoundData\|latestAnswer" src/ --include="*.sol" && \
grep -rn "updatedAt" src/ --include="*.sol" && \
grep -rn "block\.timestamp" src/ --include="*.sol" | grep -v "//\|test\|Test" | head -20
```

**Red flags:**
- `slot0()` used for price → Tier 1 (Uniswap V3 spot, flash-loan manipulable)
- `getReserves()` used for price → Tier 1 (Uniswap V2 spot, flash-loan manipulable)
- `latestRoundData` without `updatedAt` check → Tier 1 (stale Chainlink price)
- `latestAnswer` → Tier 1 (deprecated, no round validation)

### Block 4 — Arithmetic / Math

```bash
echo "=== ARITHMETIC ===" && \
grep -rn "unchecked {" src/ --include="*.sol" && \
grep -rn "/ \|/=" src/ --include="*.sol" | grep -v "//\|test\|Test" | head -30 && \
grep -rn "mulDiv\|FullMath\|PRBMath" src/ --include="*.sol" && \
grep -rn "\* 10\*\*\|* 1e18\|* WAD\|* RAY" src/ --include="*.sol"
```

**Red flags:**
- `unchecked {}` blocks → manually verify each (Solidity 0.8+ unwraps here)
- Division before multiplication (`a / b * c`) → precision loss
- `/ 1e18` in contract that handles 6-decimal tokens → decimal mismatch

### Block 5 — Input Validation

```bash
echo "=== INPUT VALIDATION ===" && \
grep -rn "address(0)\b" src/ --include="*.sol" && \
grep -rn "require.*length\|\.length ==" src/ --include="*.sol" && \
grep -rn "delegatecall" src/ --include="*.sol" && \
grep -rn "abi\.decode\|abi\.encodePacked" src/ --include="*.sol" | head -20
```

**Red flags:**
- `delegatecall` with user-controlled target → Tier 1 (arbitrary code execution)
- `abi.decode` on user-supplied calldata without length validation → Tier 1
- Array params in batch functions without dedup check → Tier 1 (double-count attack)

### Block 6 — Token Handling

```bash
echo "=== TOKEN HANDLING ===" && \
grep -rn "IERC20\.\|ERC20\." src/ --include="*.sol" | grep "transfer\b\|transferFrom\b" && \
grep -rn "SafeERC20\|safeTransfer\b" src/ --include="*.sol" | head -10 && \
grep -rn "balanceOf(address(this))" src/ --include="*.sol" && \
grep -rn "permit(" src/ --include="*.sol" | grep -v "//\|IERC20Permit" && \
grep -rn "try.*permit\|catch.*permit" src/ --include="*.sol"
```

**Red flags:**
- `token.transfer()` without `SafeERC20.safeTransfer()` → Tier 1 (return value unchecked, fails silently on old USDT)
- `balanceOf(address(this))` for pricing/shares → Tier 1 (donation attack vector)
- `permit()` without try/catch wrapper → Tier 2 (frontrun DoS possible)

### Block 7 — ERC4626 / Vault

```bash
echo "=== ERC4626 / VAULT ===" && \
grep -rn "totalAssets\|convertToShares\|previewDeposit\|previewMint" src/ --include="*.sol" && \
grep -rn "_decimalsOffset\|decimalsOffset\|virtual_shares\|dead.*shares" src/ --include="*.sol" && \
grep -rn "shares.*supply\|totalSupply\|mint.*shares" src/ --include="*.sol" | head -20
```

**Red flags:**
- ERC4626 present but `_decimalsOffset()` NOT present → Tier 1 (first depositor inflation)
- `totalAssets()` uses `balanceOf(address(this))` → Tier 1 (donation attack)
- `mint()` or `deposit()` called without same validation path → Tier 1 (MetaPool bug: mint skipped receipt check)

### Block 8 — Proxy / Upgradeable

```bash
echo "=== PROXY / UPGRADE ===" && \
grep -rn "_authorizeUpgrade\|upgradeTo\|upgradeToAndCall" src/ --include="*.sol" && \
grep -rn "initialize(" src/ --include="*.sol" | grep -v "//\|test\|Test" && \
grep -rn "_disableInitializers\|initializer\b\|Initializable" src/ --include="*.sol" && \
grep -rn "StorageSlot\|ERC1967\|TransparentProxy\|UUPSUpgradeable" src/ --include="*.sol"
```

**Red flags:**
- `_authorizeUpgrade()` without `onlyOwner` or role check → Tier 1 (anyone can upgrade)
- `initialize()` without `initializer` modifier → Tier 1 (re-initialization possible)
- Proxy present but `_disableInitializers()` NOT in impl constructor → Tier 1 (impl attackable)

### Block 9 — Signature / Replay

```bash
echo "=== SIGNATURES ===" && \
grep -rn "ecrecover\|ECDSA\.recover" src/ --include="*.sol" && \
grep -rn "chainId\|block\.chainid\|DOMAIN_SEPARATOR" src/ --include="*.sol" && \
grep -rn "nonces\[" src/ --include="*.sol" && \
grep -rn "keccak256.*abi\.encode" src/ --include="*.sol" | head -20
```

**Red flags:**
- `ecrecover` present but `chainId`/`DOMAIN_SEPARATOR` NOT present → Tier 1 (cross-chain replay)
- `ecrecover` without nonce → Tier 1 (same-chain replay)
- `ecrecover` return not checked against `address(0)` → Tier 1 (invalid sigs succeed)

### Block 10 — State Completeness / Access

```bash
echo "=== STATE COMPLETENESS ===" && \
grep -rn "grantRole\|revokeRole\|hasRole" src/ --include="*.sol" && \
grep -rn "bytes32.*ROLE\s*=" src/ --include="*.sol" && \
grep -rn "function.*migrate\|function.*batch.*stake\|function.*multiStake" src/ --include="*.sol" -A10 && \
grep -rn "} catch" src/ --include="*.sol" -A5 | grep -A5 "revert\|Error" && \
grep -rn "cached\|_cache\|lastKnown\|storedBalance" src/ --include="*.sol"
```

**Red flags:**
- Role defined but `grantRole()` call for that role NOT found anywhere → Tier 1 (role permanently empty)
- Array-based function: `flag = true` OUTSIDE/AFTER loop → Tier 1 (empty array bypass)
- `} catch { revert }` on critical path → Tier 2 (liveness DoS if external changes)
- Cache variable initialized to 0 with no first-access guard → Tier 1 (uninitialized cache)

---

## PROTOCOL-SPECIFIC PATTERNS

### Yield Aggregator (like Ern, Yearn, Beefy)
```bash
grep -rn "cumulativeReward\|rewardPerShare\|accRewardPerShare" src/ --include="*.sol"
grep -rn "harvestCooldown\|canHarvest\|performHarvest\|_harvest" src/ --include="*.sol"
grep -rn "totalDeposited\|totalPrincipal" src/ --include="*.sol"
# Check: does cumulativeReward always update before user checkpoint?
```

### Lending Protocol (like Aave, Compound)
```bash
grep -rn "collateral\|borrow\|liquidat" src/ --include="*.sol"
grep -rn "healthFactor\|isSolvent\|isLiquidatable" src/ --include="*.sol"
grep -rn "interest.*accrual\|accrueInterest\|indexIncrease" src/ --include="*.sol"
grep -rn "amplification\|A_PARAMETER\|getA()" src/ --include="*.sol"
# Check: is price oracle manipulation possible? Is interest accrual order correct?
```

### AMM / DEX
```bash
grep -rn "getReserves\|reserve0\|reserve1" src/ --include="*.sol"
grep -rn "slot0\|sqrtPriceX96\|tick\b" src/ --include="*.sol"
grep -rn "K\s*=\|invariant\|_invariant" src/ --include="*.sol"
grep -rn "amountOutMin\|minAmountOut\|deadline" src/ --include="*.sol"
# Check: is spot price used for any security decision? Missing slippage?
```

### Staking / Restaking
```bash
grep -rn "epoch\|currentEpoch\|lastEpoch\|epochId" src/ --include="*.sol"
grep -rn "unstake\|migrate\|slash\|jailValidator" src/ --include="*.sol"
grep -rn "validatorIds\|stakeIds\|delegateIds" src/ --include="*.sol"
# Check: can same ID be passed twice? Empty array skips state reset?
```

### ZK / Proof Contracts
```bash
grep -rn "verifyProof\|IVerifier\|publicInputs\b" src/ --include="*.sol"
grep -rn "return true" src/ --include="*.sol" | grep -i "verify\|proof"
grep -rn "require.*inputs\[0\]\|rangeCheck\|MAX_BALANCE" src/ --include="*.sol"
# Check: are public inputs range-checked after proof verification?
```

---

## 2025 NEW PATTERN SCANS

```bash
# ERC4626 near-empty vault (inflation variant, now widespread)
grep -rn "totalAssets\b" src/ --include="*.sol" -A10 | grep "balanceOf\|balance()"
# If totalAssets() uses raw balanceOf → donation attack risk

# EIP-2612 permit frontrun DoS
grep -rn "permitAndDeposit\|permitAndStake\|permitAndBorrow" src/ --include="*.sol"
grep -rn "try.*permit\|catch.*permit" src/ --include="*.sol"
# Missing try/catch around permit = DoS possible

# Decimal precision mismatch (6 vs 18 decimals)
grep -rn "/ 1e18\|/ WAD" src/ --include="*.sol"
grep -rn "decimals()\|IERC20Metadata" src/ --include="*.sol"
# / 1e18 WITHOUT decimals() call in same function = decimal mismatch candidate

# Uninitialized cache
grep -rn "uint256.*cached\|uint128.*cached\|int256.*cached" src/ --include="*.sol"
# Cache initialized to 0 with no first-access sync = uninitialized cache bug

# Empty array bypass
grep -rn "= true;" src/ --include="*.sol" -B15 | grep -B15 "for.*calldata"
# flag = true AFTER a loop that can be empty = bypass critical

# Streaming/continuous precision (per-second rewards)
grep -rn "rewardPerSecond\|ratePerSecond\|flowRate\|perSecond" src/ --include="*.sol"
grep -rn "uint128.*reward\|uint96.*rate" src/ --include="*.sol"
# uint128 accumulator × per-second rate = overflow risk on long time periods

# Withdrawal queue multi-field invariant
grep -rn "\.queued\b\|\.claimable\b\|\.claimed\b" src/ --include="*.sol"
# claimed <= claimable <= queued must hold — check all update paths

# Cross-chain signature reuse
grep -rn "keccak256.*abi\.encodePacked\|ECDSA\.recover" src/ --include="*.sol"
grep -rn "chainId\|block\.chainid" src/ --include="*.sol"
# ecrecover WITHOUT chainId = same sig valid on all chains

# try/catch DoS liveness
grep -rn "} catch" src/ --include="*.sol" -A5 | grep -B1 "revert\|IncompatibleAdapter"

# Nullifier timing (Worldcoin-style)
grep -rn "nullifiers\[.*\] = true\|nullifierUsed\[" src/ --include="*.sol" -B5
# Marked before action = frontrun can permanently DoS identity
```

---

## SPECIFIC BUG PATTERN SEARCHES

### Silent Modifier (if vs require)
```bash
# Find modifiers that use if() without revert — silently does nothing for unauthorized callers
grep -rn "modifier only" src/ --include="*.sol" -A10 | grep -A10 "if ("
# Correct: require(condition, "msg"); _;
# BUG: if (condition) { _; }  ← no else = still executes for unauthorized
```

### Tautology Check (variable compared to itself)
```bash
grep -rn "require(" src/ --include="*.sol" | grep "\b\(\w\+\) == \1\b"
# e.g. require(a == a, ...) = always true → always passes
```

### Same-Role Count Mismatch
```bash
grep -rn "onlyRole\b" src/ --include="*.sol" | wc -l
grep -rn "grantRole(" src/ --include="*.sol" | wc -l
# More onlyRole uses than grantRole calls = some roles may never be granted
```

### Accounting: Balance vs Tracked
```bash
grep -rn "balanceOf(address(this))" src/ --include="*.sol"
grep -rn "totalDeposited\|totalPrincipal\|_balance\b" src/ --include="*.sol"
# If protocol uses raw balanceOf for pricing AND has separate totalDeposited
# → donation attack: send tokens directly to contract → inflates balance
```

---

→ NEXT: [04-poc-and-foundry.md](04-poc-and-foundry.md)
