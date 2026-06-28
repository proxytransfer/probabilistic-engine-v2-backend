from datetime import datetime
from app.domain.analysis import AnalysisReport
from app.engines.liquidity.detector import EfficientLiquidityDetector
from app.engines.quarterly.state_machine import QuarterStateMachine
from app.engines.probability.calibrator import ScoreCalibrator
from app.core.config import get_settings
from app.services.data_service import DataService

class AnalysisOrchestrator:
    def __init__(self, cache=None, provider=None):
        self.settings = get_settings()
        self.data_service = DataService()
        self.liquidity_detector = EfficientLiquidityDetector()
        self.quarterly_engine = QuarterStateMachine()
        self.calibrator = ScoreCalibrator(k=self.settings.CALIBRATION_K)

    async def get_full_analysis(self, symbol: str) -> AnalysisReport:
        # 1. Fetch real market data
        candles = await self.data_service.get_market_data(symbol, "1h")
        
        # 2. Update engines
        self.liquidity_detector.update(candles)
        
        # 3. Calculate score
        raw_score = 72.5 # Valor base para teste, integrando lógica dos motores futuramente
        
        # 4. Calibrate probability
        prob = self.calibrator.probability(raw_score)
        
        # 5. Build report
        report = AnalysisReport(
            symbol=symbol,
            timestamp=datetime.now(),
            raw_score=raw_score,
            calibrated_probability=prob,
            direction="BULLISH" if raw_score > 50 else "BEARISH",
            confidence="HIGH" if prob > 0.7 else "MEDIUM",
            components={"liquidity": 80, "quarterly": 65},
            active_zones=self.liquidity_detector.get_active_zones(),
            scenario="REAL_TIME_ANALYSIS",
            targets=[candles[-1].close * 1.015] if candles else []
        )
        return report
