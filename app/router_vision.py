from fastapi import APIRouter, File, UploadFile, HTTPException
from app.vision_engine import analyze_frame_bytes
from app.gestures import map_gesture_token

router = APIRouter()

@router.post("/vision")
async def vision_endpoint(file: UploadFile = File(...)):
    """
    POST multipart/form-data: file (image/jpeg)
    Returns structured vision analysis and mapped action.
    """
    try:
        frame = await file.read()
        res = analyze_frame_bytes(frame)
        res["mapped_action"] = map_gesture_token(res.get("gesture", "none"))
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
