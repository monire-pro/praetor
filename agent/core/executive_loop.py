# =====================================================
# STANDARD LIBS
# =====================================================
import os
from web3 import Web3

# =====================================================
# INTERNAL IMPORTS
# =====================================================
# Ensure these imports exist in your project structure
from agent.skills.hire_api import hire_data_provider_skill
from agent.skills.pay_vendor import pay_vendor_skill
from agent.core.llm import ask_gemini_decision
# We import AgentMemory just for type hinting or fallback
from agent.core.memory import AgentMemory 

# =====================================================
# EXECUTIVE BRAIN
# =====================================================
class ExecutiveBrain:
    def __init__(self, memory_ref=None):
        # ✅ FIX: Accept shared memory from server.py
        # If no memory provided (standalone mode), create a new one.
        self.memory = memory_ref if memory_ref else AgentMemory()

        # ---- ENV ----
        self.rpc_url = os.getenv("RPC_URL")
        self.token_address = os.getenv("MNEE_TOKEN_ADDRESS")
        # Support both naming conventions
        self.treasury_address = (
            os.getenv("PRAETOR_TREASURY_ADDRESS") or os.getenv("TREASURY_ADDRESS")
        )

        # ---- VALIDATION ----
        self._validate_env()

        # ---- LAZY INIT ----
        self._w3 = None

    # =================================================
    # ENV VALIDATION
    # =================================================
    def _validate_env(self):
        missing = []

        if not self.rpc_url:
            missing.append("RPC_URL")
        if not self.token_address:
            missing.append("MNEE_TOKEN_ADDRESS")
        if not self.treasury_address:
            missing.append("TREASURY_ADDRESS")

        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        # Checksum validation
        try:
            self.treasury_address = Web3.to_checksum_address(self.treasury_address)
        except Exception:
            raise RuntimeError("TREASURY_ADDRESS is not a valid Ethereum address")

        try:
            self.token_address = Web3.to_checksum_address(self.token_address)
        except Exception:
            raise RuntimeError("MNEE_TOKEN_ADDRESS is not a valid Ethereum address")

        print(f"✅ Treasury Address Loaded: {self.treasury_address}")

    # =================================================
    # WEB3 (LAZY LOAD)
    # =================================================
    @property
    def w3(self):
        if self._w3 is None:
            self._w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            if not self._w3.is_connected():
                raise RuntimeError("Failed to connect to RPC provider")
        return self._w3

    # =================================================
    # BALANCE CHECK
    # =================================================
    def get_balance(self) -> float:
        abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function",
            }
        ]

        try:
            contract = self.w3.eth.contract(
                address=self.token_address,
                abi=abi,
            )
            raw_balance = contract.functions.balanceOf(self.treasury_address).call()
            return float(self.w3.from_wei(raw_balance, "ether"))
        except Exception as e:
            print(f"💥 Blockchain Balance Error: {e}")
            # Log error to frontend too
            self.memory.add_thought("ERROR", f"Blockchain connection failed: {e}")
            return 0.0

    # =================================================
    # MAIN EXECUTION LOOP
    # =================================================
    def run(self, user_goal: str | None = None):
        """
        Executes the agent logic.
        Returns a dictionary with result details for the Server to process.
        """
        goal = (
            user_goal
            if user_goal and len(user_goal) > 2
            else "Acquire high-quality datasets."
        )

        self.memory.add_thought("PLANNING", f"Objective: {goal}")

        try:
            # 1. SEARCH
            self.memory.add_thought("SEARCHING", "Scanning data marketplaces...")
            
            # Call your skill (Ensure this returns valid data)
            provider, cost, product_name = hire_data_provider_skill(goal)

            vendor_info = (
                f"Provider {provider[:10]}... "
                f"offers '{product_name}' for {cost} MNEE"
            )

            # 2. THINK / ANALYZE
            current_balance = self.get_balance()
            self.memory.add_thought(
                "THINKING",
                f"Analyzing offer. Wallet: {current_balance} MNEE",
            )

            decision = ask_gemini_decision(
                goal,
                vendor_info,
                current_balance,
            )

            # 3. ACT / EXECUTE
            if decision["decision"] == "APPROVE":
                self.memory.add_thought(
                    "EXECUTING",
                    f"Approved: {decision['reason']}",
                )

                # Execute Transaction
                tx_hash = pay_vendor_skill(
                    provider,
                    decision["amount_to_pay"],
                    decision["reason"],
                )

                self.memory.add_thought(
                    "SUCCESS",
                    f"Payment Sent! Tx: {str(tx_hash)[:15]}...",
                )
                
                # Return Success Data to Server for the Dashboard
                return {
                    "status": "SUCCESS",
                    "cost": decision["amount_to_pay"],
                    "tx_hash": str(tx_hash),
                    "details": product_name
                }
                
            else:
                self.memory.add_thought(
                    "ABORT",
                    f"Rejected: {decision.get('reason')}",
                )
                return {"status": "ABORT", "reason": decision.get('reason')}

        except Exception as e:
            error_msg = f"System failure: {str(e)}"
            self.memory.add_thought("ERROR", error_msg)
            return {"status": "ERROR", "error": error_msg}