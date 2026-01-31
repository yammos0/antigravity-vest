from fastapi import APIRouter, HTTPException
from typing import List
from app.engine.calculator import signal_engine, TradeSignal
from app.services.unlocks import unlock_service
from app.services.onchain import onchain_service

router = APIRouter()

@router.get("/dashboard", response_model=List[TradeSignal])
async def get_dashboard_signals():
    """
    Get signals for upcoming major unlocks.
    """
    try:
        # 1. Get Events
        events = await unlock_service.get_next_major_unlocks(limit=5)
        
        signals = []
        for event in events:
            # 2. Check Onchain pressure
            # We assume token address is known or resolvable. Mocking for now.
            fake_addr = "0x123..." 
            pressure = await onchain_service.analyze_movement_to_cex(fake_addr)
            
            # 3. Generate Signal
            sig = await signal_engine.generate_signal(event, onchain_confidence=pressure)
            signals.append(sig)
            
        return signals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
