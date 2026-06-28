import yfinance as yf
from typing import List
from app.domain.candle import Candle
from app.infrastructure.providers.base import BaseDataProvider
from datetime import datetime

class YahooFinanceProvider(BaseDataProvider):
    async def fetch_candles(self, symbol: str, timeframe: str, limit: int = 100) -> List[Candle]:
        ticker_symbol = self._map_symbol(symbol)
        interval = self._map_timeframe(timeframe)
        
        # Usar um período maior para garantir que tenhamos o 'limit' de candles
        period = "1mo" if timeframe in ["1h", "4h"] else "5d"
        
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period=period, interval=interval)
        
        if df.empty:
            raise Exception(f"Nenhum dado encontrado para o símbolo {symbol} (Yahoo: {ticker_symbol})")
            
        df = df.tail(limit)
        
        candles = []
        for index, row in df.iterrows():
            candles.append(Candle(
                timestamp=index.to_pydatetime(),
                open=float(row['Open']),
                high=float(row['High']),
                low=float(row['Low']),
                close=float(row['Close']),
                volume=float(row['Volume'])
            ))
        return candles

    def _map_symbol(self, symbol: str) -> str:
        symbol = symbol.upper()
        # Mapeamento específico solicitado pelo usuário
        if symbol in ["NQ100", "NAS100", "NQ", "USTEC"]:
            return "NQ=F"  # Futuros do Nasdaq 100
        if symbol in ["SP500", "US500"]:
            return "ES=F"
        if symbol in ["GOLD", "XAUUSD"]:
            return "GC=F"
        if symbol in ["SILVER", "XAGUSD"]:
            return "SI=F"
        # Forex
        if len(symbol) == 6 and not symbol.endswith("USDT"):
            return f"{symbol}=X"
        return symbol

    def _map_timeframe(self, timeframe: str) -> str:
        mapping = {
            "1m": "1m", "5m": "5m", "15m": "15m", "30m": "30m", "1h": "1h", "1d": "1d"
        }
        return mapping.get(timeframe, "1h")
