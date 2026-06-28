from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import analysis, health, scanner
from .api.websocket.manager import WebSocketManager
from .core.config import get_settings

settings = get_settings()
app = FastAPI(title="Probabilistic Engine v2.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(health.router)
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(scanner.router, prefix="/scanner", tags=["scanner"])

# WebSocket
ws_manager = WebSocketManager()

@app.websocket("/ws/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await ws_manager.connect(websocket, symbol)
    try:
        while True:
            # Keep-alive simple
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, symbol)
