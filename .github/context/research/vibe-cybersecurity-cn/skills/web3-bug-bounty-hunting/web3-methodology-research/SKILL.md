---
name: web3-methodology-research
description: External research synthesis from Trail of Bits, SlowMist, ConsenSys, Immunefi, and Cyfrin. Use this for advanced audit methodology, Echidna/Medusa fuzzing setup, Slither custom detector writing, attack pattern deep dives, or the 4-phase learning roadmap.
---

# METHODOLOGY & RESEARCH SYNTHESIS

Sources: Trail of Bits, SlowMist, ConsenSys, Immunefi Web3 Security Library, Cyfrin Audit Course, Lido Audits Library, Nethermind PublicAuditReports.

---

## TRAIL OF BITS

### Their Toolset

| Tool | What It Does | When to Use |
|------|-------------|-------------|
| **Slither** | Static analysis for Solidity/Vyper | Always — run first |
| **Echidna** | Property-based fuzzer (write invariants, it breaks them) | Write 3-5 invariants before reading code |
| **Medusa** | Next-gen fuzzer, multi-core, parallel corpus | Deeper campaigns after Echidna |
| **Manticore** | Symbolic execution — confirms if a path is truly reachable | Specific PoC confirmation |
| **Halmos** | Symbolic unit testing — proves for ALL inputs | Math-heavy functions |

---

### Slither Commands

```bash
# Install
pip3 install slither-analyzer

# First pass — protocol overview
slither . --print human-summary
slither . --print contract-summary

# Targeted detectors
slither . --detect reentrancy-eth,reentrancy-no-eth,unchecked-lowlevel
slither . --detect arbitrary-send-erc20,controlled-delegatecall
slither . --detect uninitialized-state,uninitialized-storage
slither . --detect suicidal,controlled-array-length

# Visualization
slither . --print inheritance-graph
slither . --print function-summary
slither . --print call-graph

# Filtered run (skip tests and libs)
slither . --exclude-low --filter-paths "test|lib"
```

---

### Echidna Quick Start

```solidity
// Write invariants BEFORE fully reading the code
contract VaultInvariants {
    Vault vault;

    // Protocol should never owe more than it holds
    function echidna_solvency() public view returns (bool) {
        return vault.totalAssets() >= vault.totalDebt();
    }

    // Share math must be consistent
    function echidna_share_math() public view returns (bool) {
        return vault.balanceOf(address(this)) <= vault.totalSupply();
    }

    // cumulativeRewardPerShare only ever increases
    function echidna_reward_monotonic() public view returns (bool) {
        return vault.cumulativeRewardPerShare() >= lastRewardPerShare;
    }
}
```

```bash
echidna contracts/VaultInvariants.sol --contract VaultInvariants --test-mode assertion

# With config
echidna Test.sol --contract EchidnaTest --config echidna.yaml
```

```yaml
# echidna.yaml
testLimit: 50000
seqLen: 100
workers: 4
corpusDir: corpus/
```

---

### Medusa Setup

```bash
# Install
# github.com/crytic/medusa
go install github.com/crytic/medusa@latest

# Run (coverage-guided, multi-core)
medusa fuzz --config medusa.json

# medusa.json
{
  "fuzzing": {
    "workers": 4,
    "testLimit": 500000,
    "corpusDirectory": "corpus"
  }
}
```

Medusa vs Echidna: Medusa is faster on large contracts due to coverage-guided exploration. Use Echidna for first pass, Medusa for extended campaigns.

---

### Trail of Bits Audit Methodology

```
1. THREAT MODEL FIRST
   - What are the assets? (tokens, governance power, user funds)
   - What are the trust boundaries? (who can call what?)
   - What are the attack surfaces? (entry points, external calls)

2. STATIC ANALYSIS
   - Run Slither with all detectors
   - Examine SlithIR output for complex functions
   - Map ALL state variables and who can write them

3. WRITE INVARIANTS BEFORE READING EVERYTHING
   - "totalAssets >= totalDebt always"
   - "shares * pricePerShare == underlying always"
   - "user can always withdraw their full deposit"
   - Run Echidna. Watch it break them.

4. SYMBOLIC EXECUTION ON HIGH-VALUE PATHS
   - Use Manticore/Halmos for precise reachability confirmation
   - Confirms "can an attacker actually reach state X?"

5. MANUAL REVIEW — FOCUS ON
   - Business logic (not syntax — Slither caught that)
   - Economic invariants (is the math right under adversarial conditions?)
   - Access control (who can call what, when, with what params?)

6. DIFFERENTIAL TESTING
   - Compare against reference implementation
   - "Function A does X. Function B does the same thing differently. Why?"
   - The inconsistency IS the bug.
```

---

### Key Bug Classes From Real ToB Audits

**EVM / Solidity:**
```
REENTRANCY VARIANTS (still common)
- Cross-function: lock in depositA, reenter via depositB before state update
- Cross-contract: callback to attacker contract via safeTransfer
- Read-only: view function reads stale state during reentrant call
  (Curve $70M — most underestimated variant)

ROUNDING ERRORS
- Division before multiplication: (a / b) * c vs (a * c) / b
- Wrong rounding direction (should round up for safety, rounds down)
- Precision loss in sequential operations

WEAK FIAT-SHAMIR (ZK SYSTEMS — ToB IEEE S&P 2023)
- ZK proof prover can forge proofs if transcript not fully committed
- Missing: challenge must bind all public inputs
- Check: is the verifier challenge a hash of EVERYTHING the prover touches?

ACCESS CONTROL GAPS
- Function A has onlyOwner → sibling function B does NOT
- Emergency functions callable by non-emergency roles
- Initializer called after deployment without restrictions

UNSAFE UPGRADES
- Storage slot collision between proxy and implementation
- Uninitialized implementation contract (selfdestruct vector)
- delegatecall to address from storage (attacker controls target)

SIGNATURE REPLAY
- Missing nonce in signed message
- Missing chainId in signed message
- Missing contract address in signed message
```

