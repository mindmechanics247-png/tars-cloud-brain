from fastapi import APIRouter, Body
from app.router_ws import broadcast_message

router = APIRouter()

@router.post("/gesture")
async def gesture_event(payload: dict = Body(...)):
    """
    Accepts {"gesture":"pinch","confidence":0.92,"meta":{}} and broadcasts to WS clients.
    Also can enqueue robot commands or call tools.
    """
    gesture = payload.get("gesture", "")
    confidence = payload.get("confidence", 0.0)
    meta = payload.get("meta", {})

    # Broadcast to connected UI clients
    await broadcast_message({"type":"gesture", "gesture": gesture, "confidence": confidence, "meta": meta})

    # Optionally queue robot action here (left as safe placeholder)
    # e.g., if gesture == "pinch": robot_queue.append({"cmd":"SELECT","args":{}})

    return {"status":"ok", "broadcasted": True}
