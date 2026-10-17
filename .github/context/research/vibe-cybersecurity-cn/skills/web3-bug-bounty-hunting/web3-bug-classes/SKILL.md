---
name: web3-bug-classes
description: Complete reference for all 10 DeFi smart contract bug classes. Use this when hunting for specific vulnerability types, need attack patterns for accounting desync, access control, incomplete path, off-by-one, oracle manipulation, ERC4626 vaults, reentrancy, flash loans, signature replay, or proxy/upgrade bugs.
---

# BUG CLASSES — DeFi Smart Contract Vulnerabilities

10 bug classes. Each one with root cause, vulnerable code, fix, grep patterns, and real paid examples.

---

## 1. ACCOUNTING STATE DESYNCHRONIZATION
> #1 Critical bug class — 28% of all Criticals on Immunefi.
> Real protocols: Yeet, Alchemix V3, Folks Finance, ResupplyFi, MetaPool

### What It Is

Two state variables are supposed to stay in sync. One code path updates variable A but forgets variable B. Later code reads both and makes decisions based on the stale B.

```
Real Value = A - B
If A is updated but B isn't → Real Value appears larger than it is → phantom value
```

### Root Cause Pattern

```solidity
// BEFORE (correct state):
// aToken.balanceOf(this) = 1000  (principal + yield)
// totalSupply = 1000              (only principal)
// yield = 1000 - 1000 = 0        ✓ correct

// Attacker triggers startUnstake:
totalSupply -= amount;  // decremented BEFORE transfer
// totalSupply = 900 now
// aToken.balanceOf still = 1000
// yield appears = 1000 - 900 = 100 (PHANTOM)

// Now harvest():
yieldAmount = aToken.balanceOf(this) - totalSupply;
// = 1000 - 900 = 100 (phantom yield — no real yield was earned)
// Protocol harvests 100 of principal and distributes as "yield"
```

### Variants

**Variant 1: Phantom Yield** — totalSupply decremented before transfer
```solidity
// Yeet protocol (35 duplicate reports):
function startUnstake(uint256 amount) external {
    totalSupply -= amount;  // decremented here, transfer happens later
    // balanceOf(this) - totalSupply now shows phantom yield
}
```

**Variant 2: Fast Path Skips State Update** — early return bypasses critical updates
```solidity
// Alchemix V3 claimRedemption:
function claimRedemption(uint256 tokenId) external {
    if (transmuter.balance >= amount) {
        transmuter.transfer(user, amount);
        _burn(tokenId);
        return;  // EARLY RETURN — cumulativeEarmarked, _redemptionWeight, totalDebt never updated
    }
    // SLOW PATH: updates all state vars correctly
    alchemist.redeem(...);
}
```

**Variant 3: Rewards Accrue to Wrong Accumulator**
```solidity
// Folks Finance Liquid Staking:
function addRewards(uint256 amount) external {
    algoBalance += amount;        // rewards go here
    // MISSING: TOTAL_ACTIVE_STAKE += amount
}
function withdraw(uint256 shares) external {
    uint256 myAmount = (shares * TOTAL_ACTIVE_STAKE) / totalSupply;
    // TOTAL_ACTIVE_STAKE never got rewards → underflow → freeze
}
```

**Variant 4: Update Happens in Wrong Order**
```solidity
// Alchemix:
function deposit(uint256 amount) external {
    _shares = (amount * totalShares) / totalAssets;  // calculated BEFORE deposit
    totalAssets += amount;   // assets added AFTER shares calculated
    totalShares += _shares;  // shares calculation used stale totalAssets → wrong rate
}
```

### Grep Patterns
```bash
# List all balance/supply variables
grep -rn "totalSupply\|totalShares\|totalAssets\|totalDebt\|totalCollateral\|cumulativeReward\|rewardPerShare" contracts/ | grep -v "//\|test"

# Find ALL writes to key variables
grep -rn "totalSupply\s*[-+*]=[^=]\|totalSupply\s*=" contracts/
grep -rn "cumulativeRewardPerShare\s*[-+*]=" contracts/

# Find all early returns in claim/redeem functions
grep -rn "\breturn\b" contracts/ -B3 | grep -B3 "if\b"
# For each early return: which state updates are in the normal path but not this one?
```

### Kill Signals
- Only one variable is involved (no pair to desync)
- Both paths update all state vars identically
- Transfer happens AFTER state update in every path (correct CEI)
- Single-transaction atomicity prevents the window (no intermediate state visible)

### Real Paid Examples

| Protocol | Root Cause |
|----------|-----------|
| Yeet | `startUnstake` decrements totalSupply before transfer → phantom yield |
| Alchemix V3 | `claimRedemption` fast path skips 3 state updates → phantom collateral |
| Folks Finance | Rewards accrue to `algoBalance` not `TOTAL_ACTIVE_STAKE` → underflow |
| ResupplyFi | ERC4626 near-empty vault exchange rate manipulation |
| MetaPool | `mint()` skipped receipt check from `_deposit()` |

---

## 2. ACCESS CONTROL
> #2 Critical bug class — 19% of all Criticals. $953M lost in 2024 alone.
> Real protocols: Wormhole ($10M), ZeroLend, Flare FAssets, Parity ($150M frozen)

### What It Is

A function that should be restricted is callable by anyone. Or a function checks the wrong condition (existence vs. ownership). Or a modifier uses `if` instead of `require` and silently does nothing for non-admins.

### Root Cause Patterns

