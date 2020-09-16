import asyncio

from asyncio import Queue
from quart import Blueprint, redirect, render_template, request, url_for, websocket

from live import customers
from live.settings import settings

bluepoint = Blueprint('views', __name__)


@bluepoint.route("/")
async def index():
    if request.cookies and request.cookies.get("secret", "") == settings.secret:
        return await render_template("index.html")
    return await render_template("block.html")


@bluepoint.route("/submit", methods=['POST'])
async def submit():
    resp = redirect(url_for("views.index"))
    form = await request.form
    resp.set_cookie("secret", form.get("secret", ""))
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


async def recv():
    while True:
        data = await websocket.receive()
        # TODO: WebSocket Check


async def send(queue: Queue):
    while True:
        data = await queue.get()
        await websocket.send(data)
