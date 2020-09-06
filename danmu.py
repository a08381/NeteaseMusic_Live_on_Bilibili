from bilibili_api import Verify, live

import app

verify = Verify(sessdata=app.config["login"]["SESSDATA"],
                csrf=app.config["login"]["bili_jct"])
danmaku = live.LiveDanmaku(app.config["roomid"], verify=verify)


def on_live(self):
    danmaku.connect()  # this will block thread
    pass


@danmaku.on("DANMU_MSG")
def on_receive(data: dict, *args, **kwargs):
    pass
