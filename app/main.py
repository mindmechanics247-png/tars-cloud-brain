# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 🔥 Import your existing routers
from app.router_ai import router as ai_router
#from app.router_vision import router as vision_router
from app.router_robot import router as robot_router
from app.router_ws import router as ws_router

# ✅ NEW: LiveKit token router
from app.router_livekit import router as livekit_router

# ─────────────────────────────────────────────
# Create FastAPI app
# ─────────────────────────────────────────────

app = FastAPI(
    title="TARS Cloud Brain",
    description="Backend that powers TARS AI, Reasoning Model, Vision, Robot Control & LiveKit Voice",
    version="3.0"
)

# ─────────────────────────────────────────────
# CORS (Android App + LiveKit WebRTC needs this)
# ─────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # OPTIONAL: restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Include all routers
# ─────────────────────────────────────────────

app.include_router(ai_router, prefix="/ai", tags=["AI Chat"])
#app.include_router(vision_router, prefix="/vision", tags=["AI Vision"])
app.include_router(robot_router, prefix="/robot", tags=["Robot Control"])
app.include_router(ws_router, prefix="/ws", tags=["WebSocket"])

# NEW LiveKit router
app.include_router(livekit_router, prefix="/livekit", tags=["LiveKit"])

# ─────────────────────────────────────────────
# Root Endpoint
# ─────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "status": "TARS Cloud Brain running successfully",
        "message": "Connected: AI + Vision + Reasoning + Robot + LiveKit"
    }
