// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

// ==================== 靶场：缺失访问控制 ====================
// 已知漏洞：emergencyWithdraw 无 onlyOwner 限制，任何人可提取全部资金。
contract AccessControlVault {
    address public owner;
    mapping(address => uint256) public balances;

    constructor() {
        owner = msg.sender;
    }

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // BUG: 缺少 onlyOwner 修饰符
    function emergencyWithdraw() external {
        uint256 amount = address(this).balance;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");
    }

    receive() external payable {}
}
