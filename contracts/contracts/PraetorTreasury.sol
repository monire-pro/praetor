// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// Import security tools
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract PraetorTreasury {
    address public owner;     // The Agent (You)
    address public mneeToken; // The Currency

    event PaymentExecuted(address indexed to, uint256 amount, string reason);

    modifier onlyOwner() {
        require(msg.sender == owner, "NOT_AUTHORIZED: Only the Agent can spend funds.");
        _;
    }

    constructor(address _agent, address _mneeToken) {
        owner = _agent;
        mneeToken = _mneeToken;
    }

    // THIS is the function your Python script was trying to call
    function executePayment(
        address _token, 
        address _to, 
        uint256 _amount, 
        string memory _reason
    ) external onlyOwner {
        // 1. Check if Treasury has enough funds
        uint256 balance = IERC20(_token).balanceOf(address(this));
        require(balance >= _amount, "INSUFFICIENT_FUNDS: Treasury is empty!");

        // 2. Send the money
        bool success = IERC20(_token).transfer(_to, _amount);
        require(success, "TRANSFER_FAILED: Token transfer failed.");

        // 3. Log it on the blockchain
        emit PaymentExecuted(_to, _amount, _reason);
    }
}