import asyncio
from asyncio import Queue
from typing import Any, Optional

from quart import redirect, render_template, url_for
from quart.app import Blueprint
from quart.globals import request, websocket, session
from quart.wrappers import Websocket

from live import customers
from live.settings import settings

bluepoint = Blueprint('views', __name__)


@bluepoint.route("/")
async def index():
    if session.get("secret", "") == settings.secret:
        return await render_template("index.html")
    return await render_template("block.html")


@bluepoint.route("/submit", methods=['POST'])
async def submit():
    resp = redirect(url_for("views.index"))
    form = await request.form
    session["secret"] = form.get("secret", "")
    return resp


@bluepoint.websocket("/ws")
async def ws():
    queue = customers.new()
    try:
        producer = asyncio.create_task(send(queue))
        consumer = asyncio.create_task(recv())
        await asyncio.gather(producer, consumer)
    except asyncio.CancelledError:
        customers.remove(queue)


async def recv() -> None:
    while True:
        data = await websocket.receive()
        # TODO: WebSocket Check


async def send(queue: Queue) -> None:
    while True:
        data = await queue.get()
        await __send(websocket, data)


async def __send(wss: Websocket, data: Optional[Any]) -> None:
    if data:
        if type(data) == str:
            await wss.send(data)
        elif type(data) == dict:
            await wss.send_json(data)
        else:
            await wss.send_json(data.__dict__)
