# API Reference — Tooling

## Slither (static analysis)

```bash
slither .                                  # whole project (reads foundry.toml + remappings)
slither . --json slither-report.json       # machine-readable
slither . --json -                          # JSON to stdout (used by agent.py)
slither . --print human-summary             # quick overview
slither . --print inheritance-graph         # inheritance / proxy layout
slither . --detect reentrancy-eth,unprotected-upgrade   # specific detectors
slither --list-detectors                    # all 90+ detectors
slither . --exclude-informational --exclude-low          # focus high/medium
slither . --triage-mode                     # interactively suppress false positives -> slither.db.json
```

Severity matrix (impact × confidence):

| Impact | Confidence | Example detectors |
|--------|------------|-------------------|
| High | High | `reentrancy-eth`, `suicidal`, `arbitrary-send-eth` |
| High | Medium | `controlled-delegatecall`, `reentrancy-no-eth` |
| Medium | High | `locked-ether`, `incorrect-equality`, `tx-origin` |
| Medium | Medium | `uninitialized-state`, `shadowing-state`, `unchecked-transfer` |
| Low | High | `naming-convention`, `solc-version`, `low-level-calls` |
| Informational | High | `pragma`, `dead-code`, `assembly` |

## Aderyn (Cyfrin, Rust static analyzer — complementary to Slither)

```bash
aderyn .                                    # markdown report.md by default
aderyn . -o aderyn-report.json              # JSON (used by agent.py)
aderyn . --scope src/                       # limit scope
```

## Mythril (symbolic execution — slow, use on critical contracts only)

```bash
myth analyze src/Vault.sol -o json
myth analyze src/Vault.sol --execution-timeout 300 --max-depth 50 -o json
myth analyze --address 0x... --rpc <url>    # deployed bytecode (read-only)
```

## Foundry — testing

```bash
forge build                                 # required before static analysis
forge test -vvv                             # unit + fuzz; -vvvv shows traces
forge test --match-contract VaultTest
forge test --match-test invariant_          # invariant suite only
forge coverage --report summary             # line/branch coverage table
forge coverage --report lcov                # for CI / tooling
forge snapshot                              # gas snapshots (DoS-by-gas review)
forge fmt --check                           # style gate
```

### Fuzz test (property over random inputs)

```solidity
function testFuzz_SetNumber(uint256 x) public {
    counter.setNumber(x);
    assertEq(counter.number(), x);
}
```

### Revert test (replaces deprecated testFail)

```solidity
function test_RevertWhen_Unauthorized() public {
    vm.prank(attacker);
    vm.expectRevert("Not authorized");   // or vm.expectRevert(MyError.selector)
    target.adminOnly();
}
```

### Key cheatcodes (`vm.*`)

| Cheatcode | Use |
|-----------|-----|
| `vm.prank(addr)` / `vm.startPrank` | impersonate caller (test access control) |
| `vm.warp(ts)` / `vm.roll(n)` | manipulate `block.timestamp` / `block.number` |
| `vm.deal(addr, amt)` | set ETH balance |
| `vm.store(addr, slot, val)` | overwrite storage (test invariants under hostile state) |
| `vm.expectRevert(...)` | assert a call reverts (with msg / custom error selector) |
| `vm.expectEmit(...)` | assert events |
| `bound(x, lo, hi)` | constrain fuzz inputs in handlers |
| `makeAddr("name")` | deterministic labelled actor |

### Invariant testing — handler pattern (the important one)

A handler wraps the target, **bounds inputs**, rotates **actors**, and tracks
**ghost variables**; `targetContract(handler)` makes the fuzzer drive only the
handler so sequences stay realistic.

```solidity
// test/Invariant.t.sol
contract VaultInvariantTest is Test {
    Vault vault;
    VaultHandler handler;

    function setUp() public {
        vault = new Vault();
        handler = new VaultHandler(vault);
        targetContract(address(handler));         // fuzz the handler, not the vault directly
    }

    function invariant_ConservationOfDeposits() public view {
        assertEq(address(vault).balance,
                 handler.ghost_depositSum() - handler.ghost_withdrawSum());
    }
    function invariant_Solvency() public view {
        assertGe(address(vault).balance, vault.totalDeposits());
    }
}
```

```solidity
// test/handlers/VaultHandler.sol
contract VaultHandler is Test {
    Vault public vault;
    uint256 public ghost_depositSum;
    uint256 public ghost_withdrawSum;
    address[] public actors;
    address internal currentActor;

    modifier useActor(uint256 seed) {
        currentActor = actors[bound(seed, 0, actors.length - 1)];
        vm.startPrank(currentActor); _; vm.stopPrank();
    }
    constructor(Vault _v) {
        vault = _v;
        for (uint256 i; i < 10; i++) { actors.push(makeAddr(string(abi.encodePacked("actor", i)))); vm.deal(actors[i], 100 ether); }
    }
    function deposit(uint256 amt, uint256 seed) external useActor(seed) {
        amt = bound(amt, 0.01 ether, 10 ether);
        vault.deposit{value: amt}(); ghost_depositSum += amt;
    }
    function withdraw(uint256 amt, uint256 seed) external useActor(seed) {
        uint256 bal = vault.balanceOf(currentActor);
        if (bal == 0) return;
        amt = bound(amt, 1, bal);
        vault.withdraw(amt); ghost_withdrawSum += amt;
    }
}
```

Tune in `foundry.toml`:

```toml
[invariant]
runs = 256
depth = 128
fail_on_revert = false   # set true once the handler fully constrains inputs

[fuzz]
runs = 10000
```

## SWC Registry (key entries)

| SWC | Title | Detected by |
|-----|-------|-------------|
| SWC-101 | Integer Overflow/Underflow | Mythril (pre-0.8 only) |
| SWC-104 | Unchecked Call Return | Slither + Mythril |
| SWC-105 | Unprotected Ether Withdrawal | Slither + Mythril |
| SWC-106 | Unprotected SELFDESTRUCT | Slither + Mythril |
| SWC-107 | Reentrancy | Slither + Mythril |
| SWC-112 | Delegatecall to Untrusted Callee | Slither |
| SWC-114 | Transaction Order Dependence (front-running) | manual |
| SWC-115 | tx.origin Authentication | Slither |
| SWC-116 | Block Timestamp Dependence | Mythril |
| SWC-120 | Weak Randomness | Slither + manual |

## References
- Slither: https://github.com/crytic/slither
- Aderyn: https://github.com/Cyfrin/aderyn
- Mythril: https://github.com/Consensys/mythril
- Foundry Book: https://getfoundry.sh/
- SWC Registry: https://swcregistry.io/
- Solidity security: https://docs.soliditylang.org/en/latest/security-considerations.html
- Solodit (audit findings DB): https://solodit.xyz/
