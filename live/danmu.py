import asyncio

from bilibili_api import Danmaku, Verify, live

from live.settings import settings


class Room:

    verify = settings.verify
    danmaku = live.LiveDanmaku(settings.room_id, verify=verify)

    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True
        self.__room_connect()

    def disconnect(self):
        self.connected = False
        self.danmaku.disconnect()

    def reconnect(self):
        self.disconnect()
        asyncio.sleep(1)
        self.connect()

    def send(self, text: str):
        danmaku = Danmaku(text=text)
        live.send_danmaku(self.danmaku.room_id, danmaku, verify=self.verify)

    def __room_connect(self):
        while self.connected:
            await self.danmaku.connect()

    @danmaku.on("DANMU_MSG")
    def on_receive(self, data: dict, *args, **kwargs):
        pass