**DeFi-Specific (from Uniswap, Frax, Reserve Protocol, Scroll audits):**
```
LIQUIDITY MATH EDGE CASES
- Integer overflow at extreme tick values (Uniswap V3 type)
- Rounding direction matters at boundary

ORACLE MANIPULATION
- TWAP too short → manipulable in same block
- Spot price used directly → 1-tx manipulation

L2 BRIDGE TRUST
- Message replay across chain reorgs
- Missing sequence number validation
- Finality assumptions wrong for specific L2
```

---

### The "Risk Accepted" Hunt

ToB's most valuable contribution to bug bounty hunting:

```
1. Find the audit report PDF for your target protocol
   (GitHub, protocol docs, "audits" page)

2. Search for "Risk Accepted" or "Acknowledged"

3. For each acknowledged finding:
   - Is the root cause still in the code? → grep to verify
   - Has any code been added AROUND the bug that creates new attack paths?
   - Is there a NEW function that has the same missing check?

4. This is valid because:
   - Protocol explicitly said "we won't fix this"
   - BUT: if new code makes it exploitable → that is a NEW bug
```

---

### ToB Grep Arsenal

```bash
# Weak Fiat-Shamir candidates (ZK verifiers)
grep -rn "keccak256\|hash\|challenge" contracts/ | grep -v "nonce\|chainId\|address(this)"

# Reentrancy: transfers before state updates
grep -rn "transfer\|safeTransfer\|call{value" contracts/ -B5 | grep -v "nonReentrant"

# Rounding direction
grep -rn "/ totalSupply\|/ totalAssets\|/ reserves\|/ shares" contracts/
# Then check: is result used for deposit (round down = safe) or withdraw (round up = safe)?

# Uninitialized proxy
grep -rn "initialize\|_disableInitializers\|initializer" contracts/
# Is implementation contract protected from direct initialization?

# Missing chainId in signatures
grep -rn "abi.encodePacked\|abi.encode" contracts/ | grep -v "chainId\|block.chainid"
```

---

### ToB Key Papers

