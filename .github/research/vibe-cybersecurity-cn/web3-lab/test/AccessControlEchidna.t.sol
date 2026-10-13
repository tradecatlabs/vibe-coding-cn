// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {AccessControlVault} from "../src/AccessControlVault.sol";

// ==================== Echidna 属性：只有 owner 能紧急提款 ====================
// 属性：非 owner 调用 emergencyWithdraw 后 vault 余额不得减少。
// 缺失访问控制下任意 sender 可清空 vault -> 反例。
contract AccessControlEchidna {
    AccessControlVault public vault;
    bool public broken;

    constructor() {
        vault = new AccessControlVault();
    }

    function fund() external payable {
        vault.deposit{value: msg.value}();
    }

    function emergencyWithdraw() external {
        bool isOwner = msg.sender == vault.owner();
        uint256 before = address(vault).balance;
        vault.emergencyWithdraw();
        if (!isOwner && address(vault).balance != before) {
            broken = true;
        }
    }

    function echidna_test_emergency_only_owner() public view returns (bool) {
        return !broken;
    }

    receive() external payable {}
}
