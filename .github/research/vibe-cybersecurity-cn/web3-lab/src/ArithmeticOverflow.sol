// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

// ==================== 靶场：算术溢出 ====================
// 已知漏洞：unchecked 块内的乘法溢出，可绕过余额上限检查。
contract ArithmeticOverflow {
    uint256 public totalSupply;

    function mint(uint256 amount) external {
        unchecked {
            // BUG: 溢出回绕使 totalSupply 变小
            totalSupply += amount;
        }
    }

    function isOverLimit() external view returns (bool) {
        return totalSupply > 1_000_000;
    }
}
