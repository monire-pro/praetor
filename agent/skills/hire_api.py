import time

def hire_data_provider_skill():
    """
    Simulates finding a data provider API and negotiating a price.
    Returns the provider's wallet address and cost.
    """
    # In a real app, this would query a marketplace API.
    # For now, we mock it.
    print("🔎 SKILL: Searching for available Data Providers...")
    time.sleep(1) 
    
    # Mock Provider (You can use one of the Hardhat accounts here)
    provider_address = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8" # Hardhat Account #1
    cost = 50 # 50 MNEE tokens
    
    print(f"🤝 SKILL: Found Provider '{provider_address}' asking {cost} MNEE.")
    return provider_address, cost