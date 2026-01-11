import os
import json
import asyncio
import time
import datetime
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse, Response
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

RPC_URL = "http://127.0.0.1:8545"
TREASURY_ADDRESS = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512"
TOKEN_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

OWNER_ADDRESS = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

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

w3 = Web3(Web3.HTTPProvider(RPC_URL))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 🔥 GLOBAL PONG / HEALTH MIDDLEWARE
# ==========================================
@app.middleware("http")
async def pong_middleware(request: Request, call_next):
    # HEAD probes (load balancers / uptime checks)
    if request.method == "HEAD":
        return Response(status_code=200, headers={"X-Pong": "true"})

    # OPTIONS probes
    if request.method == "OPTIONS":
        return JSONResponse(
            content={"pong": True},
            headers={"X-Pong": "true"}
        )

    # ?ping=true on ANY endpoint
    if request.query_params.get("ping") == "true":
        return JSONResponse(
            content={
                "pong": True,
                "path": request.url.path,
                "time": time.time()
            },
            headers={"X-Pong": "true"}
        )

    response = await call_next(request)
    response.headers["X-Pong"] = "true"
    return response

# ==========================================
# MODELS
# ==========================================
class Command(BaseModel):
    goal: str

# ==========================================
# WEBSOCKET MANAGER
# ==========================================
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
        print("🔴 [WS] Client Disconnected.")

    async def broadcast(self, message: dict):
        for connection in self.active_connections[:]:
            try:
                await connection.send_json(message)
            except Exception:
                self.active_connections.remove(connection)

manager = ConnectionManager()
log_stream: List[Dict] = []

async def add_log(tag: str, description: str):
    entry = {
        "timestamp": time.time(),
        "tag": tag,
        "description": description
    }
    log_stream.append(entry)
    log_stream[:] = log_stream[-100:]
    await manager.broadcast(entry)

# ==========================================
# STATE PERSISTENCE
# ==========================================
def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
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
    HISTORY_FILE.write_text(json.dumps(state, indent=4))

system_state = load_history()

# ==========================================
# ROUTES
# ==========================================
@app.get("/")
def root():
    return {"message": "Praetor Prime Backend is ONLINE"}

@app.get("/ping")
def ping():
    return {"pong": True, "time": time.time()}

@app.get("/status")
def status():
    return system_state

@app.get("/logs")
def logs():
    return log_stream

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(ws)

@app.post("/run-agent")
async def run_agent(command: Command):
    if system_state["status"] == "WORKING":
        return {"error": "Agent busy"}
    system_state["status"] = "WORKING"
    asyncio.create_task(run_logic(command.goal))
    return {"message": "Agent started"}

# ==========================================
# BLOCKCHAIN EXECUTION
# ==========================================
def execute_on_blockchain(amount):
    try:
        if not w3.is_connected():
            return False, "Blockchain Offline"

        contract = w3.eth.contract(address=TREASURY_ADDRESS, abi=TREASURY_ABI)
        amount_wei = w3.to_wei(amount, "ether")
        nonce = w3.eth.get_transaction_count(OWNER_ADDRESS)

        tx = contract.functions.executePayment(
            TOKEN_ADDRESS,
            "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
            amount_wei,
            "Algorithmic Yield Farm Exec"
        ).build_transaction({
            "chainId": 31337,
            "gas": 2_000_000,
            "gasPrice": w3.to_wei("1", "gwei"),
            "nonce": nonce,
        })

        signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return True, receipt.transactionHash.hex()
    except Exception as e:
        return False, str(e)

async def run_logic(goal: str):
    try:
        await add_log("COMMAND", goal)
        await asyncio.sleep(1)

        if w3.is_connected():
            await add_log("INFO", f"Chain Height: {w3.eth.block_number}")
        else:
            await add_log("ERROR", "Blockchain Offline")

        for tag, msg in [
            ("PLANNING", "Scanning treasury"),
            ("RESEARCH", "Analyzing pools"),
            ("EXECUTION", "Submitting transaction"),
        ]:
            await add_log(tag, msg)
            await asyncio.sleep(1.5)

        loop = asyncio.get_running_loop()
        success, result = await loop.run_in_executor(None, execute_on_blockchain, 150.0)

        if success:
            await add_log("SUCCESS", f"TX Confirmed: {result[:8]}...")
        else:
            await add_log("ABORT", result)

    finally:
        system_state["status"] = "IDLE"

# ==========================================
# ENTRYPOINT
# ==========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
