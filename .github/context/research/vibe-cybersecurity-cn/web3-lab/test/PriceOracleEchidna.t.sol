// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import {PriceOracleManipulation} from "../src/PriceOracleManipulation.sol";

// ==================== Echidna 属性：预言机协议不亏空 ====================
// 属性：vault 余额 + 流通 token 按当前价折算 >= 全部用户投入。
// 操纵价格后低价买高价卖会破坏该不变量 -> 反例。
contract PriceOracleEchidna {
    PriceOracleManipulation public vault;
    uint256 public totalDeposits;
    uint256 public totalTokens;

    constructor() {
        vault = new PriceOracleManipulation();
        vault.setPrice(1 ether);
    }

    function buy() external payable {
        require(vault.price() > 0, "price zero");
        uint256 tokens = msg.value * 1e18 / vault.price();
        vault.buy{value: msg.value}();
        totalDeposits += msg.value;
        totalTokens += tokens;
    }

    function sell(uint256 amount) external {
        uint256 tokens = amount < totalTokens ? amount : totalTokens;
        uint256 proceeds = tokens * vault.price() / 1e18;
        vault.sell(tokens);
        totalTokens -= tokens;
        totalDeposits = totalDeposits >= proceeds ? totalDeposits - proceeds : 0;
    }

    function setPrice(uint256 newPrice) external {
        vault.setPrice(newPrice);
    }

    // 简化模型：token 负债按当前价折算，协议资金必须覆盖用户投入
    function echidna_test_solvent() public view returns (bool) {
        if (vault.price() > 1e36) {
            return false;
        }
        uint256 backing = totalTokens * vault.price() / 1e18;
        return address(vault).balance + backing >= totalDeposits;
    }

    // 属性：价格必须处于合理区间（任意 setPrice 操纵极端值即破坏）
    function echidna_test_price_reasonable() public view returns (bool) {
        uint256 p = vault.price();
        return p >= 1e6 && p <= 1e30;
    }

    receive() external payable {}
}
