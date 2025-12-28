// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// A simple fake token so we can test on your computer
contract MockMNEE {
    string public name = "Mock MNEE";
    string public symbol = "MNEE";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;

    constructor() {
        // Mint 1,000,000 tokens to the deployer (You)
        totalSupply = 1000000 * 10**18;
        balanceOf[msg.sender] = totalSupply;
    }

    function transfer(address recipient, uint256 amount) external returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[recipient] += amount;
        return true;
    }
}