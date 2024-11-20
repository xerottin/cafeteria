from fastapi import WebSocket, WebSocketDisconnect, APIRouter

router = APIRouter(prefix="", tags=["websocket"])

active_connections = {}

@router.websocket("/ws/{cafeteria_id}")
async def websocket_endpoint(websocket: WebSocket, cafeteria_id: int):
    await websocket.accept()
    if cafeteria_id not in active_connections:
        active_connections[cafeteria_id] = []
    active_connections[cafeteria_id].append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections[cafeteria_id].remove(websocket)

