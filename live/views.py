from quart import Blueprint, redirect, render_template, request, url_for, websocket

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
    while True:
        data = await websocket.receive()
        await websocket.send(f"echo {data}")
