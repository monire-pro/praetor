import os
import json
import threading
import time
import datetime
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

# ==========================================
# 1. SETUP & PERSISTENCE
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "history.json"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev
    allow_methods=["*"],
    allow_headers=["*"],
)

class Command(BaseModel):
    goal: str

# In-Memory Storage for Logs (The "Stream")
# This replaces the file writing to frontend/public
log_stream: List[Dict] = []

def add_log(tag: str, description: str):
    """Adds a log to the stream safely."""
    entry = {
        "timestamp": time.time(),
        "tag": tag,
        "description": description
    }
    log_stream.append(entry)
    # Keep only last 100 logs to save RAM
    if len(log_stream) > 100:
        log_stream.pop(0)

def load_history():
    """Loads financial stats from JSON file."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Corrupt DB, starting fresh: {e}")
    
    # Default State
    return {
        "balance": 1000.0, # Starting balance
        "spent": 0.0,
        "revenue": 0.0,
        "net_profit": 0.0,
        "status": "IDLE",
        "history": [],
    }

def save_history(state):
    """Saves current state to JSON file."""
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

# Initialize State
system_state = load_history()
system_state["status"] = "IDLE"

# ==========================================
# 2. ROUTES
# ==========================================

@app.get("/status")
def get_status():
    return system_state

@app.get("/logs")
def get_logs():
    return log_stream

@app.post("/run-agent")
def run_agent(command: Command):
    if system_state["status"] == "WORKING":
        return {"error": "Agent is busy"}
    
    system_state["status"] = "WORKING"
    
    # Run logic in a separate thread so API doesn't freeze
    thread = threading.Thread(
        target=run_logic,
        args=(command.goal,), 
        daemon=True,
    )
    thread.start()
    
    return {"message": "Agent started", "goal": command.goal}

# ==========================================
# 3. AGENT LOGIC (The Brain)
# ==========================================

def run_logic(goal: str):
    """
    Simulates the agent thinking, working, and transacting.
    """
    try:
        add_log("COMMAND", f"Received Directive: {goal}")
        time.sleep(1) # Fake processing time

        # --- SIMULATE STEPS (Replace this with your ExecutiveBrain later) ---
        
        steps = [
            ("PLANNING", "Analyzing market conditions for opportunity..."),
            ("RESEARCH", "Querying blockchain for liquidity pools..."),
            ("ANALYSIS", "Calculating risk/reward ratio..."),
            ("EXECUTION", "Initiating smart contract interaction...")
        ]

        for tag, desc in steps:
            add_log(tag, desc)
            time.sleep(1.5) # Simulate work duration

        # --- SIMULATE SUCCESS TRANSACTION ---
        
        # Determine Success (Mocking logic)
        is_success = True 
        
        if is_success:
            cost = 50.0 
            revenue = 125.0
            profit = revenue - cost
            
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            # 1. Update Global State
            system_state["balance"] = system_state["balance"] - cost + revenue
            system_state["spent"] += cost
            system_state["revenue"] += revenue
            system_state["net_profit"] = system_state["revenue"] - system_state["spent"]
            
            # 2. Create Ledger Entry
            new_record = {
                "id": len(system_state["history"]) + 1,
                "time": timestamp,
                "type": "YIELD_FARM",
                "cost": cost,
                "revenue": revenue,
                "profit": profit
            }
            
            # 3. Insert at TOP of list (newest first)
            system_state["history"].insert(0, new_record)
            
            save_history(system_state)
            
            add_log("SUCCESS", f"Transaction Finalized. Net Profit: +{profit}")
        else:
            add_log("ABORT", "Risk too high. Aborting operation.")

    except Exception as e:
        print(f"❌ Error: {e}")
        add_log("ERROR", f"System Crash: {str(e)}")
    
    finally:
        # Always reset status
        system_state["status"] = "IDLE"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)