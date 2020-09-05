#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quart import Quart, render_template, request
from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent
config = json.load(BASE_DIR / "config.json")
app = Quart(__name__)


@app.route("/")
async def index():
    if request.cookies.get("secret") == config.get("secret"):
        return render_template()
    else:
        return render_template()
