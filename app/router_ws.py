from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        data = json.dumps(message)
        coros = [conn.send_text(data) for conn in list(self.active_connections)]
        if coros:
            await asyncio.gather(*coros, return_exceptions=True)

manager = ConnectionManager()

async def broadcast_message(message: dict):
    await manager.broadcast(message)

@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        await ws.send_text(json.dumps({"type":"connected","msg":"TARS WS connected"}))
        while True:
            txt = await ws.receive_text()
            # Simple echo or handle pings
            await ws.send_text(json.dumps({"type":"echo","msg":txt}))
    except WebSocketDisconnect:
        manager.disconnect(ws)