**Variant 1: Missing Modifier on Sibling Function**
```solidity
function vote(uint256 tokenId) external onlyNewEpoch(tokenId) {  // guarded
function reset(uint256 tokenId) external onlyNewEpoch(tokenId) { // guarded
function poke(uint256 tokenId) external {                         // NO GUARD
    // Anyone calls poke() unlimited times per epoch
    // poke() distributes FLUX rewards → infinite inflation
}
```

**Variant 2: Wrong Check — Existence vs. Ownership**
```solidity
// ZeroLend split() — anyone can steal victim's tokens:
function split(uint256 tokenId, uint256 amount) external {
    _requireOwned(tokenId);  // checks if token EXISTS, not if caller OWNS it
    _burn(tokenId);
    _mint(msg.sender, amount);  // attacker gets tokens they don't own
}
```

**Variant 3: Tautology in Require**
```solidity
// Flare FAssets — proof validation always passes:
require(
    sourceAddressesRoot == sourceAddressesRoot,  // always true! comparing to itself
    "Invalid"
);
```

**Variant 4: Silent Modifier (if vs require)**
```solidity
// VULNERABLE — non-admin silently gets through:
modifier onlyAdmin() {
    if (msg.sender == admin) {
        _;  // only executes body for admin
    }
    // non-admin: modifier body skipped, function STILL EXECUTES
}

// CORRECT:
modifier onlyAdmin() {
    require(msg.sender == admin, "Not admin");
    _;
}
```

**Variant 5: Uninitialized Proxy — initialize() Callable by Anyone**
```solidity
contract Vault {
    address public owner;
    function initialize(address _owner) public {  // MISSING: initializer modifier
        owner = _owner;  // anyone can call this and become owner
    }
}
// Fix: constructor() { _disableInitializers(); }
```

### Grep Patterns
```bash
# Find sibling function families — do ALL have the same modifier set?
grep -rn "function vote\|function poke\|function reset\|function update\|function claim\|function harvest" contracts/ -A2

# Ownership check pattern — existence vs ownership?
grep -rn "_requireOwned\|ownerOf\|_isApprovedOrOwner\|_checkAuthorized" contracts/ -B5 -A5

# Silent modifiers using if without revert
grep -rn "modifier\b" contracts/ -A8 | grep -B3 "if (" | grep -v "require\|revert\|else.*revert"

# Uninitialized initializer
grep -rn "function initialize\b" contracts/ -A3
grep -rn "_disableInitializers()" contracts/

# Missing access control on critical functions
grep -rn "function mint\b\|function burn\b\|function emergencyWithdraw\b\|function upgradeTo\b" contracts/ -A3
```

### Roles Audit Checklist
```
For every privileged role:
□ Who can GRANT this role?
□ Who can REVOKE this role?
□ Is the initial role granted in constructor to the correct address?
□ Can the same address grant itself additional roles?
□ Is there a timelock on role transfers?
□ What happens if this role address is address(0)?
□ Are all roles actually granted that are referenced in the code?
```

### Kill Signals
- Function has correct modifier AND modifier uses `require` (not silent `if`)
- Upgrade functions have `onlyOwner` or role check in `_authorizeUpgrade`
- `_disableInitializers()` is present in implementation constructor
- All roles referenced in `onlyRole()` are actually granted in constructor or initializer

### Real Paid Examples

| Protocol | Payout | Bug |
|----------|--------|-----|
| Wormhole | $10M | Uninitialized UUPS proxy → anyone calls initialize() |
| ZeroLend | n/a | split() uses existence check not ownership check |
| Alchemix | n/a | poke() missing onlyNewEpoch → infinite FLUX inflation |
| Flare | n/a | Tautology in require → proof always passes |
| Parity | $150M frozen | No access control on initWallet() in library |

---

## 3. INCOMPLETE CODE PATH
> #3 Critical bug class — 17% of Criticals.
> Real protocols: Plume, Puffer, ThunderNFT, Alchemix V3, MetaPool, LI.FI

### What It Is

The happy path (deposit, create, place) handles tokens correctly. An alternate path (update, partial fill, fast path, zero amount) either moves tokens WITHOUT updating accounting, or updates accounting WITHOUT moving tokens, or deletes state regardless of whether the operation succeeded.

### Root Cause Patterns

**Variant 1: Update Function Missing Refund**
```solidity
// ThunderNFT — place_order takes tokens, update_order doesn't refund:
function place_order(OrderInput calldata order) external {
    token.safeTransferFrom(msg.sender, address(this), order.price);  // takes tokens
    orders[orderId] = order;
}
function update_order(OrderInput calldata updatedOrder) external {
    if (updatedOrder.price < existingOrder.price) {
        uint256 refund = existingOrder.price - updatedOrder.price;
        // BUG: NO REFUND for sell orders → tokens permanently stuck
    }
    orders[orderId] = updatedOrder;
}
```

**Variant 2: Partial Fill — Token Stuck**
```solidity
// Plume — refund handles ETH only, not ERC20:
function swapForETH(uint256 amountIn) external {
    token.safeTransferFrom(msg.sender, address(this), amountIn);
    uint256 filled = dex.swap(amountIn);  // partial fill possible
    _refundExcessEth(amountIn - filled);  // BUG: refunds ETH only
    // If token is ERC20: remaining tokens NEVER refunded
}
```

