// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {Test} from "forge-std/Test.sol";
import {ArithmeticOverflow} from "../src/ArithmeticOverflow.sol";

// ==================== 算术溢出攻击验证 ====================
contract OverflowTest is Test {
    function test_UncheckedOverflowWraps() public {
        ArithmeticOverflow token = new ArithmeticOverflow();
        // 单次铸造超过 uint256 上限的一半，unchecked 内回绕
        token.mint(type(uint256).max);
        token.mint(1);
        // 总供应回绕为 0，绕过 100 万上限检查
        assertEq(token.totalSupply(), 0, "supply wrapped to zero");
        assertFalse(token.isOverLimit(), "over-limit check bypassed");
    }
}
