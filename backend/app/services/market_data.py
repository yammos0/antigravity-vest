import ccxt.pro as ccxt  # Use Pro for potential WS upgrades, though standard async is base
import ccxt.async_support as ccxt_async
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd
from app.core.config import settings

class MarketDataService:
    def __init__(self):
        self.exchanges: Dict[str, ccxt_async.Exchange] = {}
        self._initialize_exchanges()

    def _initialize_exchanges(self):
        # Initialize connectors with rate limits enabled
        common_config = {
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'},  # Default to spot, can switch to future
        }

        # BINANCE
        self.exchanges['binance'] = ccxt_async.binance({
            **common_config,
            'apiKey': settings.BINANCE_API_KEY,
            'secret': settings.BINANCE_SECRET,
        })

        # BYBIT
        self.exchanges['bybit'] = ccxt_async.bybit({
            **common_config,
            'apiKey': settings.BYBIT_API_KEY,
            'secret': settings.BYBIT_SECRET,
        })

        # OKX
        self.exchanges['okx'] = ccxt_async.okx({
            **common_config,
            'apiKey': settings.OKX_API_KEY,
            'secret': settings.OKX_SECRET,
            'password': settings.OKX_PASSPHRASE,
        })

    async def close_all(self):
        for exchange in self.exchanges.values():
            await exchange.close()

    async def get_ohlcv(self, symbol: str, exchange_id: str = 'binance', timeframe: str = '1d', limit: int = 100) -> pd.DataFrame:
        """
        Fetch OHLCV data and seek the most liquid exchange if default fails.
        """
        exchange = self.exchanges.get(exchange_id)
        if not exchange:
            raise ValueError(f"Exchange {exchange_id} not initialized")

        try:
            # Ensure symbol format (e.g., BTC/USDT)
            formatted_symbol = symbol.upper()
            if '/' not in formatted_symbol:
                formatted_symbol = f"{formatted_symbol}/USDT"

            ohlcv = await exchange.fetch_ohlcv(formatted_symbol, timeframe, limit=limit)
            
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"Error fetching OHLCV for {symbol} on {exchange_id}: {e}")
            # Fallback logic could go here
            return pd.DataFrame()

    async def get_current_price(self, symbol: str, exchange_id: str = 'binance') -> float:
        exchange = self.exchanges.get(exchange_id)
        if not exchange:
            return 0.0
        
        try:
             # Ensure symbol format
            formatted_symbol = symbol.upper()
            if '/' not in formatted_symbol:
                formatted_symbol = f"{formatted_symbol}/USDT"
            
            ticker = await exchange.fetch_ticker(formatted_symbol)
            return ticker['last']
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return 0.0

    async def get_depth_liquidity(self, symbol: str, exchange_id: str = 'binance') -> dict:
        """
        Calculate simple liquidity metrics from orderbook.
        """
        exchange = self.exchanges.get(exchange_id)
        if not exchange:
            return {}
            
        try:
            formatted_symbol = symbol.upper()
            if '/' not in formatted_symbol:
                formatted_symbol = f"{formatted_symbol}/USDT"
            
            orderbook = await exchange.fetch_order_book(formatted_symbol, limit=20)
            
            # Simple aggregation of +/- 2% liquidity could be calculated here
            # For now returning raw top bids/asks
            return {
                "bids": orderbook['bids'],
                "asks": orderbook['asks'],
                "bid_volume_top_20": sum([b[1] for b in orderbook['bids']]),
                "ask_volume_top_20": sum([a[1] for a in orderbook['asks']])
            }
        except Exception as e:
            print(f"Error fetching depth for {symbol}: {e}")
            return {}

market_service = MarketDataService()
