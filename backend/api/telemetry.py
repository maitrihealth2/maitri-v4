import asyncio
import json
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

router = APIRouter(prefix="/api/telemetry", tags=["telemetry"])

# A global list of asyncio Queues for connected SSE clients
_clients = []

async def broadcast_event(event_type: str, message: str = "", data: dict = None):
    """
    Broadcasts a telemetry event to all connected SSE clients (e.g. HTML visualizer).
    """
    payload = {
        "event_type": event_type,
        "message": message,
        "data": data or {}
    }
    
    # We serialize it to JSON for the SSE data payload
    event_payload = json.dumps(payload)
    
    for queue in _clients:
        try:
            await queue.put({"data": event_payload})
        except Exception as e:
            print(f"[TELEMETRY] Error putting event in queue: {e}")

@router.get("/stream")
async def stream():
    """
    SSE Endpoint for real-time visualization.
    Clients connect to this to receive live routing events.
    """
    q = asyncio.Queue()
    _clients.append(q)
    print(f"[TELEMETRY] New client connected. Total clients: {len(_clients)}")
    
    async def event_generator():
        try:
            while True:
                # Wait for the next message from the queue
                msg = await q.get()
                yield msg
        except asyncio.CancelledError:
            print("[TELEMETRY] Client disconnected.")
            if q in _clients:
                _clients.remove(q)
                
    return EventSourceResponse(event_generator())
