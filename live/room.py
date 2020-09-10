import asyncio
from threading import Thread

from bilibili_api import Danmaku, live

from live.settings import settings


class Room:

    def __init__(self):
        self.connected = False
        self.verify = settings.verify
        self.danmaku = live.LiveDanmaku(settings.room_id, verify=self.verify, debug=True)
        self.danmaku.add_event_handler("DANMU_MSG", self.on_receive)
        self.loop = asyncio.new_event_loop()
        self.threading = None

    def connect(self):
        if not self.connected:
            self.connected = True
            self.threading = Connect(self)
            self.threading.start()

    def disconnect(self):
        if self.connected:
            self.connected = False
            self.danmaku.disconnect()
            self.threading.join()
            self.threading = None

    def reconnect(self):
        self.disconnect()
        self.connect()

    def send(self, text: str):
        danmaku = Danmaku(text=text)
        live.send_danmaku(self.danmaku.room_real_id, danmaku, verify=self.verify)

    async def on_receive(self, event: dict, *args, **kwargs):
        data = event["data"]
        info = data["info"]
        username = info[2][1]
        message = info[1]
        self.danmaku.logger.info(f"{username}: {message}")


class Connect(Thread):

    def __init__(self, room: Room):
        super().__init__()
        self.room = room
        self.daemon = True

    def run(self):
        asyncio.set_event_loop(self.room.loop)
        while self.room.connected:
            self.room.danmaku.connect()
