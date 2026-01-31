import httpx
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pydantic import BaseModel
from app.core.config import settings

class UnlockEvent(BaseModel):
    token_symbol: str
    unlock_date: datetime
    unlock_amount: float
    unlock_percent: float  # % of circulating supply
    is_cliff: bool
    source: str

class UnlockDataService:
    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=10.0)

    async def fetch_token_unlocks(self) -> List[UnlockEvent]:
        """
        Fetch data from TokenUnlocks.app API (Mocked for now as we don't have a real key in env)
        """
        # In a real scenario, we would use:
        # url = "https://api.tokenunlocks.app/v1/unlocks"
        # headers = {"Authorization": f"Bearer {settings.TOKEN_UNLOCKS_API_KEY}"}
        # response = await self.http_client.get(url, headers=headers)
        
        # Simulating data for development/demonstration
        return [
            UnlockEvent(
                token_symbol="ARB",
                unlock_date=datetime.now() + timedelta(days=2),
                unlock_amount=1_110_000_000,
                unlock_percent=18.5,
                is_cliff=True,
                source="TokenUnlocks"
            ),
            UnlockEvent(
                token_symbol="SUI",
                unlock_date=datetime.now() + timedelta(days=5),
                unlock_amount=34_000_000,
                unlock_percent=2.4,
                is_cliff=False,
                source="TokenUnlocks"
            )
        ]

    async def fetch_cryptorank_vesting(self, symbol: str) -> Dict:
        """
        Fetch vesting schedule from Cryptorank.
        """
        # url = f"https://api.cryptorank.io/v1/currencies/{symbol}/vesting"
        # headers = {"api-key": settings.CRYPTORANK_API_KEY}
        return {}

    async def get_next_major_unlocks(self, limit: int = 5) -> List[UnlockEvent]:
        # Aggregation logic would go here
        all_unlocks = await self.fetch_token_unlocks()
        # Filter for future events and sort by sooner dates
        future_unlocks = [u for u in all_unlocks if u.unlock_date > datetime.now()]
        future_unlocks.sort(key=lambda x: x.unlock_date)
        return future_unlocks[:limit]

    async def close(self):
        await self.http_client.aclose()

unlock_service = UnlockDataService()
