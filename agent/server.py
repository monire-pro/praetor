import os
import json
import asyncio
import time
import datetime
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

# TRY IMPORTING WEB3 - If this fails, the server will crash
try:
    from web3 import Web3
except ImportError:
    print("❌ CRITICAL ERROR: 'web3' library not found.")
    print("👉 Please run: pip install web3")
    exit(1)

# ==========================================
# 1. SETUP & BLOCKCHAIN CONFIG
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "history.json"

# --- BLOCKCHAIN SETTINGS ---
RPC_URL = "http://127.0.0.1:8545" # Hardhat Localhost
TREASURY_ADDRESS = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512" 
TOKEN_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

# Hardhat Account #0 (The Owner)
OWNER_ADDRESS = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

# Minimal ABI
TREASURY_ABI = [
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

app = FastAPI()

# ATTEMPT CONNECTION TO RPC
w3 = Web3(Web3.HTTPProvider(RPC_URL))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class Command(BaseModel):
    goal: str

# --- WEBSOCKET MANAGER ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"🟢 [WS] Client Connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"🔴 [WS] Client Disconnected.")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"⚠️ Send Error: {e}")
                # Clean up dead connections
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

manager = ConnectionManager()
log_stream: List[Dict] = []

async def add_log(tag: str, description: str):
    """Adds a log and BROADCASTS it via WebSocket instantly."""
    entry = {
        "timestamp": time.time(),
        "tag": tag,
        "description": description
    }
    log_stream.append(entry)
    if len(log_stream) > 100:
        log_stream.pop(0)
    
    # PUSH TO FRONTEND
    await manager.broadcast(entry)

def load_history():
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "balance": 0.0,
        "spent": 0.0,
        "revenue": 0.0,
        "net_profit": 0.0,
        "status": "IDLE",
        "history": [],
    }

def save_history(state):
    try:
        data_to_save = {
            "balance": state["balance"],
            "spent": state["spent"],
            "revenue": state["revenue"],
            "net_profit": state["net_profit"],
            "history": state["history"]
        }
        with open(HISTORY_FILE, "w") as f:
            json.dump(data_to_save, f, indent=4)
    except Exception as e:
        print(f"❌ Failed to save DB: {e}")

system_state = load_history()

# ==========================================
# 2. ROUTES (With PING)
# ==========================================

@app.get("/")
def read_root():
    """Root endpoint to quickly check if server is running in browser."""
    return {"message": "Praetor Prime Backend is ONLINE", "status": "active"}

@app.get("/ping")
def ping_server():
    """Dedicated Ping endpoint for the frontend."""
    return {"pong": True, "time": time.time()}

@app.get("/status")
def get_status():
    return system_state

@app.get("/logs")
def get_logs():
    return log_stream

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WS Error: {e}")
        manager.disconnect(websocket)

@app.post("/run-agent")
async def run_agent(command: Command):
    if system_state["status"] == "WORKING":
        return {"error": "Agent is busy"}
    
    system_state["status"] = "WORKING"
    asyncio.create_task(run_logic(command.goal))
    return {"message": "Agent started", "goal": command.goal}

# ==========================================
# 3. REAL BLOCKCHAIN LOGIC
# ==========================================

def execute_on_blockchain(amount_mock_mnee):
    """Synchronous function to sign and send tx via Web3"""
    try:
        if not w3.is_connected():
            return False, "Blockchain Offline"

        contract = w3.eth.contract(address=TREASURY_ADDRESS, abi=TREASURY_ABI)
        
        # 1. Convert amount
        amount_wei = w3.to_wei(amount_mock_mnee, 'ether')
        
        # 2. Build Transaction
        recipient = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8" # Hardhat Account #1
        nonce = w3.eth.get_transaction_count(OWNER_ADDRESS)
        
        tx = contract.functions.executePayment(
            TOKEN_ADDRESS,
            recipient,
            amount_wei,
            "Algorithmic Yield Farm Exec"
        ).build_transaction({
            'chainId': 31337, # Hardhat Chain ID
            'gas': 2000000,
            'gasPrice': w3.to_wei('1', 'gwei'),
            'nonce': nonce,
        })
        
        # 3. Sign
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        
        # 4. Send
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return True, receipt.transactionHash.hex()
    
    except Exception as e:
        return False, str(e)

async def run_logic(goal: str):
    try:
        await add_log("COMMAND", f"Received Directive: {goal}")
        await asyncio.sleep(1) 

        # 1. Check Blockchain Connection
        if w3.is_connected():
            block = w3.eth.block_number
            await add_log("INFO", f"Connected to Local Chain. Height: {block}")
        else:
            await add_log("ERROR", "Blockchain Unreachable. Is Hardhat running?")
            # We don't return here to allow simulation mode if chain is down
        
        steps = [
            ("PLANNING", "Scanning Treasury for available capital..."),
            ("RESEARCH", "Identifying MNEE liquidity pools..."),
            ("EXECUTION", "Broadcasting transaction to Hardhat Node...")
        ]

        for tag, desc in steps:
            await add_log(tag, desc)
            await asyncio.sleep(1.5)

        # 2. TRIGGER REAL TRANSACTION
        amount_to_move = 150.0 # MNEE
        
        loop = asyncio.get_running_loop()
        success, result = await loop.run_in_executor(None, execute_on_blockchain, amount_to_move)

        if success:
            tx_hash_short = f"{result[:6]}...{result[-4:]}"
            
            # Update UI State
            cost = 10.0
            revenue = 180.0
            profit = revenue - cost
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            system_state["balance"] += profit
            system_state["spent"] += cost
            system_state["revenue"] += revenue
            system_state["net_profit"] = system_state["revenue"] - system_state["spent"]
            
            new_record = {
                "id": len(system_state["history"]) + 1,
                "time": timestamp,
                "type": "ON_CHAIN_EXEC",
                "cost": cost,
                "revenue": revenue,
                "profit": profit
            }
            system_state["history"].insert(0, new_record)
            save_history(system_state)
            
            await add_log("SUCCESS", f"Confirmed on-chain: {tx_hash_short}")
            await add_log("FINANCE", f"Yield Harvested: +{profit} MNEE")
        else:
            await add_log("ABORT", f"Tx Failed: {result}")

    except Exception as e:
        print(f"❌ Error: {e}")
        await add_log("ERROR", f"System Crash: {str(e)}")
    
    finally:
        system_state["status"] = "IDLE"

if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0 is safer for avoiding localhost resolution issues on some machines
    uvicorn.run(app, host="127.0.0.1", port=8000)