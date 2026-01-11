# 🛡️ PRAETOR_AGI — Autonomous Treasury Sentinel

> **A “Glass Cockpit” for autonomous AI agents to earn, spend, and manage MNEE stablecoin with real-time reasoning and human guardrails.**

![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-MVP-green)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![AI](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-magenta)
![Stablecoin](https://img.shields.io/badge/Stablecoin-MNEE-blue)

---

## 💡 Inspiration

We are witnessing the dawn of **Agentic Finance**.

AI models can write code and generate content, but they remain **economically paralyzed** — unable to pay for servers, purchase APIs, or manage real capital.

**PRAETOR_AGI** solves the **Trust Gap**.

It allows an AI to act as an **autonomous CFO**, earning and spending **MNEE stablecoin**, while operating inside a transparent **“Glass Cockpit”** where humans can **observe, understand, and override** every decision in real time.

---

## 🚀 What It Does

PRAETOR is not a chatbot — it is a **financial entity**.

1. **Autonomous Reasoning**  
   Powered by **Google Gemini 2.5 Flash**, the agent interprets natural-language goals  
   *(e.g. “Market this product to 100 users”)* and evaluates **cost vs ROI**.

2. **MNEE Treasury Management**  
   The agent controls a real on-chain wallet, treating **MNEE as scarce capital**.  
   Spending = cost. Receiving = revenue.

3. **The “Glass Cockpit”**  
   A real-time React dashboard streams:
   - Agent reasoning
   - Risk scores
   - Transaction hashes
   - Treasury balance

4. **Emergency Kill Switch**  
   A hard **ABORT** control instantly revokes signing permissions if the agent behaves unexpectedly.

---

## 🏗️ Architecture

The system mirrors a biological organism:

- **🧠 Brain (AI):** Google Gemini 2.5 Flash  
- **🦾 Body (Blockchain):** Web3.py + MNEE Smart Contract  
- **🧬 Nervous System (Backend):** FastAPI  
- **👁️ Eyes (Frontend):** React + Tailwind CSS  

```mermaid
graph TD
    User[Human Operator] -->|Sets Goal| Frontend
    Frontend[React Glass Cockpit] -->|WebSocket| Backend
    Backend[FastAPI Sentinel] <-->|JSON Decisions| Brain[Gemini 2.5 Flash]
    Backend -->|Tx Request| Blockchain[MNEE Smart Contract]
    Blockchain -->|Tx Hash / Balance| Backend
    Backend -->|Live Logs| Frontend
🛠️ Tech Stack
AI

Google Gemini 2.5 Flash (google-generativeai)

Backend

Python 3.10+

FastAPI

Uvicorn

Web3.py

Frontend

React (Vite)

Tailwind CSS

Lucide Icons

Blockchain

Ethereum (Mainnet / Local Fork)

MNEE Stablecoin

Deployment

Backend: Render

Frontend: Vercel

💻 Installation & Setup
Prerequisites

Node.js + npm

Python 3.9+

Google Gemini API Key

(Optional) Ethereum wallet private key

1️⃣ Clone the Repository
git clone https://github.com/your-username/praetor-agi.git
cd praetor-agi

2️⃣ Backend Setup (The Agent)
cd agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt


Create .env inside agent/:

GEMINI_API_KEY=your_google_ai_key
RPC_URL=https://mainnet.infura.io/v3/YOUR_ID
PRIVATE_KEY=your_wallet_private_key
TREASURY_ADDRESS=0x...
MNEE_TOKEN_ADDRESS=0x...


Run the backend:

uvicorn server:app --reload

3️⃣ Frontend Setup (The Glass Cockpit)
cd ../frontend
npm install
npm run dev


Open:
👉 http://localhost:5173

🛡️ Safety & Guardrails

PRAETOR enforces defense-in-depth:

System Prompt Constraints

MNEE is scarce

Risk tolerance < 7 / 10

Hard-Coded Limits

Any transaction > 500 MNEE is rejected, regardless of AI intent

Human Override

Manual kill switch at all times

🔮 Roadmap

🤝 Multi-Agent Swarms
CEO, CFO, and Risk Officer agents voting on actions

🏛️ DAO Treasury Controls
Community-governed budget caps

🚀 Mainnet Launch
Live MNEE vault with real capital

📄 License

Distributed under the MIT License.
See LICENSE for details.

Built with ❤️ for the MNEE × Google AI Hackathon


---

If you want, I can also:
- 🔥 Optimize this for **Devpost judging**
- 📊 Add an **Architecture Diagram image**
- 🧪 Add a **Demo / Screenshots** section
- 🏆 Rewrite it for **grant or accelerator review**

Just tell me.
