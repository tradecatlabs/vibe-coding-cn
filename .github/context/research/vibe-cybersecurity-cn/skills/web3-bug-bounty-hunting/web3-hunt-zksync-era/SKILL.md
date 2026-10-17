---
name: web3-hunt-zksync-era
description: ZKsync Era (Immunefi) completed hunt — 0 findings after exhaustive 5-session audit. Use as a DEFENSE STUDY — learn what makes a protocol unhuntable, which patterns block all 10 bug classes, and when to abandon a target. Contains architecture breakdown, 25 tested attack vectors, and pre-dive scoring refinements for large L1 bridge protocols.
---

# LIVE HUNT: ZKsync Era (Immunefi) — COMPLETED, 0 FINDINGS

> **Outcome**: 0 submittable findings after 5+ sessions, 22+ agents, 25+ contracts, 25+ attack vectors
> **Lesson**: This file exists as a DEFENSE STUDY — what a hardened protocol looks like, and when to stop hunting.

---

## TARGET PROFILE

| Field | Value |
|-------|-------|
| Protocol | ZKsync Era (L2 rollup) |
| Platform | Immunefi |
| TVL | $322M (L2BEAT Total Value Secured) |
| Bounty | $100K minimum Critical, $1.1M max |
| Codebase | 750K LOC (Solidity + Rust + Yul) |
| Audits | OpenZeppelin V29 (June 2025), multiple prior audits |
| Version | Protocol V29.4 |
| Repo | `github.com/matter-labs/era-contracts` |
| Primacy | Primacy of Impact — even out-of-scope assets qualify |
| Prior payouts | $50K (ChainLight ZK circuit bug) |

### Pre-Dive Scorecard

| Check | Result | Score |
|-------|--------|-------|
| TVL > $500K | $322M | PASS |
| Max payout > $10K | $100K minimum | PASS |
| Simple protocol? | 750K LOC, L1↔L2 bridge + ZK + governance | PASS (complex) |
| < 500 lines? | 750K LOC | PASS |
| **Audit quality** | OpenZeppelin (top-tier) on ALL critical paths | **WARNING** |

> **REFINEMENT**: Pre-dive should weight audit quality MORE for large protocols.
> A protocol passing TVL/LOC/payout checks can still be unhuntable if OZ/ToB audited the exact code you'd hunt.
> Add "audit firm tier" as a SOFT kill signal for 500K+ LOC protocols.

---

## ARCHITECTURE (What Makes It Hardened)

### L1 Bridge Stack
```
Bridgehub (router)
  ├── L1AssetRouter (token routing)
  │     ├── L1Nullifier (deposit/withdrawal state)
  │     └── L1NativeTokenVault (token custody)
  ├── ChainTypeManager (chain registration)
  └── ValidatorTimelock (RBAC execution delay)
```

### L2 System Contracts (kernel space 0x8000-0xFFFF)
```
Bootloader (0x8001) → AccountCodeStorage, NonceHolder, KnownCodeStorage,
ImmutableSimulator, ContractDeployer, L1Messenger (0x8008),
MsgValueSimulator, L2BaseToken (0x800a), SystemContext (0x800b),
BootloaderUtilities, Compressor, ComplexUpgrader
```

### L2 User Space Contracts (0x10000+)
```
Create2Factory, Bridgehub, AssetRouter, NativeTokenVault, MessageRoot
```

### Diamond Proxy Pattern (EIP-2535)
- All facets (Admin, Executor, Mailbox, Getters) share single `ZKChainStorage` struct
- No storage collision possible between facets
- Function selectors explicitly mapped in DiamondCut

---

## ALL 25 ATTACK VECTORS TESTED

### Critical Path (Vectors 1-8)

| # | Vector | Target | Why It Failed |
|---|--------|--------|---------------|
| 1 | UnsafeBytes offset miscalculation | L1Nullifier `_parseL2WithdrawalMessage` | All callers pre-validate message length before UnsafeBytes calls |
| 2 | Legacy/new boundary double-withdrawal | L1Nullifier | `_isLegacyTxDataHash` try/catch returns false on decode failure; encoding prefix discriminator prevents collision |
| 3 | `secondBridgeAddress` return value manipulation | Bridgehub `requestL2TransactionTwoBridges` | `>0xFFFF` check blocks system contracts; L2-side `msg.sender` auth makes crafted returns useless |
| 4 | Failed deposit claim wrong amount (legacy encoding) | L1Nullifier `claimFailedDeposit` | Legacy hash uses try/catch; `depositHappened` correctly tracks per-encoding-version |
| 5 | V29 interop root forgery | Executor | `addChainBatchRoot` requires `onlyChain + onlyL2`; historical roots verified via Merkle |
| 6 | Missing access control on sibling function | All bridge contracts | Every external function has appropriate modifier; checked all 50+ external functions |
| 7 | Fee-on-transfer token accounting desync | NativeTokenVault | L1ERC20Bridge: `if (amount != _amount) revert TokensWithFeesNotSupported()` |
| 8 | Governance timelock bypass | ValidatorTimelock | 5-role RBAC via AccessControlEnumerable; `block.timestamp >= commitTimestamp + delay` |

