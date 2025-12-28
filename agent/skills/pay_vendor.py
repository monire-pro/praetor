# import os
# from web3 import Web3
# from dotenv import load_dotenv

# load_dotenv()

# def pay_vendor_skill(vendor_address, amount, reason):
#     # 1. Setup
#     rpc_url = os.getenv("RPC_URL")
#     private_key = os.getenv("PRIVATE_KEY")
#     treasury_address = os.getenv("TREASURY_ADDRESS") # <--- MUST BE HERE
    
#     w3 = Web3(Web3.HTTPProvider(rpc_url))
#     account = w3.eth.account.from_key(private_key)

#     # 2. Define the Treasury ABI (The 'executeTransaction' function)
#     # We assume your Treasury contract has a function like this:
#     # function executeTransaction(address to, uint256 value, bytes data)
#     treasury_abi = [
#         {
#             "inputs": [
#                 {"internalType": "address", "name": "_to", "type": "address"},
#                 {"internalType": "uint256", "name": "_amount", "type": "uint256"}
#             ],
#             "name": "payVendor", # CHECK YOUR SOLIDITY FUNCTION NAME!
#             "outputs": [],
#             "stateMutability": "nonpayable",
#             "type": "function"
#         }
#     ]

#     contract = w3.eth.contract(address=treasury_address, abi=treasury_abi)

#     # 3. Build Transaction
#     # We call the Treasury to pay the Vendor
#     amount_wei = w3.to_wei(amount, 'ether')
    
#     tx = contract.functions.payVendor(vendor_address, amount_wei).build_transaction({
#         'from': account.address,
#         'nonce': w3.eth.get_transaction_count(account.address),
#         'gas': 2000000,
#         'gasPrice': w3.to_wei('1', 'gwei')
#     })

#     # 4. Sign & Send
#     signed_tx = w3.eth.account.sign_transaction(tx, private_key)
#     tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
#     return w3.to_hex(tx_hash)

import os
from agent.core.wallet import AgentWallet

def pay_vendor_skill(vendor_address, amount, reason):
    wallet = AgentWallet()
    token_address = os.getenv("MNEE_TOKEN_ADDRESS")
    
    # Execute the payment logic
    tx_hash = wallet.pay(token_address, vendor_address, amount, reason)
    return tx_hash