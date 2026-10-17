// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

// ==================== 靶场：重入漏洞 ====================
// 已知漏洞：withdraw 未遵循 Checks-Effects-Interactions，
// 先转账再更新余额，可被恶意合约重入反复提取。
contract ReentrancyVault {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() external {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "no balance");
        // BUG: 外部调用先于状态更新（CEI 违反）
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");
        balances[msg.sender] = 0;
    }

    receive() external payable {}
}
