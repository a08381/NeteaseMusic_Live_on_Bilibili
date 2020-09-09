import asyncio

from bilibili_api import Danmaku, Verify, live

from live.settings import settings


class Room:

    danmaku = live.LiveDanmaku(33156)

    def __init__(self):
        self.verify = settings.verify
        self.danmaku = live.LiveDanmaku(settings.room_id, verify=self.verify)
        self.connected = False

    async def connect(self):
        self.connected = True
        asyncio.create_task(self.__room_connect())

    async def disconnect(self):
        self.connected = False
        self.danmaku.disconnect()

    async def reconnect(self):
        await self.disconnect()
        await asyncio.sleep(1)
        await self.connect()

    async def send(self, text: str):
        danmaku = Danmaku(text=text)
        live.send_danmaku(self.danmaku.room_id, danmaku, verify=self.verify)

    async def __room_connect(self):
        while self.connected:
            await self.danmaku.connect()

    @danmaku.on("DANMU_MSG")
    def on_receive(self, data: dict, *args, **kwargs):
        pass
