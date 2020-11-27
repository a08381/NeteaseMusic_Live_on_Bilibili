#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""
 __      __                  __                                               
/\ \  __/\ \  __            /\ \                                              
\ \ \/\ \ \ \/\_\    ___    \_\ \    ___ ___     ___   __  __  _ __    ___    
 \ \ \ \ \ \ \/\ \ /' _ `\  /'_` \ /' __` __`\  / __`\/\ \/\ \/\`'__\/' _ `\  
  \ \ \_/ \_\ \ \ \/\ \/\ \/\ \L\ \/\ \/\ \/\ \/\ \L\ \ \ \_\ \ \ \/ /\ \/\ \ 
   \ `\___x___/\ \_\ \_\ \_\ \___,_\ \_\ \_\ \_\ \____/\ \____/\ \_\ \ \_\ \_\
    '\/__//__/  \/_/\/_/\/_/\/__,_ /\/_/\/_/\/_/\/___/  \/___/  \/_/  \/_/\/_/
                                                                              
"""

from quart import Quart

from live.settings import settings
from live.views import bluepoint

Application = Quart(__name__)

Application.jinja_env.auto_reload = True
Application.register_blueprint(bluepoint)

Application.secret_key = settings.secret_key

if __name__ == "__main__":

    Application.run()
