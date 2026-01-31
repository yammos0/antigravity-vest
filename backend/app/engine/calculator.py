import numpy as np
from enum import Enum
from pydantic import BaseModel
from typing import Optional
from app.services.market_data import market_service
from app.services.unlocks import UnlockEvent

class SignalType(str, Enum):
    SHORT = "SHORT"
    AVOID = "AVOID"
    LONG_AFTER_DUMP = "LONG_AFTER_DUMP"

class TradeSignal(BaseModel):
    token: str
    signal: SignalType
    uis_score: float
    confidence: float
    expected_move_pct: float
    reason: str

class SignalEngine:
    async def calculate_uis(self, event: UnlockEvent, circulating_supply: float) -> float:
        """
        UIS = (unlock_percent * circulating_supply) / avg_daily_volume * volatility_factor * historical_dump_factor
        """
        symbol = event.token_symbol
        
        # 1. Fetch Market Data
        # We need historical volume for avg calc
        ohlcv = await market_service.get_ohlcv(symbol, limit=30)
        if ohlcv.empty:
            return 0.0 # Insufficient data
            
        avg_daily_volume = ohlcv['volume'].mean() * ohlcv['close'].mean() # Approximate USD volume
        if avg_daily_volume == 0:
            return 0.0

        # 2. Calculate Volatility Factor (ATR / Realized Volatility)
        # Simplified: Use StdDev of returns
        returns = ohlcv['close'].pct_change().dropna()
        volatility = returns.std()
        volatility_factor = 1.0 + (volatility * 10) # Scaling factor, baseline 1.0
        
        # 3. Historical Dump Factor
        # Hardcoded 1.1 for now, in real engine this comes from database of past unlocks
        historical_dump_factor = 1.1 
        
        # 4. Unlock Value
        # unlock_percent is passed from event (e.g. 18.5 for 18.5%), convert to decimal if needed, 
        # but formula implies raw magnitude. Let's assume ratio relative to daily volume is key.
        
        unlock_tokens = event.unlock_amount
        unlock_value_usd = unlock_tokens * ohlcv['close'].iloc[-1]
        
        # Revised Formula implementation based on "Pressure Ratio"
        # Pressure = Value of Unlock / Avg Daily Volume
        pressure_ratio = unlock_value_usd / avg_daily_volume
        
        uis = pressure_ratio * volatility_factor * historical_dump_factor
        return uis

    async def generate_signal(self, event: UnlockEvent, onchain_confidence: float = 0.0) -> TradeSignal:
        # Need to fetch circulating supply. For now assume we have it or fetch from API.
        # Placeholder: 1B for demo if not provided
        circulating_supply = 1_000_000_000 
        
        uis = await self.calculate_uis(event, circulating_supply)
        
        # Signal Logic
        # UIS > 1.2 -> SHORT
        # 0.7 - 1.2 -> AVOID
        # < 0.7 -> LONG_AFTER_DUMP
        
        signal_type = SignalType.AVOID
        expected_move = 0.0
        
        if uis > 1.2:
            signal_type = SignalType.SHORT
            expected_move = -5.0 - (uis * 2.0) # Simple linear model
        elif uis < 0.7:
            signal_type = SignalType.LONG_AFTER_DUMP
            expected_move = 5.0 + ((1/uis) * 1.0)
        else:
            signal_type = SignalType.AVOID
            expected_move = -1.0 # Slight dip expected usually
            
        # Confidence calculation
        # Base confidence 50%
        confidence = 50.0
        if event.is_cliff:
            confidence += 15.0
        
        # Onchain pressure adds confidence to Short
        if signal_type == SignalType.SHORT:
            confidence += (onchain_confidence * 20.0) # Up to +20% from onchain
            
        return TradeSignal(
            token=event.token_symbol,
            signal=signal_type,
            uis_score=round(uis, 2),
            confidence=min(confidence, 99.0),
            expected_move_pct=round(expected_move, 2),
            reason=f"UIS: {uis:.2f} (Pressure: High)"
        )

signal_engine = SignalEngine()
