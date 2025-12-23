from fastapi import APIRouter, Body
from typing import Dict

router = APIRouter()
ROBOT_QUEUE = []

@router.post("/robot/command")
async def robot_command(payload: Dict = Body(...)):
    """
    { "cmd": "HEAD_LEFT", "args": {} }
    This endpoint enqueues a command for the robot. The robot should poll /robot/next or connect via WS.
    """
    cmd = payload.get("cmd")
    args = payload.get("args", {})
    if not cmd:
        return {"status":"error","msg":"cmd missing"}
    ROBOT_QUEUE.append({"cmd": cmd, "args": args})
    return {"status":"ok","queued": len(ROBOT_QUEUE)}

@router.get("/robot/next")
async def robot_next():
    """Robot polls for next command (pop from queue)."""
    if ROBOT_QUEUE:
        return ROBOT_QUEUE.pop(0)
    return {"cmd":"NOOP"}
