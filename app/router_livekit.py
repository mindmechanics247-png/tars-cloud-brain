# app/router_livekit.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from livekit import api
from app.config import LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL

router = APIRouter()

class TokenRequest(BaseModel):
    identity: str
    room: str = "tars-room"
    name: str | None = None

@router.post("/token")
async def generate_livekit_token(req: TokenRequest):
    """
    Generates a LiveKit JWT token so Android app can join the voice room.
    """

    if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET or not LIVEKIT_URL:
        raise HTTPException(status_code=500, detail="❌ LiveKit API keys missing in .env")

    at = api.AccessToken(api_key=LIVEKIT_API_KEY, api_secret=LIVEKIT_API_SECRET)
    grants = api.VideoGrants(room_join=True, room=req.room)

    token = (
        at.with_identity(req.identity)
          .with_name(req.name or req.identity)
          .with_grants(grants)
          .to_jwt()
    )

    return {
        "token": token,
        "url": LIVEKIT_URL,
        "api_key": LIVEKIT_API_KEY
    }
