from bilibili_api import Verify, live

import settings
import asyncio


class Room:

    def __init__(self):
        self.verify = Verify(sessdata=settings.config["login"]["SESSDATA"], csrf=settings.config["login"]["bili_jct"])
        self.danmaku = live.LiveDanmaku(settings.config["roomid"], verify=self.verify)
        self.send = live.send_danmaku
        self.connected = False

    def connect(self):
        self.connected = True
        asyncio.create_task(self.__room_connect())

    def disconnect(self):
        self.connected = False
        self.danmaku.disconnect()

    def reconnect(self):
        self.disconnect()
        asyncio.sleep(1)
        self.connect()

    async def __room_connect(self):
        while self.connected:
            await self.danmaku.connect()
            
    @danmaku.on("DANMU_MSG")
    def on_receive(data: dict, *args, **kwargs):
        pass
