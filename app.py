#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path

from quart import Quart, request, render_template

BASE_DIR = Path(__file__).resolve().parent
config_file = BASE_DIR / "config.json"
if not config_file.exists():
    sample_file = BASE_DIR / "config_sample.json"
    config_file.write_bytes(sample_file.read_bytes())
config = json.load(config_file)
app = Quart(__name__)


@app.route("/")
async def index():
    if request.cookies.get("secret") == config.get("secret"):
        return render_template("")
    return render_template("block.html")

if __name__ == "__main__":
    app.run()
