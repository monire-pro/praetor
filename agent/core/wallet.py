import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

class AgentWallet:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
        self.private_key = os.getenv("PRIVATE_KEY")
        self.account = self.w3.eth.account.from_key(self.private_key)
        self.treasury_address = os.getenv("TREASURY_ADDRESS")
        
        # Minimal ABI for the Treasury Contract
        self.treasury_abi = [
            {
                "inputs": [
                    {"internalType": "address", "name": "_token", "type": "address"},
                    {"internalType": "address", "name": "_to", "type": "address"},
                    {"internalType": "uint256", "name": "_amount", "type": "uint256"},
                    {"internalType": "string", "name": "_reason", "type": "string"}
                ],
                "name": "executePayment",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        self.treasury = self.w3.eth.contract(address=self.treasury_address, abi=self.treasury_abi)

    def pay(self, token_address, recipient, amount, reason):
        """
        Instructs the Treasury to pay someone.
        """
        print(f"💸 WALLET: Preparing payment of {amount} to {recipient} for '{reason}'...")
        
        # Build Transaction
        tx = self.treasury.functions.executePayment(
            token_address,
            recipient,
            self.w3.to_wei(amount, 'ether'),
            reason
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 500000,
            'gasPrice': self.w3.to_wei('20', 'gwei')
        })

        # Sign & Send
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"✅ WALLET: Payment Sent! Hash: {tx_hash.hex()}")
        return tx_hash.hex()