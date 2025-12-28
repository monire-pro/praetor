import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
token_addr = os.getenv("MNEE_TOKEN_ADDRESS")
treasury_addr = os.getenv("TREASURY_ADDRESS")

# Minimal ABI for Transfer
abi = [{"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"}]
token = w3.eth.contract(address=token_addr, abi=abi)

print(f"💰 Sending 5000 MNEE to Treasury: {treasury_addr}")
tx = token.functions.transfer(treasury_addr, w3.to_wei(5000, 'ether')).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 200000,
    'gasPrice': w3.to_wei('10', 'gwei')
})
signed = w3.eth.account.sign_transaction(tx, os.getenv("PRIVATE_KEY"))
w3.eth.send_raw_transaction(signed.raw_transaction)
print("✅ Treasury Funded!")