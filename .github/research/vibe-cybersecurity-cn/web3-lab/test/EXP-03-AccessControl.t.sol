// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {Test} from "forge-std/Test.sol";
import {AccessControlVault} from "../src/AccessControlVault.sol";

// ==================== 缺失访问控制攻击验证 ====================
contract AccessControlTest is Test {
    function test_AnyoneCanEmergencyWithdraw() public {
        AccessControlVault vault = new AccessControlVault();
        // owner 存入 10 ETH
        vm.deal(address(this), 10 ether);
        vault.deposit{value: 10 ether}();

        // 任意第三方提取全部资金
        vm.deal(address(0xBAD), 1 ether);
        vm.prank(address(0xBAD));
        vault.emergencyWithdraw();

        assertEq(vault.balances(address(this)), 10 ether, "owner accounting broken");
        assertEq(address(0xBAD).balance, 11 ether, "attacker stole vault funds");
        assertEq(address(vault).balance, 0, "vault empty");
    }
}
