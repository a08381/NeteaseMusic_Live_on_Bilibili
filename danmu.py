from bilibili_api import Verify

class Danmu:

    def __init__(self, sessdata: str, csrf: str):
        self.verify = Verify(sessdata=sessdata, csrf=csrf)