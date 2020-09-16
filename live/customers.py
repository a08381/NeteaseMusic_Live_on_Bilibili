import asyncio

__ws_queue = []


def broadcast(data: str):
    for queue in __ws_queue:
        queue.put_nowait(data)


def new() -> asyncio.Queue:
    queue = asyncio.Queue()
    __ws_queue.append(queue)
    return queue


def remove(queue: asyncio.Queue):
    __ws_queue.remove(queue)
