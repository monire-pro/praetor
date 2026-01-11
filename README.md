```markdown
# 🛡️ PRAETOR_AGI: Autonomous Treasury Sentinel

> **A "Glass Cockpit" for autonomous AI agents to earn, spend, and manage MNEE stablecoin with real-time reasoning and human guardrails.**

![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-MVP-green)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![AI](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-magenta)
![Stablecoin](https://img.shields.io/badge/Stablecoin-MNEE-blue)

---

## 💡 Inspiration
We are witnessing the dawn of **Agentic Finance**. AI models can write code and generate art, but they remain "economically paralyzed"—unable to pay for servers, buy API keys, or invest in liquidity pools.

We built **PRAETOR_AGI** to solve the "Trust Gap." It allows an AI to act as an autonomous CFO—earning and spending **MNEE** stablecoin—while operating inside a transparent **"Glass Cockpit"** where a human can watch, understand, and override every decision in real-time.

## 🚀 What It Does
PRAETOR is not just a chatbot; it is a **financial entity** that lives on the blockchain.

1.  **Autonomous Reasoning:** Powered by **Google Gemini 2.5 Flash**, the agent analyzes natural language goals (e.g., *"Market this product to 100 users"*) and calculates cost vs. potential ROI.
2.  **MNEE Treasury Management:** The agent holds a real wallet balance in MNEE. It understands that spending MNEE is a "cost" and receiving MNEE is "revenue."
3.  **The "Glass Cockpit":** A real-time React dashboard that streams the agent's inner monologue, transaction hashes, and risk assessments to the human user.
4.  **Kill Switch:** A physical-style **ABORT** button that instantly revokes the agent's signing privileges if it starts "hallucinating" or taking excessive risks.

## 🏗️ Architecture

The system mimics a biological organism:

* **Brain (AI):** `Google Gemini 2.5 Flash` (Reasoning, Risk Assessment, Strategy).
* **Body (Blockchain):** `Web3.py` + `MNEE Smart Contract` (Execution, Wallet, Ledger).
* **Nervous System (Backend):** `FastAPI` (State management, bridging AI to Chain).
* **Eyes (Frontend):** `React` + `Tailwind` (Visualization, Human Control).

```mermaid
graph TD
    User[Human Operator] -->|Sets Goal| Frontend
    Frontend[React "Glass Cockpit"] -->|WebSocket| Backend
    Backend[FastAPI Sentinel] <-->|JSON Decision| Brain[Gemini 2.5 Flash]
    Backend -->|Tx Request| Blockchain[Ethereum / MNEE Contract]
    Blockchain -->|Tx Hash / Balance| Backend
    Backend -->|Live Logs| Frontend

```

## 🛠️ Tech Stack

* **AI:** Google Gemini 2.5 Flash (via `google-generativeai`)
* **Backend:** Python, FastAPI, Uvicorn, Web3.py
* **Frontend:** React, Vite, Tailwind CSS, Lucide Icons
* **Blockchain:** Ethereum Mainnet / Local Fork (Simulation), MNEE Stablecoin
* **Deployment:** Render (Backend), Vercel (Frontend)

---

## 💻 Installation & Setup

### Prerequisites

* Node.js & npm
* Python 3.9+
* A Google Gemini API Key
* (Optional) An Ethereum Wallet Private Key

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/praetor-agi.git](https://github.com/your-username/praetor-agi.git)
cd praetor-agi

```

### 2. Backend Setup (The Agent)

Navigate to the agent folder:

```bash
cd agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```

Create a `.env` file in the `agent/` folder:

```ini
GEMINI_API_KEY="your_google_ai_key"
RPC_URL="[https://mainnet.infura.io/v3/YOUR_ID](https://mainnet.infura.io/v3/YOUR_ID)" # Or use a local fork URL
PRIVATE_KEY="your_wallet_private_key"
TREASURY_ADDRESS="0x..." # Address of the MNEE vault or user wallet
MNEE_TOKEN_ADDRESS="0x..." # MNEE contract address

```

Run the backend:

```bash
uvicorn server:app --reload

```

### 3. Frontend Setup (The Cockpit)

Open a new terminal and navigate to the frontend folder:

```bash
cd ../frontend
npm install
npm run dev

```

Visit `http://localhost:5173` (or your local port) to see the PRAETOR Dashboard.

---

## 🛡️ Safety & Guardrails

PRAETOR implements a **"Dual-Check"** system:

1. **System Prompting:** The AI is explicitly instructed that *MNEE is scarce* and *Risk must be < 7/10*.
2. **Hard Coded Logic:** The Python backend rejects any transaction over **500 MNEE** automatically, regardless of what the AI "wants" to do.

## 🔮 What's Next?

* **Multi-Agent Swarms:** A "Board of Directors" where 3 agents (CEO, CFO, Risk Officer) vote on transactions.
* **DAO Integration:** Allowing a community to vote on the agent's budget cap.
* **Live Mainnet Launch:** Deploying the Vault contract to Ethereum Mainnet with real MNEE capital.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

*Built with ❤️ for the MNEE / Google AI Hackathon.*

```

```