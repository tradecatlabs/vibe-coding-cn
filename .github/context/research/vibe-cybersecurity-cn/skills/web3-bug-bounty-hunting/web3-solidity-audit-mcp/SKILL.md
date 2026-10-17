---
name: web3-solidity-audit-mcp
description: MCP server integrating Slither + Aderyn + SWC patterns into Claude Code for smart contract auditing. Use when analyzing Solidity files, running DeFi-specific detectors, or generating invariants. 10 MCP tools, 86 SWC detectors, DeFi preset pack, CI/CD workflow.
---

# SKILL 36 — SOLIDITY AUDIT MCP: CLAUDE-NATIVE SMART CONTRACT SCANNER
> From: github.com/mariano-aguero/solidity-audit-mcp — MCP server plugging Slither + Aderyn + SWC patterns into Claude Code
> 10 tools. 19 built-in finding explainers. 86 SWC detectors. DeFi + Web3 preset detector packs. CI/CD ready.

---

## WHAT IT IS

An MCP server that gives Claude Code direct access to Slither, Aderyn, Slang AST, SWC pattern matching, and a gas optimizer — all in one unified pipeline with auto-deduplication. Instead of context-switching between tools, you ask Claude to audit a contract and get a merged, severity-sorted report.

**Stack:**
```
External (install separately):
  Slither   → Trail of Bits, 90+ detectors, deep data flow
  Aderyn    → Cyfrin Rust-based, fast AST analysis
  Echidna   → Property fuzzer (optional)
  Halmos    → Symbolic execution (optional)

Built-in (no install):
  Slang     → Nomic Foundation AST parser, precise pattern matching
  SWC       → 86 detectors against Smart Contract Weakness Classification registry
  Gas       → Storage packing, loop, calldata optimizations
```

---

## INSTALL & CONFIGURE

```bash
# Prerequisites
pip install slither-analyzer solc-select
solc-select install 0.8.20 && solc-select use 0.8.20
curl -L https://foundry.paradigm.xyz | bash && foundryup

# Aderyn (Rust)
cargo install aderyn
# or: curl -L https://raw.githubusercontent.com/Cyfrin/aderyn/dev/cyfrinup/install | bash

# MCP server
npm install -g solidity-audit-mcp
# or: npx solidity-audit-mcp

# Optional fuzzers
brew install echidna    # macOS
pip install halmos      # symbolic execution
```

**Wire into Claude Code** — add to `~/.claude/mcp.json`:
```json
{
  "mcpServers": {
    "audit": {
      "command": "npx",
      "args": ["solidity-audit-mcp"]
    }
  }
}
```

**Or project-level** `.mcp.json` in repo root:
```json
{
  "mcpServers": {
    "audit": {
      "command": "node",
      "args": ["/path/to/solidity-audit-mcp/dist/index.js"]
    }
  }
}
```

**Docker** (all tools pre-installed):
```bash
docker run -v $(pwd):/contracts solidity-audit-mcp audit /contracts/Token.sol
```

---

## THE 10 MCP TOOLS

### `analyze_contract` — Full Pipeline (Start Here)

```
analyze_contract(
  contractPath: "contracts/Vault.sol",
  analyzers: ["slither", "aderyn", "slang"],   # or omit for all
  runTests: true                                 # run forge tests too
)
```

**Pipeline:**
1. Parse metadata (functions, state vars, inheritance)
2. Run Slither + Aderyn in parallel
3. Detect risky patterns via Slang AST
4. Deduplicate findings across all tools
5. Sort by severity
6. Return unified report + JSON

### `get_contract_info` — Attack Surface Map (No Analysis)

```
get_contract_info("contracts/Protocol.sol")
```

Returns instantly:
- Functions by visibility (external, public, internal, private)
- Payable functions — all ETH entry points
- delegatecall usage — proxy risk surface
- State variables and modifiers
- Inheritance chain

**Use before full audit to understand the attack surface.**

### `check_vulnerabilities` — SWC Pattern Scan

```
check_vulnerabilities(
  contractPath: "contracts/Token.sol",
  detectors: ["SWC-107", "SWC-115", "CUSTOM-017"]  # or omit for all 86
)
```

**19 built-in finding explainers (full Foundry PoC + remediation):**

