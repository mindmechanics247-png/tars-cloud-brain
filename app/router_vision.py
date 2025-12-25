from fastapi import APIRouter

router = APIRouter()

@router.post("/vision")
async def vision_disabled():
    return {
        "status": "disabled",
        "message": "Vision moved to ESP32-CAM. Cloud vision disabled."
    }
