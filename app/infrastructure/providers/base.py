from abc import ABC, abstractmethod
from typing import List
from app.domain.candle import Candle

class BaseDataProvider(ABC):
    @abstractmethod
    async def fetch_candles(self, symbol: str, timeframe: str, limit: int) -> List[Candle]:
        pass
