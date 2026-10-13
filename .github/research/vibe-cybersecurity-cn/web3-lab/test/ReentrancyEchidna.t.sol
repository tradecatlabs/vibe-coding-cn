// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {ReentrancyVault} from "../src/ReentrancyVault.sol";

// ==================== Echidna 属性：重入不导致资不抵债 ====================
// 属性：vault 余额始终 >= 全部负债（balances 之和）。
// 重入漏洞下 withdraw 多付，vault 余额会跌破负债 -> 反例。
contract ReentrancyEchidna {
    ReentrancyVault public vault;
    uint256 public liabilities;
    bool public broken;

    constructor() {
        vault = new ReentrancyVault();
    }

    function deposit() external payable {
        vault.deposit{value: msg.value}();
        liabilities += msg.value;
        check();
    }

    function withdraw() external {
        vault.withdraw();
        check();
    }

    function check() internal {
        // 负债包括本合约全部余额（攻击路径下 balance 未随提款清零）
        if (address(vault).balance < liabilities) {
            broken = true;
        }
    }

    receive() external payable {
        // 重入：只要 vault 还付得起就继续提
        if (address(vault) == address(0)) {
            return;
        }
        uint256 owed = vault.balances(address(this));
        if (owed > 0 && address(vault).balance >= owed) {
            vault.withdraw();
        }
    }

    function echidna_test_no_insolvency() public view returns (bool) {
        return !broken;
    }
}
