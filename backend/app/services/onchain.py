import httpx
from typing import List, Dict, Optional
from app.core.config import settings

class OnchainService:
    def __init__(self):
        # In production, use AsyncWeb3 from web3.py
        # For this architecture demo, using raw RPC calls via HTTPX is lighter
        self.rpc_url = f"https://eth-mainnet.g.alchemy.com/v2/{settings.ALCHEMY_API_KEY}"
        self.http_client = httpx.AsyncClient()
        
        # Known CEX Hot Wallets (Simplified List)
        self.cex_wallets = {
            "0x28C6c06298d514Db089934071355E5743bf21d60": "Binance 14",
            "0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549": "Binance 15",
            "0xf89d7b9c864f589bbf53a82105107622b35eaa40": "Bybit",
            # ... and so on
        }

    async def get_token_transfers(self, token_address: str, from_block: str = "latest"):
        """
        Fetch recent Transfer events for a token using eth_getLogs
        Topic0 for Transfer: 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
        """
        if not settings.ALCHEMY_API_KEY:
            # Mock if no key
            return []

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getLogs",
            "params": [{
                "address": token_address,
                "fromBlock": from_block,
                "toBlock": "latest",
                "topics": ["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"]
            }]
        }
        
        try:
            response = await self.http_client.post(self.rpc_url, json=payload)
            data = response.json()
            if "result" in data:
                return data["result"]
            return []
        except Exception as e:
            print(f"RPC Error: {e}")
            return []

    async def analyze_movement_to_cex(self, token_address: str, threshold: float = 100000.0) -> float:
        """
        Returns a 'pressure score' based on transfers to CEXs.
        0.0 = No pressure
        1.0 = High pressure (Big transfers to CEX)
        """
        logs = await self.get_token_transfers(token_address)
        pressure = 0.0
        
        for log in logs:
            # Parse 'to' address from topic[2] (padded 32 bytes)
            to_topic = log["topics"][2]
            to_address = "0x" + to_topic[26:] # Extract last 20 bytes
            
            if to_address in self.cex_wallets: # Case sensitivity needs handling in real code
                # Simplify: just increment pressure for demo
                pressure += 0.2
        
        return min(pressure, 1.0)

onchain_service = OnchainService()
