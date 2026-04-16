import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from src.auth.jwt import decode_token
import redis.asyncio as aioredis
from src.config import settings

router = APIRouter(prefix="/ws", tags=["realtime"])
active_connections: dict[str, list[WebSocket]] = {}


@router.websocket("/alerts/{facility_id}")
async def alert_websocket(websocket: WebSocket, facility_id: str, token: str = Query(None)):
    try:
        if token:
            decode_token(token)
    except Exception:
        await websocket.close(code=4001)
        return

    await websocket.accept()
    if facility_id not in active_connections:
        active_connections[facility_id] = []
    if len(active_connections[facility_id]) >= 50:
        await websocket.close(code=4002)
        return
    active_connections[facility_id].append(websocket)

    r = None
    try:
        r = await aioredis.from_url(settings.redis_url, decode_responses=True)
        pubsub = r.pubsub()
        await pubsub.subscribe(f"alerts:{facility_id}", "alerts:all")

        async def heartbeat():
            while True:
                await asyncio.sleep(30)
                try:
                    await websocket.send_json({"type": "heartbeat"})
                except Exception:
                    break

        hb_task = asyncio.create_task(heartbeat())

        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        if r:
            try:
                await r.aclose()
            except Exception:
                pass
        if facility_id in active_connections and websocket in active_connections[facility_id]:
            active_connections[facility_id].remove(websocket)
