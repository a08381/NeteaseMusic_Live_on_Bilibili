#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quart import Quart

from live.settings import settings
from live.views import bluepoint

Application = Quart(__name__)

Application.jinja_env.auto_reload = True
Application.register_blueprint(bluepoint)

Application.secret_key = settings.secret_key

if __name__ == "__main__":
    Application.run()
