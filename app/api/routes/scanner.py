from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.services.analysis_orchestrator import AnalysisOrchestrator
from app.domain.analysis import AnalysisReport

router = APIRouter()

@router.post("/scan", response_model=Dict[str, AnalysisReport])
async def scan_assets(symbols: List[str]):
    results = {}
    orchestrator = AnalysisOrchestrator()
    
    for symbol in symbols:
        try:
            report = await orchestrator.get_full_analysis(symbol)
            results[symbol] = report
        except Exception:
            continue
            
    return results
