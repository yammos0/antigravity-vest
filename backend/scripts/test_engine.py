import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from app.engine.calculator import signal_engine
from app.services.unlocks import unlock_service

async def main():
    print("--- Antigravity Engine Test ---")
    
    # 1. Fetch Mock Events
    print("Fetching Unlocks...")
    events = await unlock_service.get_next_major_unlocks()
    
    for event in events:
        print(f"\nAnalyzing {event.token_symbol} Unlock ({event.unlock_percent}% supply)...")
        
        # 2. Run Engine
        try:
            signal = await signal_engine.generate_signal(event, onchain_confidence=0.5)
            
            print(f"SIGNAL: {signal.signal.value}")
            print(f"CONFIDENCE: {signal.confidence}%")
            print(f"UIS SCORE: {signal.uis_score}")
            print(f"EXPECTED MOVE: {signal.expected_move_pct}%")
            
        except Exception as e:
            print(f"Error analyzing {event.token_symbol}: {e}")

    await unlock_service.close()
    # Close other services if needed (market_service auto-closes usually or needs explicit close)
    from app.services.market_data import market_service
    await market_service.close_all()

if __name__ == "__main__":
    asyncio.run(main())