**Variant 3: Queue Entry Deleted on Failure**
```solidity
// Puffer — delete happens before execution, in batch where one failure corrupts all:
function executeTransaction(bytes32 txHash) external {
    Transaction memory tx = queue[txHash];
    delete queue[txHash];  // deleted BEFORE execution
    (bool success,) = tx.target.call{value: tx.value}(tx.data);
    // In batch: failure of one element corrupted state for whole batch
}
```

**Variant 4: safeApprove Without Cleanup**
```solidity
// Plume — residual approval blocks second swap:
function executeSwap(uint256 amount) external {
    token.safeApprove(router, amount);    // approve full amount
    uint256 used = router.swap(amount);   // partial fill: used < amount
    // remaining approval (amount - used) never cleared
    // Next call: safeApprove(router, newAmount) → REVERTS (current allowance != 0)
}
// Fix: token.safeApprove(router, 0); before approving
```

**Variant 5: mint() Skips Receipt Check That deposit() Has**
```solidity
// MetaPool — mint() bypasses the check enforced by _deposit():
function deposit(uint256 assets, address receiver) public override returns (uint256 shares) {
    shares = _deposit(assets, receiver);  // includes receipt validation
}
function mint(uint256 shares, address receiver) public override returns (uint256 assets) {
    assets = convertToAssets(shares);
    _mint(receiver, shares);  // BUG: directly mints without _deposit() validation
    // _deposit() has: require(actualReceived >= expectedAmount, "Insufficient")
    // mint() skips this → mints without receiving actual assets
}
```

### The Function Family Comparison Test

For every pair of functions that do similar things:
```
1. List all state changes in function A (deposit/place/create)
2. List all state changes in function B (withdraw/update/cancel)
3. For each state change in A: does B have the corresponding reverse?
4. For each token transfer in A: does B have the corresponding refund?
5. For each event in A: does B emit a corresponding event?
If A does X but B doesn't do the reverse of X → BUG.
```

### Grep Patterns
```bash
# Find create/place/add vs update/modify function pairs
grep -rn "function place_\|function create_\|function add_\|function open_" contracts/ -A5
grep -rn "function update_\|function modify_\|function edit_\|function change_" contracts/ -A5

# Find refund logic — does it handle both ETH and ERC20?
grep -rn "_refundExcess\|refundTokens\|refundAmount\|remainder" contracts/ -A10

# safeApprove without zero-reset before
grep -rn "safeApprove\b" contracts/

# delete before operation completes
grep -rn "delete\b" contracts/ -B5 -A5

# ERC4626: compare deposit() vs mint(), withdraw() vs redeem()
grep -rn "function deposit\|function mint\|function withdraw\|function redeem" contracts/ -A10
```

### Kill Signals
- update/cancel functions explicitly handle token transfers in all cases
- Partial fills refund both ETH and ERC20 paths
- `safeApprove(router, 0)` present before every `safeApprove(router, amount)`
- `deposit()` and `mint()` both call the same internal `_deposit()` function

### Real Paid Examples

| Protocol | Root Cause |
|----------|-----------|
| Plume | `_refundExcessEth` handles ETH only → ERC20 partial fill stuck |
| Plume | `safeApprove` without cleanup → second swap reverts |
| ThunderNFT | `update_order` missing refund for sell orders |
| Puffer | `executeTransaction` deletes queue entry on failure |
| LI.FI | $1.7M — library skips whitelist → arbitrary external call |
| MetaPool | `mint()` bypasses receipt check that `deposit()` has |

---

## 4. OFF-BY-ONE & BOUNDARY CONDITIONS
> #4 High bug class — 22% of Highs. Single character change. Massive impact.
> Real protocols: VeChain Stargate, Alchemix, Flare, Shardeum

### What It Is

At a boundary condition (period end, epoch transition, time == deadline), the wrong comparison operator routes to the wrong code branch. The "equal case" is the bug — `>` misses it, `>=` catches it.

### Root Cause Pattern

```solidity
// VeChain Stargate — post-exit drain:
function _claimableDelegationPeriods(address delegator) internal view returns (uint256) {
    uint256 endPeriod = userInfo[delegator].exitPeriod;

    // BUG: when block.period == endPeriod (exactly at exit), condition is FALSE
    if (endPeriod > nextClaimablePeriod) {
        return 0;  // exited users get nothing — correct for this case
    }
    // WRONG: endPeriod == nextClaimablePeriod lands here
    return nextClaimablePeriod - lastClaimedPeriod;
    // → returns rewards for the period after exit → infinite post-exit drain

    // FIX:
    // if (endPeriod >= nextClaimablePeriod) { return 0; }
}
```

### The 6 Boundary Locations to Check

**1. Period / Epoch Boundaries**
```bash
grep -rn "period\|epoch\|round" contracts/ -i | grep "[<>][^=]"
# Every > should be questioned: should it be >=?
```

**2. Time-Based Locks**
```solidity
// Question: is the exact moment of expiry locked or unlocked?
return block.timestamp < users[user].depositTimestamp + lockPeriod;
// At timestamp == depositTimestamp + lockPeriod: false → NOT locked (unlocked at exact expiry)
```

**3. Loop Break Conditions**
```solidity
// Alchemix — processes yield per week:
for (uint256 t = weekStart; t <= weekEnd; t += WEEK) {
    if (t > roundedTimestamp) break;  // BUG: should be t >= roundedTimestamp
    // When t == roundedTimestamp: doesn't break → processes incomplete week
    // → caches supply at wrong timestamp → division by zero in claims
}
```
```bash
grep -rn "\bbreak\b" contracts/ -B5
# For each break: should it also break when equal?
```

