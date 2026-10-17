// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ArithmeticOverflow} from "../src/ArithmeticOverflow.sol";

// ==================== Echidna 属性测试包装 ====================
// 属性：totalSupply 单调不减。unchecked 溢出会回绕破坏该属性，
// Echidna 应能找到使 mint 回绕的反例序列。
contract OverflowEchidna {
    ArithmeticOverflow public token;
    bool public overflowDetected;

    constructor() {
        token = new ArithmeticOverflow();
    }

    function mint(uint256 amount) public {
        uint256 before = token.totalSupply();
        token.mint(amount);
        if (token.totalSupply() < before) {
            overflowDetected = true;
        }
    }

    // 属性：任何 mint 后都不允许发生回绕
    function echidna_test_no_wrap_around() public view returns (bool) {
        return !overflowDetected;
    }
}