| Paper | Why It Matters |
|-------|---------------|
| [Weak Fiat-Shamir Attacks](https://eprint.iacr.org/2023/691) | Breaks ZK proofs — critical if target uses ZK |
| [What are the Actual Flaws in Important Smart Contracts?](https://github.com/trailofbits/publications/blob/master/papers/smart_contract_flaws_fc2020.pdf) | Ground truth on real Solidity bugs |
| [Echidna: Effective, Usable, and Fast Fuzzing](https://github.com/trailofbits/publications/blob/master/papers/echidna_issta2020.pdf) | Master fuzzing methodology |

**Free Guides:**
```
Testing Handbook:            https://appsec.guide/
ZKDocs (ZK vulnerabilities): https://www.zkdocs.com/
Secure Smart Contracts:      https://secure-contracts.com/
```

---

## SLOWMIST LEARNING ROADMAP

### The 4-Phase Path

```
Phase 1: Foundation (1-3 months)         → Solidity + EVM + Ethernaut
Phase 2: DeFi Protocols & Real Hacks (2-4 months) → AMMs, lending, bridges + reproduce hacks
Phase 3: EVM Internals + Advanced (3-6 months)    → Storage, proxies, fuzzing, first contest
Phase 4: Multi-Chain + Specialization (ongoing)   → Pick your chain + live Immunefi bounties
```

---

### Phase 1: Foundation

**Blockchain Basics:**
- Ethereum accounts, transactions, blocks, gas
- Mempool: pending transactions, frontrunning mechanics
- Storage: world state, Merkle-Patricia trees, slot layout

**Solidity (Essential Level):**
- Data types, memory vs storage vs calldata vs stack
- Function visibility: public, external, internal, private
- Low-level: `call`, `delegatecall`, `staticcall`, `create`, `create2`
- Assembly (Yul): inline assembly, memory layout

**Key Resources:**
```
1. Solidity docs: docs.soliditylang.org (read ALL of it)
2. Cyfrin Updraft: free courses, beginner to advanced
3. "Mastering Ethereum" — Antonopoulos (Chapters 1–7)
4. Solidity by Example: solidity-by-example.org
```

**Practice:**
```
1. Ethernaut: ethernaut.openzeppelin.com — 30 challenges (complete ALL before Phase 2)
2. Capture The Ether: capturetheether.com — foundational math/crypto bugs
3. Damn Vulnerable DeFi: damnvulnerabledefi.xyz — do after Phase 2
```

**Phase 1 checkpoint:**
- [ ] Can write a Solidity contract without referencing docs
- [ ] Understand storage slot layout (slots, packing, mappings)
- [ ] Completed all Ethernaut challenges
- [ ] Can explain reentrancy, integer overflow, access control bugs verbally

---

### Phase 2: DeFi Protocols & Real Hacks

**Protocols to Understand Deeply (Tier 1 — composes with everything):**
```
1. Uniswap V2/V3 — AMM formula x*y=k, flash swaps, TWAP oracle
2. Aave V3 — aTokens, flash loans, health factor + liquidation
3. Compound V2/V3 — cTokens, borrow/supply rates
4. ERC4626 — shares vs assets, first depositor attack, rounding direction
```

**How to Study Real Hacks:**
```
1. Read the post-mortem (rekt.news, medium, blog)
2. Find the transaction on Etherscan
3. Trace on Phalcon/Tenderly
4. Find the PoC: git clone https://github.com/SunWeb3Sec/DeFiHackLabs
5. Run it: forge test -vvv --contracts src/test/YEAR-MONTH/HackName_exp.sol
6. Add comments explaining every line
```

**Hacks to Study (priority order):**
```
1.  Cream Finance (Oct 2021) — $130M — flash loan + price manipulation
2.  Euler Finance (Mar 2023) — $197M — donation attack + liquidation
3.  Mango Markets (Oct 2022) — $117M — self-oracle manipulation
4.  Nomad Bridge (Aug 2022) — $200M — zero-value as trusted root
5.  Beanstalk (Apr 2022) — $182M — flash loan governance
6.  Curve Finance (Jul 2023) — $70M — Vyper compiler reentrancy
7.  Wormhole (Feb 2022) — $320M — fake sysvar on Solana
8.  Balancer (Aug 2023) — $2M — read-only reentrancy
9.  Poly Network (Aug 2021) — $610M — arbitrary external call
10. Compound Governance (Sep 2022) — $150M — proposal bug
```

**Audit Reports to Read:**
```
Solodit (solodit.cyfrin.io)         — 50K+ findings, searchable
Code4rena (code4rena.com/reports)   — 700+ public reports
Sherlock (sherlock.xyz)             — all public after contest
github.com/trailofbits/publications
github.com/spearbit/portfolio
github.com/ConsenSys/Diligence-Audit-Reports
```

**Phase 2 checkpoint:**
- [ ] Can trace a real hack from post-mortem to running PoC
- [ ] Understand all 4 Tier-1 DeFi protocols
- [ ] Read 10+ audit reports, categorized findings by bug class
- [ ] Completed Damn Vulnerable DeFi challenges

---

### Phase 3: EVM Internals + Advanced Techniques

**Storage Layout:**
```
Every contract has 2^256 storage slots
- Slot 0: first state variable
- Mapping key at slot n: keccak256(abi.encode(key, n))
- Dynamic array at slot n: length at n, elements at keccak256(n) + i
- String < 32 bytes: packed in one slot
```

**Key Opcodes for Auditors:**
```
DELEGATECALL  — executes code in caller's context (storage collision risk)
STATICCALL    — cannot modify state (no writes, no events)
CREATE2       — deterministic address (front-running, same-address malice)
SELFDESTRUCT  — force-feeds ETH (breaks balance assumptions)
TSTORE/TLOAD  — transient storage (post-Cancun, cleared each tx)
```

**Proxy Patterns:**
```
Transparent Proxy: admin controls upgrades, user calls go to impl
UUPS (EIP-1822):   upgrade logic IN the implementation — protect _authorizeUpgrade()
Beacon Proxy:      all proxies point to Beacon — one upgrade changes ALL
```

**Symbolic Execution:**
```bash
pip install halmos
halmos --contract ContractName --function testSymbolic
# Proves/disproves invariants for ALL possible inputs (not just sampled)
```

**Phase 3 checkpoint:**
- [ ] Can calculate any storage slot manually
- [ ] Understand all 3 proxy patterns and their attack surfaces
- [ ] Can write Echidna fuzzing properties for any protocol
- [ ] First Code4rena/Sherlock contest submitted

---

### Phase 4: Specialization

**Choose one:**

| Track | Chain | Tools | Key Bugs |
|-------|-------|-------|----------|
| EVM DeFi | Ethereum, Arbitrum, Base | Slither, Echidna, Foundry | Accounting desync, oracle, reentrancy |
| Solana | Solana | Sec3 X-Ray, Trident, Soteria | Missing signer check, remaining_accounts |
| Cross-Chain Bridges | Any | Tenderly, Phalcon | Message replay, zero-value trusted root |
| ZK Systems | Any | Halmos, ZKDocs | Unsound constraints, missing range checks |
| Move (Sui/Aptos) | Sui, Aptos | Move Prover | Wrong ability annotations, missing capability |

**SlowMist's 8-Step Audit Methodology:**
```
1. Information Collection — docs, design, scope (exact commit hash)
2. Risk Item Sorting — list all fund-holding components, rank by TVL
3. Code Review (line by line) — track state changes, external calls, access control
4. Testing and Verification — run existing tests, write PoC for suspects
5. Security Testing (Automated) — Slither, Aderyn, Mythril
6. Discussion and Review — classify severity, remove false positives
7. Report Writing — use standard template, quantify impact in USD
8. Fix Review — re-audit after fixes, check for regressions
```

**SlowMist Security Checklist (Condensed):**
```
Arithmetic:
- [ ] Division before multiplication? (should multiply first)
- [ ] unchecked {} blocks with user input?
- [ ] Type casts (uint256 → uint128 → uint64)? Check each step.

Access Control:
- [ ] initialize() callable again? After deployment?
- [ ] Role assignment in constructor: complete? Missing any role?
- [ ] Two-step ownership transfer?

Reentrancy:
- [ ] All external calls follow CEI?
- [ ] nonReentrant on all token-transfer functions?
- [ ] Cross-function reentrancy: shared state between two functions?
- [ ] Read-only reentrancy: view function read during external call?

Business Logic:
- [ ] Token accounting: uses balanceBefore/After not amount for fee tokens?
- [ ] Rounding direction: who benefits from rounding? (should favor protocol)
- [ ] Complete paths: does EVERY exit path update ALL state?
- [ ] Sibling functions: do all have the same guards?

Oracle / Price:
- [ ] Is price from manipulable source (getReserves, slot0)?
- [ ] Chainlink: staleness check? Price > 0? Round completeness?
- [ ] TWAP window: > 30 minutes for lending/borrowing?
```

---

## CONSENSYS ATTACK PATTERNS

Source: github.com/ConsenSys/smart-contract-best-practices — the canonical reference for Solidity security.

---

### CEI Pattern (Most Important Rule)

**Checks → Effects → Interactions**

```solidity
function exampleFunction(uint256 amount) external {
    // CHECKS: validate all conditions
    require(amount > 0, "Zero amount");
    require(balances[msg.sender] >= amount, "Insufficient balance");

    // EFFECTS: update state BEFORE any external interaction
    balances[msg.sender] -= amount;
    totalBalance -= amount;

    // INTERACTIONS: external calls last
    (bool success,) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

When CEI is not enough: cross-function reentrancy. Function A modifies state partially, calls external, Function B reads the partial state. CEI in A doesn't protect B. Need `nonReentrant` on both.

---

### Reentrancy

```solidity
// VULNERABLE: external call before state update
function withdrawBalance() public {
    uint256 amount = userBalances[msg.sender];
    (bool success,) = msg.sender.call{value: amount}("");  // INTERACTION first
    require(success);
    userBalances[msg.sender] = 0;  // EFFECT too late
}

// SECURE: CEI order
function withdrawBalance() public {
    uint256 amount = userBalances[msg.sender];
    userBalances[msg.sender] = 0;  // EFFECT first
    (bool success,) = msg.sender.call{value: amount}("");  // INTERACTION second
    require(success);
}
```

**Grep:** `.call{value:` without `nonReentrant` and without preceding state update

---

### tx.origin (Always Invalid for Auth)

```solidity
// VULNERABLE
require(tx.origin == owner);  // phishable — tx.origin is the EOA, not msg.sender

// SECURE
require(msg.sender == owner);
```

**Grep:** `tx\.origin` — any use in auth checks is a finding

---

### Force-Feeding ETH (selfdestruct)

```solidity
// VULNERABLE: relies on address(this).balance for logic
require(address(this).balance == 0, "Must be empty");  // can be bypassed

// ATTACK:
contract ForceFeed {
    constructor(address target) payable {
        selfdestruct(payable(target));  // Force ETH in — no receive() needed
    }
}

// SECURE: track ETH explicitly
uint256 totalTrackedBalance;
function deposit() external payable {
    totalTrackedBalance += msg.value;  // never use address(this).balance directly
}
```

**Grep:** `address(this).balance` in require/assert or conditional logic

---

### DoS with Block Gas Limit

```solidity
// VULNERABLE: unbounded loop
function distributeRewards() external {
    for (uint256 i = 0; i < participants.length; i++) {
        payable(participants[i]).transfer(1 ether);  // attacker registers 1000 addresses → OOG
    }
}

// SECURE: pull payment pattern
mapping(address => uint256) public pendingRewards;

function claimReward() external {
    uint256 amount = pendingRewards[msg.sender];
    require(amount > 0);
    pendingRewards[msg.sender] = 0;
    payable(msg.sender).transfer(amount);
}
```

**Grep:** `for.*participants\|for.*users\|for.*holders` with `.transfer` or `.call` inside

---

### Delegatecall to Arbitrary Address

```solidity
// VULNERABLE: user controls target and data
function execute(address target, bytes calldata data) external {
    (bool success,) = target.delegatecall(data);
    // delegatecall uses THIS contract's storage → attacker can modify anything
}

// ATTACK: deploy malicious contract with same slot layout
// call: target.execute(maliciousImpl, abi.encodeCall(exploit, ()))
// → target.owner() now returns attacker's address
```

**Grep:** `delegatecall` where the address comes from user input (parameter, mapping, external call)

---

### Spot Oracle Price Manipulation

```solidity
// VULNERABLE: reads current pool price (flash-loan manipulable)
function getPrice(address token) external view returns (uint256) {
    (uint112 reserve0, uint112 reserve1,) = IUniswapV2Pair(pool).getReserves();
    return (reserve1 * 1e18) / reserve0;
}

// SECURE: TWAP (30-minute window)
uint32[] memory secondsAgos = new uint32[](2);
secondsAgos[0] = 1800;  // 30 minutes
secondsAgos[1] = 0;
(int56[] memory tickCumulatives,) = IUniswapV3Pool(pool).observe(secondsAgos);
// → cannot be manipulated in one transaction
```

---

### Division Precision Loss

```solidity
// WRONG: loses precision (divides first)
uint256 fee = (amount / 100) * feeRate;

// CORRECT: multiply before divide
uint256 fee = (amount * feeRate) / 100;

// ROUNDING DIRECTION:
// Collateral required: round UP (protects protocol)
uint256 collateral = Math.ceilDiv(loanAmount * collateralFactor, 100);

// Shares for deposit: round DOWN (user gets less — safe)
// Shares for withdrawal: round UP (user pays more — safe)
```

---

### Signature Malleability

```solidity
// VULNERABLE: raw ecrecover — two valid (v,r,s) exist for every signature
address signer = ecrecover(hash, v, r, s);

// SECURE: OpenZeppelin ECDSA — rejects malleable signatures (s in lower half only)
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
address signer = ECDSA.recover(hash, signature);
```

---

### ConsenSys Grep Arsenal

```bash
# Reentrancy
grep -rn "\.call{value:\|\.send(\|\.transfer(" contracts/ | grep -v "//\|test"

# tx.origin auth
grep -rn "tx\.origin" contracts/

# Timestamp dependence
grep -rn "block\.timestamp.*%" contracts/   # modulo = gameable
grep -rn "block\.timestamp.*==" contracts/  # exact equality = fragile

# Unchecked blocks
grep -rn "unchecked {" contracts/ -A 10

# Force-feed vulnerability
grep -rn "address(this)\.balance" contracts/ | grep -v "//\|test"

# Push payments (should be pull)
grep -rn "\.transfer(\|\.send(" contracts/ | grep "for\|while"

# Raw ecrecover
grep -rn "ecrecover(" contracts/ | grep -v "ECDSA"

# Delegatecall with user input
grep -rn "delegatecall(" contracts/ -B5
```

---

## IMMUNEFI VULNERABILITY LIBRARY

Source: github.com/immunefi-team/Web3-Security-Library — Immunefi's official vulnerability taxonomy.

### The 15 Vulnerability Classes

**Class 1: Access Control**
Missing or improperly implemented authorization. Sub-types: missing modifier, incorrect modifier (silent bypass), privilege escalation, unprotected initialization.
```bash
grep -rn "function.*public\|function.*external" contracts/ | grep -v "view\|pure"
# For each: does it have onlyOwner/onlyRole?
```

**Class 2: Arithmetic**
Integer overflow/underflow, precision loss, rounding errors, type truncation, ERC4626 first depositor.
```bash
grep -rn "unchecked {" contracts/ -A20
grep -rn "uint8(\|uint16(\|uint32(\|uint64(" contracts/  # truncations
```

**Class 3: Oracle Manipulation**
Spot price from AMM (getReserves, slot0), stale Chainlink (missing staleness check), single oracle, TWAP too short.
```bash
grep -rn "getReserves\|slot0\|latestAnswer\|latestRoundData" contracts/
# For latestRoundData: is updatedAt checked? Is price > 0?
```

**Class 4: Logic Errors**
Wrong operator (> vs >=), missing state update on one path, tautology, missing guard on sibling function.
```bash
grep -rn "[<>][^=]" contracts/ | grep "period\|epoch\|amount\|timestamp"
# For each: ask "what happens when these are equal?"
```

**Class 5: Reentrancy**
Classic, cross-function, read-only ($70M Curve), cross-contract, ERC721/ERC777 hooks.
```bash
grep -rn "\.call{value:\|safeTransfer\|onERC721Received" contracts/
```

**Class 6: Flash Loans**
Zero-cost capital: oracle manipulation, flash loan governance voting, ERC4626 share price inflation.
Key question: "If an attacker had unlimited capital for 1 transaction, what's the worst they could do?"
```bash
grep -rn "getReserves\|slot0" contracts/                  # flash-manipulable oracles
grep -rn "totalSupply\|balanceOf" contracts/ | grep "vote\|quorum"  # flash loan voting
```

**Class 7: Denial of Service**
Gas limit DoS, reverting push payment, block stuffing, forced revert in catch block, griefing via protocol state.
```bash
grep -rn "for.*\.length" contracts/ -A5 | grep "transfer\|send\|call"
```

**Class 8: Cryptography**
ECDSA malleability, missing chainId (cross-chain replay), missing nonce (same-chain replay), weak RNG, ZK proof always passes, missing circuit range check.
```bash
grep -rn "ecrecover(" contracts/                            # raw = malleable
grep -rn "chainId\|block\.chainid" contracts/               # cross-check with ecrecover
grep -rn "block\.timestamp.*random\|blockhash.*random" contracts/
```

**Class 9: Front-Running**
ERC20 approve race, EIP-2612 permit frontrun DoS, sandwich attacks (missing slippage), harvest frontrun.
```bash
grep -rn "minAmountOut\|minOut\|deadline" contracts/        # should be on all swaps
grep -rn "permit(" contracts/ | grep -v "try\|catch"        # permit without try/catch = frontrunnable
```

**Class 10: Token Standards**
Fee-on-transfer (amount received ≠ sent), rebasing (balances change without transfers), ERC777 reentrancy, non-reverting ERC20 (USDT).
```bash
grep -rn "transferFrom\|transfer(" contracts/               # safeTransfer used?
grep -rn "balanceOf(address(this))" contracts/
```
Key resource: github.com/d-xo/weird-erc20 — catalog of non-standard ERC20 behaviors

**Class 11: Upgrade Patterns**
Uninitialized implementation, storage slot collision, missing `_disableInitializers()`, UUPS `_authorizeUpgrade()` unprotected.
```bash
grep -rn "function initialize\|_disableInitializers\|initializer\|reinitializer" contracts/
grep -rn "_authorizeUpgrade" contracts/
# Does it have onlyOwner or equivalent?
```

**Class 12: Bridge Vulnerabilities**
Signature/message replay (missing nullifier), validator set manipulation, spoofed system accounts (Wormhole $320M), zero value as valid root (Nomad $200M).
```bash
grep -rn "verify\|processMessage\|executeTransaction" contracts/
grep -rn "messageHash\|nonce\|nullifier" contracts/
```

**Class 13: Governance**
Flash loan voting (no snapshot), low quorum manipulation, timelock bypass.
```bash
grep -rn "balanceOf\|getCurrentVotes" contracts/ | grep "vote\|proposal"
# Should be: getPastVotes(account, block.number - 1) not current balance
```

**Class 14: Randomness**
`block.timestamp % n`, `blockhash`, `keccak256(block.timestamp, msg.sender)` — all predictable/manipulable. Use Chainlink VRF or commit-reveal.
```bash
grep -rn "block\.timestamp.*%\|blockhash.*random\|keccak256.*block\." contracts/
```

**Class 15: MEV**
Sandwich attacks, JIT liquidity, back-running. Not a "bug" per se — design protocols to be MEV-resistant (slippage protection, private mempools, Dutch auction liquidations).

---

### Immunefi Bug Fix Reviews (Top 10)

```
1. Wormhole ($10M)       — uninitialized proxy
   immunefi.com/blog/wormhole-uninitialized-proxy-bugfix-review

2. Aurora ($6M)          — delegatecall balance bypass
   immunefi.com/blog/aurora-infinite-spend-bugfix-review

3. Polygon ($2.2M)       — missing balance/signature check
   immunefi.com/blog/polygon-lack-of-balance-check-bugfix-postmortem

4. Optimism ($2M)        — selfdestruct duplication

5. Notional ($1M)        — double-counted collateral

6. Balancer ($1M)        — ERC4626 rounding + flash swap

7. Beanstalk ($182M)     — flash loan governance
   immunefi.com/blog/beanstalk-insufficient-input-validation-bugfix-review

8. DFX Finance ($100K)   — 2-decimal rounding
   immunefi.com/blog/dfx-finance-rounding-error-bugfix-review

9. Alchemix ($28K)       — admin brick forced revert
   dacian.me/28k-bounty-admin-brick-forced-revert

10. APWine ($100K)       — incorrect delegation check
```

Full PoC repo: github.com/immunefi-team/bugfix-reviews-pocs
→ Each folder: `forge test -vvv --match-path test/CONTRACT_NAME*`

---

### Tool Matrix (Complete by Phase)

```
Phase 1 — Setup:
  Etherscan       → get source, ABI, constructor args, admin address
  DeFiLlama       → TVL, protocol type, chain
  Solodit         → search 50K+ findings by type/chain/severity

Phase 2 — Static Analysis:
  Slither         → reentrancy, access control, uninitialized vars
  Aderyn          → Foundry projects, generates markdown report
  Mythril         → symbolic execution, integer bugs
  Semgrep         → custom pattern matching

Phase 3 — Dynamic Analysis:
  Foundry         → fork testing, PoC execution
  Echidna         → stateful fuzzer, property violations
  Medusa          → coverage-guided, faster on large contracts
  Halmos          → symbolic — proves for ALL inputs

Phase 4 — On-Chain Investigation:
  Phalcon         → transaction tracer, full call tree, token flows
  Tenderly        → fork + simulate, replay with modified params
  Dedaub          → decompile unverified contracts
  Eigenphi        → MEV/arbitrage analytics
```

---

### CTF Resources (Practice Before Live Hunting)

```
Ethernaut (ethernaut.openzeppelin.com) — 30 challenges, browser-based
Damn Vulnerable DeFi (damnvulnerabledefi.xyz) — 17 DeFi-specific challenges
Capture The Ether (capturetheether.com) — math and crypto fundamentals
Paradigm CTF (github.com/paradigmxyz/paradigm-ctf-2023) — competition-grade
Immunefi Community Challenges (github.com/immunefi-team/community-challenges) — 7 challenges

Solana: Neodyme Solana Security Workshop (github.com/neodyme-labs/solana-security-workshop)
ZK: zkHack (zkhack.dev)
```

---

## CYFRIN AUDIT COURSE

Source: github.com/Cyfrin/security-and-auditing-full-course-s23 — Patrick Collins + Tincho. 8 sections, 8 real codebases.

### The 3-Phase Audit Process

```
PHASE 1 — INITIAL REVIEW
  0. Scoping       → exact commit hash, in-scope contracts, chains
  1. Reconnaissance → read ALL docs, prior audits, understand system
  2. Vulnerability Identification → find bugs
  3. Reporting     → write findings

PHASE 2 — PROTOCOL FIXES
  1. Protocol fixes issues
  2. Protocol retests

PHASE 3 — MITIGATION REVIEW
  1. Re-read the fixes
  2. Verify each fix addresses root cause
  3. Check for new bugs introduced by fix
  4. Reporting
```

Mitigation reviews pay well — fixes often introduce NEW bugs.

---

### Scoping Checklist (Before Reading Code)

```
□ Commit hash (exact — not just "main")
□ Repo URL and in-scope vs out-of-scope contracts
□ Solc version
□ Chains to deploy to (different chains have different opcodes)
□ Token types (ERC20, ERC721, ERC4626, rebasing, fee-on-transfer?)
□ Known issues (don't file these)
□ Roles (who can call what? Admin power scope?)
□ Test coverage: forge test → what's the coverage?
```

---

### The Tincho Methodology

```
1. READ THE DOCS FIRST
   - Don't touch code until you understand the protocol in plain English
   - What does it do? Who uses it? What are the assets?

2. START SMALL → GO LARGE
   - Begin with the simplest contracts first
   - Work up to the most complex

3. NOTE-TAKING IN-CODE
   - // @audit potential issue here
   - // @audit-ok verified safe
   - // @note important to remember

4. USE SOLIDITY METRICS
   - cloc . → count lines
   - Solidity Metrics (VSCode) → complexity score, inheritance graph
   - High complexity = more bugs per line
```

---

### Cyfrin Finding Format

```markdown
### [S-#] TITLE (Root Cause + Impact)

**Description:**
[What the code does wrong. Quote the specific line(s). Be exact.]

**Impact:**
[What an attacker can do with this. Quantify if possible.]

**Proof of Concept:**
[Working code or step-by-step. Without this it won't get paid.]

**Recommended Mitigation:**
[Exact fix. Show the diff if possible.]
```

**Title formula:** `[ROOT CAUSE] in [function name] allows [WHO] to [IMPACT]`

---

### Bug Class Map (8 Codebases)

| Section | Codebase | Bug Classes |
|---------|----------|-------------|
| 3 | PasswordStore | Access control, private data on-chain |
| 4 | Puppy Raffle | Reentrancy, weak RNG, arithmetic, DoS |
| 5 | TSwap | Invariant breaking, weird ERC20s |
| 6 | Thunder Loan | Proxy/storage collision, oracle manipulation |
| 7 | Boss Bridge | Signature replay, bridge hacks |
| 7.5 | MEV lesson | Frontrunning, sandwich attacks |
| 8 | Vault Guardians | Governance attack, flash loan voting |

---

### Key Bug Classes with Code

**Invariant Breaking (TSwap — AMM):**
```bash
# Write BEFORE reading all code:
function invariant_constantProduct() public {
    assertEq(
        tokenA.balanceOf(address(pool)) * tokenB.balanceOf(address(pool)),
        initialK
    );
}
```

**Storage Collision (Thunder Loan — Proxy):**
```bash
forge inspect ContractName storage-layout
# Compare storage layouts of proxy vs implementation
# Any variable sharing the same slot = storage collision
```

**Governance Attack (Vault Guardians):**
```solidity
// VULNERABLE: flash loan voting
function getVotes(address account) public view returns (uint256) {
    return token.balanceOf(account);  // current balance = flash-loanable
}

// FIXED: snapshot at proposal creation
// ERC20Votes.getPastVotes(account, block.number - 1)
```

**Weak RNG:**
```solidity
// VULNERABLE
uint256 winner = uint256(keccak256(abi.encodePacked(
    msg.sender, block.timestamp, block.difficulty
))) % players.length;

// FIXED: Chainlink VRF or commit-reveal
```

---

### Cyfrin Tools Reference

```bash
# Static analysis
slither .
aderyn .

# Code metrics (before reading)
cloc .

# Invariant testing config
# foundry.toml:
[invariant]
runs = 128
depth = 15
fail_on_revert = true

# Read any storage slot
cast storage 0xAddress SLOT_NUMBER --rpc-url $RPC_URL

# Decode calldata
cast 4byte-decode CALLDATA

# Check if address is contract
cast code 0xAddress --rpc-url $RPC_URL
```

---

### Severity Classification (CodeHawks / Cyfrin)

```
CRITICAL — Direct loss of funds, no preconditions, any user can trigger
HIGH     — Loss of funds or protocol core function broken, some preconditions
MEDIUM   — Loss of value or core function impaired, significant preconditions
LOW      — Best practice violation, minor loss, or theoretical
INFO/GAS — No security impact
```

**The Rekt Test (protocol should answer YES to all):**
```
□ All actors, roles, and privileges documented?
□ External services, contracts, and oracles documented?
□ Method to freeze/pause in emergency?
□ Plan for when you get hacked?
□ Off-chain monitoring for suspicious activity?
□ Bug bounty program?
□ Documented and tested incident response plan?
```

---

### Cyfrin Key Resources

```
CodeHawks (competitive audits):     https://codehawks.com
Solodit (searchable findings DB):   https://solodit.xyz
DeFiHackLabs:                       https://github.com/SunWeb3Sec/DeFiHackLabs
Weird ERC20 list:                   https://github.com/d-xo/weird-erc20
Cyfrin audit checklist (Hans'):     https://github.com/Cyfrin/audit-checklist
Solcurity:                          https://github.com/transmissions11/solcurity
SC Exploits Minimized:              https://github.com/Cyfrin/sc-exploits-minimized
```

---

## LIDO & NETHERMIND (Key Tools and Patterns)

### Lido Audits Library (34-lido-audits-library.md)

**Source:** github.com/lidofinance/audits — 100+ reports, 2020–2026. Protocol TVL: $20B+.

**Core strategy:** Every "Acknowledged" finding is a live bug in production.

```bash
# Download audit PDFs and extract acknowledged findings:
brew install poppler
pdftotext "AuditReport.pdf" - | grep -A 20 "Acknowledged\|Risk Accepted"

# Clone current code:
git clone https://github.com/lidofinance/lido-dao.git
git clone https://github.com/lidofinance/dual-governance.git
git clone https://github.com/lidofinance/community-staking-module.git
```

**Highest-signal acknowledged bugs (all present in production):**
- Certora V2: 4 High issues acknowledged
- Statemind V2: 1 Critical + 2 High acknowledged
- Oxorio V2 on-chain: 7 Major issues ALL acknowledged
- MixBytes CSM: 23 out of 41 issues acknowledged

**Recurring bug patterns across Lido audits:**
1. **Oracle report manipulation** — off-chain oracle data accepted without validation on `submitReportData()` input params
2. **Withdrawal queue accounting desync** — `requestWithdrawal()` and `finalize()` desynced, allows claiming more than deposited
3. **Staking Router module trust** — modules self-report validator counts, malicious module can misreport
4. **Access control on privileged functions** — admin functions callable during unexpected protocol states
5. **L2 Bridge without finality check** — bridge accepts messages without verifying L1 reorg-safe finality
6. **Dual Governance tiebreaker abuse** — tiebreaker activation bypasses veto state

**Lido grep arsenal:**
```bash
# Oracle
grep -rn "submitReportData\|handleConsensusReport" contracts/
# Withdrawal
grep -rn "finalize\|claimWithdrawal\|_finalize" contracts/
# CSM bond
grep -rn "getBondSummary\|penalize\|_chargeDepositFee" contracts/
# Dual Governance state machine
grep -rn "activateNextState\|_getDualGovernanceState" contracts/
# Functions missing pause check
grep -rn "whenNotPaused\|_requireNotPaused" contracts/ | wc -l
grep -rn "function.*external\|function.*public" contracts/ | grep -v "view\|pure" | wc -l
# If second >> first: functions missing pause protection
```

---

### Nethermind Audit Patterns (35-nethermind-audit-patterns.md)

**Source:** github.com/NethermindEth/PublicAuditReports — 166 audits, 428 total issues.
Protocols: Vana, Royco, Panoptic V2, Worldcoin (×11), Mellow (×7), ZkLend (×5), Lido ZK Oracle, and 50+ more.

**5 Critical Bug Classes (study these first):**

1. **Empty array bypass of state reset (Vana)** — state flag set after a loop that can be skipped by passing `[]`
   ```bash
   grep -rn "= true;" src/ -B10 | grep -B10 "for.*calldata"
   # Flag: flag = true after loop that could be empty
   ```

2. **Duplicate ID in batch operations (Vana)** — same ID passed twice → double credit
   ```bash
   grep -rn "function.*migrate\|function.*batch" src/ --include="*.sol" -A20
   # Missing: require(!seen[id]) inside loop
   ```

3. **Uninitialized cache variable (Royco)** — `cachedTotalAssets` starts at 0, first depositor gets all shares
   ```bash
   grep -rn "cached\|_cache\|Cache" src/ --include="*.sol"
   # Missing: = realValue in constructor OR if (cache == 0) init guard
   ```

4. **Unauthorized offer updates (Mangrove)** — `updateOffer()` has no `require(owner[id] == msg.sender)`
   ```bash
   grep -rn "function update\|function modify" src/ --include="*.sol"
   # If function takes ID but no owner check → critical
   ```

5. **Decimal precision mismatch (Panoptic V2)** — 6-decimal token in 18-decimal math rounds collateral to 0
   ```bash
   grep -rn "/ 1e18\|/ WAD\|/ 10\*\*18" src/ --include="*.sol"
   grep -rn "decimals()\|IERC20Metadata" src/ --include="*.sol"
   # / 1e18 present but decimals() NOT in same function = precision bug candidate
   ```

**Top recurring patterns (Medium/High, 9–18 instances each):**
- Cache sync desync — cache updated on deposit/withdraw but not on interest accrual
- Rounding direction favoring attacker — `mulDiv` with wrong `Rounding` enum
- ZK circuit input not range-checked — verifier passes but public input is unconstrained
- Epoch/period consistency gaps — reads `currentEpoch` but writes to `lastDistributedEpoch`
- Cross-token decimal hell in multi-asset vaults — sums 6-decimal and 18-decimal balances directly
- `try/catch { revert }` pattern — catch block that reverts permanently bricks user withdrawals
- Withdrawal queue invariant violation — `claimed <= claimable <= queued` not maintained

**Nethermind 5-minute critical scan:**
```bash
# 1. Empty-array state flag
grep -rn "= true;" src/ | grep -v "require\|assert\|if ("
# Then check if inside/after loop

# 2. Array deduplication missing
grep -rn "function.*batch\|function.*multi\|function.*bulk" src/ --include="*.sol" -A20

# 3. Uninitialized cache
grep -rn "uint256.*cached\|uint128.*cached" src/ --include="*.sol" -B5

# 4. Decimal mismatch
grep -rn "/ 1e18" src/ && grep -rn "6.*decimals\|USDC\|USDT" src/

# 5. Missing ownership check on update functions
grep -rn "function update.*Id\|function modify.*Id" src/ --include="*.sol"
```

**Highest-bounty protocols audited by Nethermind:**
- Worldcoin (×11 audits) — $50K–$2M Critical
- Lido ZK Oracle — $100K–$2M Critical
- ZkLend (×5) — $50K–$1M Critical
- Panoptic V2 — $50K–$1M Critical
- Eigenlayer — $100K–$2M Critical

---

→ NEXT: [07-live-hunt-ern.md](07-live-hunt-ern.md)