**4. Array Index Boundaries**
```solidity
for (uint256 i = 0; i <= array.length; i++) {  // should be i < array.length
    process(array[i]);  // array[array.length] = out of bounds → revert
}
```
```bash
grep -rn "\.length\s*-\s*1\|i\s*<=\s*.*\.length\b" contracts/
```

**5. Amount / Balance Boundaries**
```solidity
require(balanceOf(msg.sender) >= amount);  // allows exact full withdrawal
// vs:
require(balanceOf(msg.sender) > amount);   // can't withdraw last wei
```

**6. Rounding and Precision Boundaries**
```solidity
// Can any input amount produce exactly 0 output that should be non-zero?
uint256 shares = (amount * totalSupply) / totalAssets;
// If amount is just below threshold → gets 0 shares → free deposit entry
```

### Mental Test for Every Comparison

For every `if (A > B)` found: "What happens when A == B?" Which branch? Is that correct?
For every `if (A < B)` found: "What happens when A == B?"

### Grep Patterns
```bash
# Variables that represent boundaries
grep -rn "Period\|Epoch\|Round\|Index\|Timestamp\|Deadline" contracts/ -A3 | grep "[<>][^=]"
grep -rn "period\|epoch\|round\|deadline\|cutoff\|threshold" contracts/ -A3 | grep "[<>][^=]"

# Loop breaks — boundary included?
grep -rn "\bbreak\b\|\bcontinue\b" contracts/ -B10
```