| ID | Finding | Severity |
|----|---------|---------|
| SWC-107 | Reentrancy | Critical |
| SWC-112 | Delegatecall to untrusted callee | Critical |
| CUSTOM-017 | Missing access control on critical function | Critical |
| CUSTOM-018 | ERC-7702 unprotected initializer | Critical |
| CUSTOM-004 | Price oracle manipulation / flash loan | Critical |
| CUSTOM-032 | ERC-4337 paymaster drain | Critical |
| SWC-101 | Integer overflow/underflow (unchecked) | High |
| SWC-104 | Unchecked call return value | High |
| SWC-115 | Authorization through tx.origin | High |
| CUSTOM-001 | Array length mismatch | High |
| CUSTOM-011 | Signature without replay protection | High |
| CUSTOM-029 | Merkle double-claim | High |
| SWC-116 | Block timestamp dependence | Medium |
| CUSTOM-005 | Missing zero address validation | Medium |
| CUSTOM-013 | Hash collision via abi.encodePacked | Medium |
| CUSTOM-015 | Division before multiplication | Medium |
| CUSTOM-016 | Permit without deadline | Medium |
| SWC-100 | Function default visibility | Medium |
| SWC-103 | Floating pragma | Low |

### `explain_finding` — Deep Dive on Any Finding

```
explain_finding(
  findingId: "CUSTOM-011",         # or "SWC-107", or keyword "reentrancy"
  contractContext: "ERC4626 vault with harvest callback"
)
```

Returns: root cause → impact → step-by-step exploit → vulnerable code → secure code → Foundry PoC template → remediation → references.

**Use this mid-hunt** when you find a suspicious pattern and want the full exploit scenario before writing a PoC.

**Supported keywords:** `reentrancy`, `overflow`, `flash loan`, `oracle`, `replay`, `nonce`, `encodepacked`, `precision loss`, `permit`, `access control`, `merkle`, `airdrop`, `erc-7702`, `paymaster`, `erc-4337`, `delegatecall`, `tx.origin`, `zero address`, `timestamp`

### `generate_invariants` — Auto-Generate Foundry Invariant Tests

```
generate_invariants(
  contractPath: "contracts/Vault.sol",
  protocolType: "vault"    # auto, erc20, erc721, vault, lending, amm, governance, staking
)
```

Returns ready-to-paste `invariant_*()` functions + handler contract + `forge test --invariant` run commands.

**Protocol-specific invariants generated:**
```
ERC-4626 vault:    totalAssets >= total share value
                   share price non-decreasing
                   deposit/withdraw round-trip solvency
Lending:           protocol solvency, liquidatable positions
AMM:               constant product k, no free lunch on swap
Staking:           reward monotonicity, total staked balance, slash accounting
Governance:        proposal state machine, quorum immutability
```

### `diff_audit` — Audit Only Changes

```
diff_audit(
  oldContractPath: "v1/Vault.sol",
  newContractPath: "v2/Vault.sol",
  focusOnly: true   # only report issues in changed code
)
```

Returns: functions added/removed/modified, new vulns introduced, issues resolved. Use on upgrade PRs.

### `audit_project` — Whole Directory

```
audit_project(
  projectRoot: "./contracts",
  exclude: ["node_modules/**", "test/**", "mocks/**"]
)
```

Aggregated findings across all .sol files + per-contract breakdown + project-level risk score.

### `optimize_gas` — Gas Analysis

```
optimize_gas("contracts/Protocol.sol", includeInformational: true)
```

Returns: storage packing opportunities, loop optimizations, calldata vs memory, visibility suggestions, estimated savings per change.

### `run_tests` — Forge Integration

```
run_tests(projectRoot: ".", contractName: "Vault")
```

Returns: pass/fail/skip counts, coverage %, gas report, execution time.

### `generate_report` — Formatted Output

```
generate_report(findings, contractInfo, format: "markdown", projectName: "Protocol")
```

Formats into: executive summary + risk level + findings table + remediation guidance.

---

## DeFi DETECTOR PRESET

The `defi.json` preset contains 10 high/medium severity DeFi-specific detectors:

```
oracle-manipulation      → HIGH  — spot price used, no TWAP, no staleness check
flash-loan-risk          → HIGH  — balance check before/after single tx
slippage-check           → HIGH  — swap with no minOut parameter
reentrancy-erc777        → HIGH  — ERC777 tokensReceived callback reentrancy
donation-attack          → HIGH  — totalAssets() uses balanceOf (inflatable)
price-stale-check        → HIGH  — Chainlink latestRoundData without check
unchecked-transfer       → MEDIUM — transfer/transferFrom return value ignored
precision-loss           → MEDIUM — division before multiplication
front-running-vulnerable → MEDIUM — state change in predictable order
liquidity-removal-risk   → MEDIUM — LP withdrawal without reserve check
```

