#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio

from quart import Quart

from live.danmu import Room
from live.views import bluepoint

Application = Quart(__name__)

Application.jinja_env.auto_reload = True
Application.register_blueprint(bluepoint)

if __name__ == "__main__":

    room = Room()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(room.connect())

    Application.run()
