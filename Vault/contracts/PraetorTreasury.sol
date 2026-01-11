// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract PraetorTreasury is Ownable {
    constructor() Ownable(msg.sender) {}

    receive() external payable {}

    function withdraw(address _token, uint256 _amount) external onlyOwner {
        IERC20 token = IERC20(_token);
        require(token.balanceOf(address(this)) >= _amount, "Insufficient funds");
        token.transfer(msg.sender, _amount);
    }

    function getBalance(address _token) external view returns (uint256) {
        return IERC20(_token).balanceOf(address(this));
    }
}