### Extended Surface (Vectors 9-25)

| # | Vector | Why It Failed |
|---|--------|---------------|
| 9 | GatewayTransactionFilterer bypass | Era mainnet: `transactionFilterer == address(0)`, not used |
| 10 | Precommitment sentinel collision | `_revertBatches` properly resets precommitment; sentinel values don't collide |
| 11 | L2→L1 message forgery via `sendToL1` | Anyone can call `sendToL1`, but L1 verifies `sender=0x8008` in log — can't forge system log sender |
| 12 | Compressor state diff manipulation | `publishCompressedBytecode` called only from bootloader context |
| 13 | Admin privilege escalation | Diamond proxy admin is governance; no facet can self-modify |
| 14 | Fee calculation overflow | All fee math uses SafeMath or checked arithmetic |
| 15 | Free L2 transaction abuse | `reservedDynamic` field properly handled; bootloader validates gas |
| 16 | DataEncoding L1/L2 mismatch | All 10 encode/decode pairs verified consistent across L1↔L2 |
| 17 | NTV token registration race | `_ensureTokenRegistered` is idempotent; double registration returns same assetId |
| 18 | Asset ID collision | `keccak256(chainId, ntvAddress, tokenAddress)` — no collision possible |
| 19 | Beacon proxy CREATE2 collision | Standard CREATE2; address determined by deployer+salt+bytecodeHash |
| 20 | Cross-contract reentrancy | Each contract has independent ReentrancyGuard AND follows CEI |
| 21 | Address aliasing collision | Bijective mapping (add/subtract offset mod 2^160) |
| 22 | Diamond proxy selector clash | Explicit selector mapping in DiamondCut; duplicates would revert |
| 23 | Priority tree manipulation | Merkle range proofs; `unprocessedIndex` only moves forward |
| 24 | Chain migration state corruption | `forwardedBridgeMint` validates consistency; atomic revert on mismatch |
| 25 | Cross-chain message replay | `isWithdrawalFinalized[chainId][batch][index]` prevents replay |

---

## WHY THIS PROTOCOL IS UNHUNTABLE (Solidity Surface)

### Defense Pattern 1: CEI Everywhere
```solidity
// L1Nullifier._finalizeDeposit (line 411)
isWithdrawalFinalized[chainId][l2BatchNumber][l2MessageIndex] = true; // EFFECT first
// ... then external call to NTV
```
Every single withdrawal/claim/deposit path follows Check-Effect-Interact.

### Defense Pattern 2: Independent Access Control on L2
Each L2 system contract independently enforces access:
- `L2BaseToken.transferFromTo`: checks `msg.sender` against 3 allowed callers
- `L1Messenger.sendToL1`: open to anyone, but L1 verifies sender field in log
- `SystemContext`: `onlyCallFromBootloader` on all state-changing functions
- No single RBAC failure cascades

### Defense Pattern 3: Encoding Collision Resistance
```
LEGACY_ENCODING_VERSION = 0x00  (first byte)
NEW_ENCODING_VERSION    = 0x01  (first byte)
```
Different first byte = impossible to confuse one format for another.

### Defense Pattern 4: Mature Legacy Boundary Handling
Three bridge generations coexist cleanly:
1. L1ERC20Bridge (legacy wrapper → delegates to AssetRouter)
2. L1SharedBridge (previous → absorbed into AssetRouter/Nullifier)
3. L1AssetRouter + L1Nullifier (current)

Each boundary has explicit version checks, try/catch decoding, and fallback paths.

### Defense Pattern 5: Audit Fix Quality
V29 OZ audit found 3 HIGHs. All fixes were thorough — not just patches but architectural improvements.
The "least audited code" assumption (that fixes are hastily applied) did NOT hold here.

---

## STRATEGIC TAKEAWAYS

### When to Abandon a Large L1 Bridge Target
1. After systematically testing top 8 attack vectors (Days 1-2): if all blocked, ROI drops exponentially
2. If OZ/ToB audited the EXACT codebase version you're reviewing (not an older version)
3. If 22+ automated agents all return clean across all contracts
4. If encoding, access control, and CEI are all consistently applied with zero exceptions

### What Could Still Work on ZKsync
1. **ZK circuits** (Rust/RISC-V) — different skillset, different attack surface, prior $50K payout proves bugs exist there
2. **Bootloader assembly** (Yul) — 5000+ lines of hand-written Yul, complex gas accounting, less audited
3. **New code drops** (V30+) — fresh code = fresh bugs. Monitor `era-contracts` releases
4. **EVM emulation edge cases** — `EvmGasManager`, EVM opcode compatibility gaps
5. **Interop protocol** (when launched) — `L2InteropRootStorage` is minimal now, but interop = massive new surface

### Pre-Dive Scoring Refinement
Add to the scorecard:
```
SOFT KILL: If protocol has OZ/ToB/Cyfrin audit on current version AND codebase > 500K LOC
           → expect 40+ hours for MAYBE 1 finding
           → only proceed if bounty floor > $50K AND you have protocol-specific expertise
```

---

> NEXT: [08-ai-tools.md](08-ai-tools.md)