### Kill Signals
- Both `>=` and `>` are present with clear, distinct intent in comments
- Unit tests explicitly cover the equal-case boundary
- No period/epoch system in the contract (can't have epoch boundary bug)

### Real Paid Examples

| Protocol | Impact | Bug |
|----------|--------|-----|
| VeChain Stargate | High | `>` should be `>=` → infinite post-exit reward drain |
| Alchemix | High | `>` should be `>=` in loop → processes incomplete week → div/0 |
| VeChain (same) | High | Same bug reported by 3 different hunters simultaneously |

---

## 5. ORACLE / PRICE MANIPULATION
> 12% of all reports, largest individual payouts. $117M Mango, $70M Curve.
> Real protocols: Swaylend, ZeroLend, Chainlink integrations, Pyth, Uniswap V2/V3

### What It Is

If a protocol reads a wrong price, it can be tricked into accepting undercollateralized loans, minting assets with fake backing, liquidating healthy positions, or issuing more debt than collateral supports. With a flash loan: attacker has $1B+ of free capital for 1 block.

### Chainlink Bugs

**Bug A — Missing Staleness Check (most common)**
```solidity
// VULNERABLE:
(, int256 price,,,) = priceFeed.latestRoundData();
return uint256(price);
// If Chainlink node goes down, last reported price returned indefinitely

// CORRECT:
(, int256 price,, uint256 updatedAt,) = priceFeed.latestRoundData();
require(block.timestamp - updatedAt <= MAX_PRICE_AGE, "Stale price");
require(price > 0, "Invalid price");
return uint256(price);
```

**Bug B — Missing Sequencer Uptime Check (L2 only)**
```solidity
// On Arbitrum, Optimism: if sequencer goes down, prices can be stale
(, int256 answer, uint256 startedAt,,) = sequencerUptimeFeed.latestRoundData();
require(answer == 0, "Sequencer down");
require(block.timestamp - startedAt >= GRACE_PERIOD, "Grace period active");
```

**Bug C — Using latestAnswer() (deprecated)**
```solidity
int256 price = priceFeed.latestAnswer();  // doesn't return timestamp → no staleness check possible
```

### Pyth Bugs

**Bug A — Confidence Not Subtracted**
```solidity
// VULNERABLE: uses price directly without confidence interval
PythStructs.Price memory p = pyth.getPriceNoOlderThan(priceId, MAX_AGE);
return amount * uint256(int256(p.price)) / 1e8;  // overstates collateral

// CORRECT (conservative):
return amount * uint256(int256(p.price - int64(p.conf))) / 1e8;
```

**Bug B — Hardcoded Global Confidence Threshold**
```solidity
uint256 public constant ORACLE_MAX_CONF_WIDTH = 20;  // BPS — may fail for volatile assets
```

### AMM Spot Price (Most Dangerous)

**Uniswap V2 — getReserves() Attack**
```solidity
// VULNERABLE: reading price from getReserves() in same block as action
(uint112 reserve0, uint112 reserve1,) = pair.getReserves();
return reserve1 * 1e18 / reserve0;  // spot price — manipulable via flash loan

// Attack: Flash loan 10M USDC → swap → inflated price → deposit → borrow → drain → swap back
```

**Uniswap V3 — slot0() Attack**
```solidity
// VULNERABLE: slot0 is manipulable within one block
(uint160 sqrtPriceX96,,,,,,) = pool.slot0();

// SAFE (TWAP):
uint32[] memory secondsAgos = new uint32[](2);
secondsAgos[0] = 1800;  // 30 minutes ago
secondsAgos[1] = 0;
(int56[] memory tickCumulatives,) = pool.observe(secondsAgos);
// Cost to manipulate TWAP for 30 min > profit from exploit
```

**Protocol-Internal (balanceOf) Donation Attack**
```solidity
// VULNERABLE:
function totalAssets() public view returns (uint256) {
    return token.balanceOf(address(this));  // manipulable via direct token transfer
}
// Attack: donate tokens directly → inflate price → borrow more
```

### Grep Patterns
```bash
grep -rn "latestRoundData()" contracts/ -A5
# Is updatedAt captured? Is block.timestamp - updatedAt <= MAX checked?

grep -rn "sequencer\|SEQUENCER\|ArbitrumSequencer" contracts/
# Present on L2? If not → bug

grep -rn "slot0\b\|getReserves()" contracts/
# Any pricing logic using these = flash loan manipulable

grep -rn "latestAnswer()" contracts/
# Deprecated → should use latestRoundData()
```

### Oracle Checklist
```
□ Chainlink: updatedAt staleness check present?
□ Chainlink: price > 0 check present?
□ Chainlink: on L2? Sequencer uptime check present?
□ Chainlink: using deprecated latestAnswer()?
□ Pyth: confidence subtracted from collateral valuation?
□ Pyth: per-asset confidence threshold or global?
□ Uniswap V2: using getReserves() for pricing? → needs TWAP
□ Uniswap V3: using slot0() for pricing? → needs TWAP
□ Protocol: using balanceOf(this) for pricing? → needs internal tracking
□ TWAP: window >= 30 minutes?
□ Circuit breaker if price moves >X% in single block?
```

### Kill Signals
- Protocol has no lending/borrowing (yield-only protocols like simple staking vaults can't be oracle-drained)
- DEX swap is operational only (not used for security-critical collateral valuation)
- All AMM price reads use TWAP with >= 30 minute window
- Price has both staleness AND validity (> 0) checks

---

## 6. ERC4626 VAULT BUGS
> Found repeatedly in 2024-2025: Belong, ResupplyFi, Napier, Astaria, Smilee Finance, FlatMoney

### What It Is

ERC4626 = tokenized vault standard. Users deposit assets, get shares. `1 share = totalAssets / totalShares`. The edge cases kill protocols.

### Bug 1: First Depositor Inflation Attack

```
1. Attacker deposits 1 wei → gets 1 share
2. Attacker DONATES 999,999 USDC directly to vault (not via deposit)
   → totalAssets = 1M, totalSupply = 1 share → 1 share = 1M USDC
3. Victim deposits 999,999 USDC
   → shares = (999,999 * 1) / 1,000,000 = 0 shares (rounds down)
   → Victim gets 0 shares, can't withdraw
4. Attacker redeems 1 share → receives ~2M USDC
```

```solidity
// VULNERABLE (no virtual offset):
function convertToShares(uint256 assets) public view returns (uint256) {
    uint256 supply = totalSupply();
    return supply == 0 ? assets : (assets * supply) / totalAssets();
}

// FIX (OpenZeppelin virtual offset):
return assets.mulDiv(
    totalSupply() + 10 ** _decimalsOffset(),  // +1 virtual share
    totalAssets() + 1,                          // +1 virtual asset
    rounding
);
```

### Bug 2: Share Transfer Missing Stake/Lock Record Migration

```solidity
// Custom ERC20 with lock period tracking:
mapping(address => Stake[]) public stakes;

function _update(address from, address to, uint256 value) internal override {
    super._update(from, to, value);  // just moves balances
    // MISSING: migrate stakes from 'from' to 'to'
    // Bob has shares but no stake records → can't withdraw → permanent freeze
}
```

### Bug 3: Rounding Direction Attacks

```solidity
// If protocol rounds consistently in user's favor:
// Swap 1 wei → get back 1 wei (should be 0.5 wei rounded down)
// Repeat 1M times → drain pool

// RULE:
// For deposits/mints: round DOWN (fewer shares issued = conservative = safe)
// For withdrawals/redeems: round DOWN (fewer assets given = conservative = safe)
// If rounding consistently favors user → drainable via tiny swaps
```

### Bug 4: Donation Attack via balanceOf

```solidity
// VULNERABLE: price derived from raw balance
function totalAssets() public view override returns (uint256) {
    return underlying.balanceOf(address(this));  // manipulable via direct transfer
}

// SAFE: track internally
uint256 private _trackedBalance;
function totalAssets() public view override returns (uint256) {
    return _trackedBalance;
}
```

### Grep Patterns
```bash
# First depositor check
grep -rn "convertToShares\|_convertToShares\|previewDeposit" contracts/ -A5
# Is denominator: totalAssets() + 1?
# Is numerator: totalSupply() + 10**decimalsOffset()?

# Transfer without stake migration
grep -rn "_update\b\|function _transfer\b" contracts/ -A10
# Does _update migrate stakes/locks/rewards when from != 0 AND to != 0?

# Donation attack
grep -rn "totalAssets\(\)" contracts/ -A3
# Does it use balanceOf(address(this)) directly?

# Rounding direction
grep -rn "/ totalAssets\|/ totalSupply\|/ reserves" contracts/
```

### Vault Checklist
```
□ First depositor: does convertToShares use +1 virtual offset?
□ Is there a "dead shares" mechanism or minimum deposit?
□ Transfer: does _update migrate stake/lock/reward records?
   (OR: are transfers disabled entirely?)
□ totalAssets(): tracked internally or raw balanceOf?
□ Rounding: consistent direction (always favor protocol)?
□ Does mint() call the same internal logic as deposit()?
□ Does redeem() call the same internal logic as withdraw()?
```

### Kill Signals
- OpenZeppelin ERC4626 v4.9+ with `_decimalsOffset()` override present
- Protocol is NOT ERC4626 — uses simpler 1:1 share model (inflation attack doesn't apply)
- Transfers disabled entirely (TransferLocked pattern) prevents stake migration bug
- `totalAssets()` uses internal tracked balance, not `balanceOf(this)`

---

## 7. REENTRANCY (ALL VARIANTS)
> $300M+ losses since Jan 2024. Penpie $27M, Curve $70M.
> Classic + Cross-function + Read-only + Cross-contract. All 4 must be checked.

### Variant 1: Classic Reentrancy (CEI Violation)

```solidity
// VULNERABLE: state updated AFTER external call
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    (bool success,) = msg.sender.call{value: amount}("");  // attacker's receive() fires
    require(success);
    balances[msg.sender] -= amount;  // runs AFTER attacker's callback → reenter with old balance
}

// CORRECT (Checks-Effects-Interactions):
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    balances[msg.sender] -= amount;  // Effect FIRST
    (bool success,) = msg.sender.call{value: amount}("");  // Interaction last
    require(success);
}
```

### Variant 2: Cross-Function Reentrancy

```solidity
// withdraw() and transfer() share balance state:
function withdraw() external nonReentrant {
    uint256 amount = balances[msg.sender];
    balances[msg.sender] = 0;
    token.safeTransfer(msg.sender, amount);  // triggers ERC777 tokensReceived
    // In tokensReceived: calls transfer() (different function — different nonReentrant mutex?)
}
// KEY: Does nonReentrant block ALL functions or just the current one?
// OpenZeppelin ReentrancyGuard: blocks reentry into ANY nonReentrant function on the contract
// Custom mutex: check if it's per-function or per-contract
```

### Variant 3: Read-Only Reentrancy ($70M Curve)

```solidity
// Contract A (e.g., Curve pool) is mid-state-change when external call fires:
function removeLiquidity() external nonReentrant {
    totalSupply -= lpAmount;  // totalSupply updated
    (bool success,) = msg.sender.call{value: ...}("");  // fires attacker code
    poolBalance -= withdrawn;  // poolBalance updated AFTER the call
}

// In attacker's receive():
// Reads CurvePool.totalSupply (updated) and CurvePool.poolBalance (NOT yet updated)
// Price = poolBalance / totalSupply → artificially inflated
// Borrows against inflated collateral value in a third protocol
```

### Variant 4: Cross-Contract Reentrancy

```
Protocol A calls Protocol B
Protocol B makes external call (to attacker)
Attacker calls Protocol A while B is mid-execution
Protocol A sees consistent own state
But Protocol A's computation depends on Protocol B's state (which is inconsistent)
```

### Grep Patterns
```bash
# Step 1: Find all external calls
grep -rn "\.call(\|\.call{value\|safeTransfer\|safeTransferFrom\|\.transfer(\|\.send(" contracts/

# Step 2: For each — is state updated BEFORE this call?
# Does the function have nonReentrant?

# Step 3: ERC777 tokens with hooks
grep -rn "ERC777\|IERC777\|tokensReceived\|tokensToSend" contracts/

# Step 4: External state read during execution (read-only reentrancy)
grep -rn "ICurve\|IBalancer\|IUniswap\|IPool\b" contracts/ -A3

# External calls in MIDDLE of state updates (state before AND after the call)
grep -rn "\.call{value\|\.call(" contracts/ -B20 -A5
```

### Kill Signals
- All `_processYield` / `_claim` functions follow CEI: state updated before transfer
- Reward token is not ERC777 (no tokensReceived hook)
- `nonReentrant` present on all external-call-containing functions
- `harvest()` / sensitive functions require whitelisted caller (attacker can't trigger)

### Real Paid Examples

| Protocol | Loss | Variant |
|----------|------|---------|
| Penpie | $27M | Classic: `batchHarvestMarketRewards()` missing nonReentrant |
| Curve Finance | $70M | Read-only: Vyper compiler bug broke reentrancy guard |
| Siren Protocol | Contest | Cross-function: withdraw() + claimFees() share state |
| Rari Capital | $80M | Cross-contract: Compound fork + ETH callback |

---

## 8. FLASH LOAN ATTACKS
> Used in 83% of eligible exploits. $0 capital required.
> Real protocols: Beanstalk $182M, Mango $117M, Euler $197M

### What It Is

Flash loans give unlimited capital for 1 block with no collateral. Any check that relies on "attacker doesn't have enough tokens" is broken.

### The 3 Attack Patterns

**Pattern 1: Oracle Manipulation**
```
1. Flash borrow 100,000 ETH
2. Dump 100,000 ETH → TARGET_TOKEN on Uniswap (price crashes)
3. Liquidate TARGET_TOKEN positions at crashed price → steal collateral
4. Repay flash loan
```
OR (pump version):
```
1. Flash borrow USDC
2. Buy TARGET_TOKEN → price pumps
3. Deposit as collateral at inflated price
4. Borrow against it
5. Sell TARGET_TOKEN back (price normalizes)
6. Repay flash loan → protocol has bad debt
```

**Pattern 2: Governance Attack**
```
1. Flash borrow governance tokens (no collateral needed)
2. Vote on malicious proposal (if no snapshot delay)
3. Execute: "send all funds to attacker"
4. Repay flash loan
Required weakness: voting power checked at vote time, not at proposal creation
Defense: snapshot voting power at proposal creation block
```

**Pattern 3: Liquidity Manipulation**
```
1. Flash borrow LP tokens
2. Remove liquidity → temporarily drain pool
3. Pool's balances are tiny → exploit "minimum liquidity" edge case
4. Re-add liquidity → repay flash loan
```

### Flash Loan Providers

```solidity
// Balancer V2 (no fee, mainnet + most networks)
address constant BALANCER_VAULT = 0xBA12222222228d8Ba445958a75a0704d566BF2C8;
// Implement: receiveFlashLoan(tokens, amounts, feeAmounts, userData)

// Morpho Blue (~0% fee)
address constant MORPHO = 0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb;
// Implement: onMorphoFlashLoan(assets, data)

// Aave V3 (0.05% fee)
address constant AAVE_POOL = 0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2;
// Implement: executeOperation(assets, amounts, premiums, initiator, params)

// Uniswap V2 (0.3% fee)
// IUniswapV2Pair.swap(amount0Out, amount1Out, to, data)
// Implement: uniswapV2Call(sender, amount0, amount1, data)
```

### Flash Loan Vulnerability Checklist
```
□ Does any function read an AMM spot price (getReserves/slot0)?
  → Can be manipulated in same block with flash loan
□ Does any function allow voting without snapshot delay?
  → Flash loan governance attack
□ Does any pricing function use balanceOf(address(this))?
  → Donation attack (flash loan + transfer)
□ Is there ANY check of "how many tokens does attacker have?"
  → If yes: can they flash borrow enough to pass the check?
□ Does any calculation compare current balance to a stored value?
  → Can be manipulated by depositing/withdrawing via flash loan
```

### Kill Signals
- Protocol has no lending/borrowing, oracle pricing, or governance (flash loan has nothing to exploit)
- Early withdrawal fee makes flash deposit/withdraw unprofitable (0.1% fee > 1-block yield steal)
- Harvest requires whitelisted caller (attacker can't trigger harvest to abuse it)
- All price reads use TWAP (can't be manipulated in single block)

---

## 9. SIGNATURE REPLAY
> High payout potential $5K-$500K. Cross-chain opportunity.
> Real protocols: Polygon $2.2M, zkSync $200K, Alchemix, EIP-2612 permit

### The 3 Variants

**Variant 1: Cross-Chain Signature Replay**
```solidity
// VULNERABLE: signature doesn't include chainId
function claimRewards(address user, uint256 amount, bytes memory signature) external {
    bytes32 message = keccak256(abi.encodePacked(user, amount));  // no chainId!
    address signer = ECDSA.recover(message, signature);
    require(signer == authorizedSigner, "Invalid signature");
    // Attack: claim on Ethereum, replay same signature on Arbitrum
}

// FIX: include chainId in DOMAIN_SEPARATOR
bytes32 DOMAIN_SEPARATOR = keccak256(abi.encode(
    keccak256("EIP712Domain(string name,uint256 chainId,address verifyingContract)"),
    keccak256("Protocol"),
    block.chainid,      // CHAIN ID
    address(this)       // CONTRACT ADDRESS
));
```

**Variant 2: Missing Nonce (Same-Chain Replay)**
```solidity
// VULNERABLE: no nonce → same signature reusable indefinitely
function executePermit(address user, uint256 amount, bytes memory sig) external {
    bytes32 hash = keccak256(abi.encodePacked(user, amount, address(this)));
    // No nonce tracking → replay this call indefinitely
}
// FIX:
mapping(address => uint256) public nonces;
bytes32 hash = keccak256(abi.encodePacked(user, amount, nonces[user]++, address(this)));
```

**Variant 3: EIP-2612 Permit Frontrun DoS**
```solidity
// Victim submits: permitAndDeposit(owner, spender, value, deadline, v, r, s)
// Attacker sees in mempool, frontruns: token.permit(owner, spender, value, deadline, v, r, s)
// → nonce consumed → victim's tx reverts (permit fails, deposit never happens)

// SAFE pattern: wrap permit in try/catch
function permitAndDeposit(uint256 amount, uint256 deadline, uint8 v, bytes32 r, bytes32 s) external {
    try token.permit(msg.sender, address(this), amount, deadline, v, r, s) {}
    catch {}  // allowance already set → deposit proceeds regardless
    token.safeTransferFrom(msg.sender, address(this), amount);
}
```

**ECDSA Malleability**
```solidity
// VULNERABLE: signatures used as mapping keys (bytes not address)
mapping(bytes => bool) public usedSignatures;
function claim(bytes memory sig) external {
    require(!usedSignatures[sig]);
    // Attacker modifies s value → different bytes, same signer → bypasses check
}
// FIX: use OpenZeppelin ECDSA.recover (normalizes s to lower half)
```

### Grep Patterns
```bash
grep -rn "ecrecover\|ECDSA\.recover" contracts/
grep -rn "chainId\|block\.chainid\|DOMAIN_SEPARATOR" contracts/
# ecrecover present without corresponding chainId = replay vulnerability

grep -rn "nonces\[\|nonce\b" contracts/
# ecrecover without nonce tracking = potentially replayable

grep -rn "permit(" contracts/ | grep -v "//\|IERC20Permit\|interface"
grep -rn "try.*permit\|catch.*permit" contracts/
# Safe pattern: wrapped in try/catch
```

### Signature Checklist
```
□ Does signature include: chainId? (cross-chain replay protection)
□ Does signature include: contract address? (replay between contracts)
□ Does signature include: nonce? (same-chain replay protection)
□ Does signature include: deadline/expiry?
□ Is OpenZeppelin ECDSA used (not raw ecrecover)?
□ Are signatures used as mapping keys? (malleability attack)
□ Is permit() wrapped in try/catch in compound functions?
□ If multi-chain: is DOMAIN_SEPARATOR computed at runtime (not hardcoded)?
```

### Kill Signals
- Protocol has no off-chain signature mechanism at all
- DOMAIN_SEPARATOR includes both `block.chainid` and `address(this)`
- All signature uses have nonces with `nonces[user]++` pattern
- OpenZeppelin ECDSA library used throughout

---

## 10. PROXY / UPGRADE BUGS
> $10M Wormhole, $150M Parity. Uninitialized impl = anyone becomes admin.
> Patterns: UUPS, Transparent Proxy, Beacon Proxy, Storage Collision

### Variant 1: Uninitialized Implementation (Most Common Critical)

```solidity
// VULNERABLE: implementation deployed but initialize() never called
// AND: no _disableInitializers() in constructor
contract MyVault {
    function initialize(address _owner) external {
        require(!initialized);
        initialized = true;
        owner = _owner;
    }
}
// Attack:
// 1. Find impl address: proxy.implementation()
// 2. Call impl.initialize(attacker) directly → attacker owns impl
// 3. Call impl.upgradeTo(malicious_contract) → proxy delegates to malicious
// 4. Drain all funds through proxy

// FIX:
constructor() {
    _disableInitializers();  // prevents any initialize() call on impl directly
}
```

### Variant 2: Storage Collision

```solidity
// VULNERABLE: New implementation adds variable BEFORE existing ones
// V1: slot 0 = totalAssets, slot 1 = owner
// V2: slot 0 = newFee (overwrites totalAssets!), slot 1 = totalAssets (overwrites owner!)

// FIX: Always append new variables at the END
// Use __gap arrays for reserved slots:
uint256[50] private __gap;  // reserve 50 slots for future vars
```

### Variant 3: UUPS Without _authorizeUpgrade Protection

```solidity
// VULNERABLE: Anyone can upgrade
contract MyUUPS is UUPSUpgradeable {
    function _authorizeUpgrade(address newImplementation) internal override {
        // EMPTY! No access control → anyone calls upgradeTo(malicious)
    }
}

// CORRECT:
function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
```

### Variant 4: Reinitializer Not Protected

```solidity
function initializeV2() public reinitializer(2) {
    // No access control → anyone calls this → resets state
}
```

### Grep Patterns
```bash
grep -rn "function initialize\b" contracts/ -A3
# Does it have: initializer modifier? _disableInitializers() in constructor?

grep -rn "_disableInitializers()" contracts/
# Absent? Check if proxy implementation is separately deployable

grep -rn "_authorizeUpgrade" contracts/ -A3
# Is there: onlyOwner / onlyRole / require(msg.sender == admin)?
# Empty body = anyone can upgrade

# Storage layout comparison between versions
grep -rn "slot\|__gap\|ERC1967Storage" contracts/
```

### Proxy Checklist
```
□ Is the implementation contract upgradeable? (UUPS/Transparent/Beacon?)
□ Is implementation's initialize() protected by initializer modifier?
□ Is _disableInitializers() called in implementation constructor?
□ Does _authorizeUpgrade() have access control?
□ If new version: are variables only added at the END of storage?
□ Is there a __gap reserved for future variables?
□ Is DOMAIN_SEPARATOR recalculated or hardcoded? (hardcoded breaks on upgrade)
□ Are there any selfdestruct calls? (can brick proxy permanently)
```

### Kill Signals
- Contract is NOT upgradeable (no proxy pattern, no `upgradeTo`, no `initialize`)
- Implementation constructor calls `_disableInitializers()`
- `_authorizeUpgrade` has `onlyOwner` or equivalent
- Storage layout shows `__gap` arrays between version-specific variables

### Real Paid Examples

| Protocol | Payout | Bug |
|----------|--------|-----|
| Wormhole | $10M | Uninitialized UUPS proxy → anyone calls initialize() |
| Parity | $150M frozen | No access control on initWallet() in library |

---

## QUICK REFERENCE: Bug Class by Frequency

| Rank | Class | % Criticals | Flash Loan? | First Grep |
|------|-------|-------------|-------------|-----------|
| 1 | Accounting Desync | 28% | No | `totalSupply\|totalShares\|totalAssets` |
| 2 | Access Control | 19% | No | `function.*external` without modifier |
| 3 | Incomplete Path | 17% | Sometimes | `function update_\|function cancel` |
| 4 | Off-By-One | 22% Highs | No | `period\|epoch\|round.*[<>][^=]` |
| 5 | Oracle Manipulation | 12% | Yes | `latestRoundData\|getReserves\|slot0` |
| 6 | ERC4626 Vaults | Varies | Yes | `convertToShares\|totalAssets()` |
| 7 | Reentrancy | 8% | Sometimes | `\.call{value\|safeTransfer` before state |
| 8 | Flash Loan | 83% use it | Yes | Any spot price or governance vote |
| 9 | Signature Replay | 3% | No | `ecrecover\|ECDSA.recover` |
| 10 | Proxy/Upgrade | 2% | No | `function initialize\|_authorizeUpgrade` |

---

→ NEXT: [03-grep-arsenal.md](03-grep-arsenal.md)
