import yfinance as yf
import httpx
from typing import List
from app.domain.candle import Candle
from app.infrastructure.providers.base import BaseDataProvider
from datetime import datetime, timedelta

class YahooFinanceProvider(BaseDataProvider):
    async def fetch_candles(self, symbol: str, timeframe: str, limit: int = 100) -> List[Candle]:
        symbol = symbol.upper()
        
        # ── Rota 1: Binance (Cripto em tempo real - SEM CACHE) ────────────────
        if symbol in ["BTCUSD", "ETHUSD", "SOLUSD", "BNBUSD"]:
            return await self._fetch_binance(symbol, timeframe, limit)
        
        # ── Rota 2: Yahoo Finance (Forex, Índices, Metais) ────────────────────
        return await self._fetch_yahoo(symbol, timeframe, limit)

    async def _fetch_binance(self, symbol: str, timeframe: str, limit: int) -> List[Candle]:
        # Mapear BTCUSD para BTCUSDT (Binance usa USDT)
        binance_symbol = symbol.replace("USD", "USDT")
        interval = self._map_timeframe_binance(timeframe)
        
        url = f"https://api.binance.com/api/v3/klines"
        params = {
            "symbol": binance_symbol,
            "interval": interval,
            "limit": limit
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
        candles = []
        for item in data:
            # item[0]: Open time, item[1]: Open, item[2]: High, item[3]: Low, item[4]: Close, item[5]: Volume
            candles.append(Candle(
                timestamp=datetime.fromtimestamp(item[0] / 1000.0),
                open=float(item[1]),
                high=float(item[2]),
                low=float(item[3]),
                close=float(item[4]),
                volume=float(item[5])
            ))
        return candles

    async def _fetch_yahoo(self, symbol: str, timeframe: str, limit: int) -> List[Candle]:
        ticker_symbol = self._map_symbol_yahoo(symbol)
        interval = self._map_timeframe_yahoo(timeframe)
        
        # Forçar busca de dados frescos usando datas explícitas
        # Isso evita o cache de dados históricos desatualizados
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start=start_date, end=end_date, interval=interval)
        
        if df.empty:
            # Fallback se a busca por data falhar (ex: mercado fechado ou símbolo novo)
            df = ticker.history(period="1mo", interval=interval)
            
        if df.empty:
            raise Exception(f"Nenhum dado encontrado para o símbolo {symbol}")
            
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

    def _map_symbol_yahoo(self, symbol: str) -> str:
        # Mapeamento robusto para Yahoo Finance
        mapping = {
            "NQ100": "NQ=F",
            "SP500": "ES=F",
            "DOW": "YM=F",
            "DAX": "^GDAXI",
            "XAUUSD": "GC=F",
            "XAGUSD": "SI=F",
            "OIL": "CL=F"
        }
        if symbol in mapping:
            return mapping[symbol]
        
        # Forex (ex: EURUSD -> EURUSD=X)
        if len(symbol) == 6:
            return f"{symbol}=X"
            
        return symbol

    def _map_timeframe_binance(self, timeframe: str) -> str:
        mapping = {"1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h", "4h": "4h", "1d": "1d"}
        return mapping.get(timeframe, "1h")

    def _map_timeframe_yahoo(self, timeframe: str) -> str:
        mapping = {"1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h", "1d": "1d"}
        return mapping.get(timeframe, "1h")
