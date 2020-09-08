#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quart import Quart, redirect, render_template, request, url_for, websocket
from pathlib import Path

settings_file = Path(__file__).resolve().parent / "live/settings.py"
if not settings_file.exists():
    sample_file = settings_file.parent / "settings_sample.py"
    settings_file.write_bytes(sample_file.read_bytes())

from live import settings


app = Quart(__name__)

app.jinja_env.auto_reload = True


@app.route("/")
async def index():
    if request.cookies and request.cookies.get("secret", "") == settings.config.get("secret", "SECRET"):
        return await render_template("index.html")
    return await render_template("block.html")


@app.route("/submit", methods=['POST'])
async def submit():
    resp = redirect(url_for("index"))
    form = await request.form
    resp.set_cookie("secret", form.get("secret", ""))
    return resp


@app.websocket("/ws")
async def ws():
    while True:
        data = await websocket.receive()
        await websocket.send(f"echo {data}")


if __name__ == "__main__":
    app.run(host='0', debug=True)
