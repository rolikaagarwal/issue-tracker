import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.utils import pubsub_instance

router = APIRouter()

@router.get("/events")
async def events():
    """
    Server-Sent Events stream: clients subscribe here.
    """
    queue = await pubsub_instance.subscribe()

    async def event_generator():
        try:
            while True:
                msg = await queue.get()
                yield f"data: {json.dumps(msg)}\n\n"
        finally:
            await pubsub_instance.unsubscribe(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
