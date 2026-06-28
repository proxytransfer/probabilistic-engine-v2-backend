from fastapi import APIRouter, HTTPException
from app.services.analysis_orchestrator import AnalysisOrchestrator

router = APIRouter()

@router.get("/{symbol}")
async def get_analysis(symbol: str):
    try:
        orchestrator = AnalysisOrchestrator()
        report = await orchestrator.get_full_analysis(symbol)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
