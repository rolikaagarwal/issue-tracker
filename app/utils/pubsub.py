import asyncio

class PubSub:
    def __init__(self):
        self.subscribers: list[asyncio.Queue] = []

    async def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        self.subscribers.append(q)
        return q

    async def unsubscribe(self, q: asyncio.Queue):
        try:
            self.subscribers.remove(q)
        except ValueError:
            pass

    async def publish(self, message: dict):
        for q in self.subscribers:
            await q.put(message)


