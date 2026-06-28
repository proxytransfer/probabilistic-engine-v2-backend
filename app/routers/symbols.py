# app/routers/symbols.py
# Coloque este arquivo em: app/routers/symbols.py
# Depois em app/main.py adicione:
#   from app.routers.symbols import router as symbols_router
#   app.include_router(symbols_router)

from fastapi import APIRouter

router = APIRouter(tags=["symbols"])

SYMBOLS = [
    # ── Crypto ────────────────────────────────────────────────────────────────
    {"symbol": "BTCUSD",  "name": "Bitcoin / USD",              "category": "crypto",  "provider": "binance"},
    {"symbol": "ETHUSD",  "name": "Ethereum / USD",             "category": "crypto",  "provider": "binance"},
    {"symbol": "SOLUSD",  "name": "Solana / USD",               "category": "crypto",  "provider": "binance"},
    {"symbol": "BNBUSD",  "name": "BNB / USD",                  "category": "crypto",  "provider": "binance"},

    # ── Índices ───────────────────────────────────────────────────────────────
    {"symbol": "NQ100",   "name": "Nasdaq 100 (Futuros)",       "category": "indices", "provider": "yahoo"},
    {"symbol": "SP500",   "name": "S&P 500 (Futuros)",          "category": "indices", "provider": "yahoo"},
    {"symbol": "DOW",     "name": "Dow Jones (Futuros)",         "category": "indices", "provider": "yahoo"},
    {"symbol": "DAX",     "name": "DAX 40 (Futuros)",           "category": "indices", "provider": "yahoo"},

    # ── Forex — Top 5 pares ───────────────────────────────────────────────────
    {"symbol": "EURUSD",  "name": "Euro / Dólar",               "category": "forex",   "provider": "yahoo"},
    {"symbol": "GBPUSD",  "name": "Libra / Dólar",              "category": "forex",   "provider": "yahoo"},
    {"symbol": "USDJPY",  "name": "Dólar / Iene",               "category": "forex",   "provider": "yahoo"},
    {"symbol": "USDCHF",  "name": "Dólar / Franco Suíço",       "category": "forex",   "provider": "yahoo"},
    {"symbol": "AUDUSD",  "name": "Dólar Australiano / Dólar",  "category": "forex",   "provider": "yahoo"},

    # ── Metais ────────────────────────────────────────────────────────────────
    {"symbol": "XAUUSD",  "name": "Ouro / USD",                 "category": "metals",  "provider": "yahoo"},
    {"symbol": "XAGUSD",  "name": "Prata / USD",                "category": "metals",  "provider": "yahoo"},
    {"symbol": "OIL",     "name": "Petróleo WTI",               "category": "metals",  "provider": "yahoo"},
]


@router.get("/symbols")
async def get_symbols():
    """
    Retorna todos os símbolos suportados.
    O Lovable usa isso para montar o dropdown de seleção.
    """
    return SYMBOLS


@router.get("/symbols/{category}")
async def get_symbols_by_category(category: str):
    """
    Filtra por categoria: crypto | indices | forex | metals
    """
    filtered = [s for s in SYMBOLS if s["category"] == category.lower()]
    if not filtered:
        return {"error": f"Categoria '{category}' não encontrada", "valid": ["crypto", "indices", "forex", "metals"]}
    return filtered
