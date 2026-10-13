// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

// ==================== 靶场：预言机操纵 ====================
// 已知漏洞：使用单池瞬时价格作为喂价，攻击者可闪贷操纵价格套利。
contract PriceOracleManipulation {
    uint256 public price;
    mapping(address => uint256) public balances;

    function setPrice(uint256 newPrice) external {
        // BUG: 价格可由任何人直接设置，无权限、无 TWAP
        price = newPrice;
    }

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // 用当前价格结算：价格被操纵时，套利者可低价买入高价卖出
    function buy() external payable {
        require(price > 0, "price not set");
        uint256 amount = msg.value * 1e18 / price;
        balances[msg.sender] += amount;
    }

    function sell(uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient");
        balances[msg.sender] -= amount;
        (bool ok, ) = msg.sender.call{value: amount * price / 1e18}("");
        require(ok, "transfer failed");
    }

    receive() external payable {}
}