**Load in Claude Code:**
```
analyze_contract("contracts/Vault.sol", analyzers: ["slither", "aderyn"], detectorPreset: "defi")
```

---

## CI/CD — GITHUB ACTIONS WORKFLOW

Drop this in `.github/workflows/audit.yml` to block PRs with Critical/High findings:

```yaml
name: Smart Contract Audit
on:
  pull_request:
    paths: ["**.sol"]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }

      - name: Install tools
        run: |
          pip install slither-analyzer solc-select
          solc-select install 0.8.28 && solc-select use 0.8.28
          ADERYN_VER=$(curl -sf https://api.github.com/repos/Cyfrin/aderyn/releases/latest | grep '"tag_name"' | sed -E 's/.*"([^"]+)".*/\1/')
          curl -fL "https://github.com/Cyfrin/aderyn/releases/download/${ADERYN_VER}/aderyn-x86_64-unknown-linux-gnu.tar.xz" | tar -xJf - -C /tmp
          sudo install -m 755 /tmp/aderyn /usr/local/bin/aderyn
          npm install -g solidity-audit-mcp

      - name: Audit changed contracts
        run: |
          # Get changed .sol files
          CHANGED=$(git diff --name-only origin/${{ github.base_ref }} | grep '\.sol$' || true)
          for f in $CHANGED; do
            solidity-audit-cli audit "$f" --severity-threshold high --format sarif --output results.sarif
          done

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with: { sarif_file: results.sarif }
```

**Exit codes for CI gates:**
```
0 → no findings above threshold → PR can merge
1 → findings detected → block PR
2 → execution error → investigate
```

---

## CLI USAGE (Outside Claude Code)

```bash
# Full audit
solidity-audit-cli audit ./contracts/Token.sol

# Filter severity
solidity-audit-cli audit ./contracts/Token.sol --severity-threshold high

# Different output formats
solidity-audit-cli audit ./contracts/Token.sol --format json
solidity-audit-cli audit ./contracts/Token.sol --format sarif --output results.sarif
solidity-audit-cli audit ./contracts/Token.sol --format markdown

# Compare versions
solidity-audit-cli diff ./v1/Token.sol ./v2/Token.sol

# Gas analysis
solidity-audit-cli gas ./contracts/Token.sol
```

---

## SAAS / REMOTE MODE

Run as a remote MCP server that any client connects to via SSE:

```bash
# Start
MCP_API_KEY=your-secret npm run saas:up  # → http://localhost:3000

# Configure client
{
  "mcpServers": {
    "audit": {
      "transport": "sse",
      "url": "http://your-server:3000/sse",
      "headers": { "Authorization": "Bearer your-secret" }
    }
  }
}

# Health check
GET /health  → { "tools": 10, "slither": {"available": true}, "aderyn": {"available": true} }
```

---

## ERN — SOLIDITY AUDIT MCP APPLIED

```
# STEP 1: Attack surface map before touching code
get_contract_info("contracts/ErnVault.sol")
→ lists: payable functions, delegatecall usage, external functions without modifiers

# STEP 2: Full pipeline with DeFi preset
analyze_contract(
  "contracts/ErnDistributor.sol",
  analyzers: ["slither", "aderyn", "slang"]
)
→ Slither will flag: DISTRIBUTOR_ROLE with no granted address
→ Aderyn will flag: unchecked return value in aToken.transfer()
→ SWC will flag: CUSTOM-017 missing access control on distributeRewards()

# STEP 3: Generate invariants for yield accounting
generate_invariants(
  "contracts/ErnVault.sol",
  protocolType: "vault"
)
→ Returns ready-to-paste Foundry invariant tests:
  invariant_totalAssetsGteDebt()        ← aToken balance >= totalDeposited
  invariant_sharePriceNonDecreasing()   ← cumulativeRewardPerShare only increases
  invariant_depositWithdrawRoundTrip()  ← user gets back what they put in

# STEP 4: Explain the signature replay finding in detail
explain_finding("CUSTOM-011", contractContext: "Ern distributor with off-chain signatures")
→ Returns: exploit scenario + vulnerable code + fixed code + Foundry PoC template

# STEP 5: Run invariant tests
run_tests(projectRoot: ".", contractName: "ErnVault")
→ Any invariant failure = confirmed Critical finding
```

---

→ NEXT: [00-START-HERE.md](00-START-HERE.md)
