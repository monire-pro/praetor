# =====================================================
# STANDARD LIBS
# =====================================================
import os
import json
from google import genai

# =====================================================
# GEMINI CLIENT (LAZY + SAFE)
# =====================================================
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing")

    return genai.Client(api_key=api_key)

# =====================================================
# DECISION MAKER
# =====================================================
def ask_gemini_decision(goal, vendor_info, current_balance):
    """
    Sends the current situation to Gemini and asks for a JSON decision.
    """

    prompt = f"""
You are an Autonomous Treasury Agent responsible for buying AI training data.

CURRENT SITUATION:
- Your Goal: {goal}
- Your Wallet Balance: {current_balance} MNEE tokens
- Vendor Offer: {vendor_info}

INSTRUCTIONS:
1. Evaluate if the vendor's offer is fair and if you can afford it.
2. Respond STRICTLY in JSON format. Do not write any other text.

REQUIRED JSON FORMAT:
{{
    "decision": "APPROVE" or "REJECT",
    "reason": "Short explanation of why",
    "amount_to_pay": number (or 0 if rejected)
}}
"""

    try:
        client = get_gemini_client()

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        clean = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(clean)

    except Exception as e:
        print(f"❌ GEMINI DECISION ERROR: {e}")
        return {
            "decision": "REJECT",
            "reason": f"LLM failure: {str(e)}",
            "amount_to_pay": 0,
        }
