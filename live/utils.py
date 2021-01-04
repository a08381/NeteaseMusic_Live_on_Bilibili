from enum import Enum
from typing import Any, Tuple

import qrcode
import requests
from PIL import Image
from bilibili_api import Verify

from live.settings import settings


class Status(Enum):
    KEY_ERROR = -1,
    KEY_TIMEOUT = -2,
    NOT_SCAN = -4,
    NOT_SUBMIT = -5,
    SUCCESS = 0,
    UNKNOWN_ERROR = 1

    @classmethod
    def get(cls, data: int):
        if data == -1:
            return Status.KEY_ERROR
        elif data == -2:
            return Status.KEY_TIMEOUT
        elif data == -4:
            return Status.NOT_SCAN
        elif data == -5:
            return Status.NOT_SUBMIT
        elif data == 0:
            return Status.SUCCESS
        else:
            return Status.UNKNOWN_ERROR


def make_qrcode(url: str, img: Image = None) -> Image:
    qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=4)
    qr.add_data(url)
    qr.print_ascii(invert=True)
    qr.make()

    image = qr.make_image()
    image.convert("RGBA")

    if img:
        img_w, img_h = image.size
        factor = 4
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        icon_w, icon_h = img.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        img = img.resize((icon_w, icon_h), Image.ANTIALIAS)

        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        img = img.convert("RGBA")
        image.paste(img, (w, h), img)

    return image


def get_login_qrcode() -> Tuple[Any, str]:
    image = None
    key = ""
    raw = requests.get("http://passport.bilibili.com/qrcode/getLoginUrl")
    if raw.status_code == 200:
        root = raw.json()
        if root["code"] == 0:
            url = root["data"]["url"]
            key = root["data"]["oauthKey"]
            image = make_qrcode(url)
    return image, key


def check_login_info(key: str) -> Status:
    data = {
        "oauthKey": key
    }
    raw = requests.post("http://passport.bilibili.com/qrcode/getLoginInfo", data=data)
    if raw.status_code == 200:
        root = raw.json()
        if root["status"]:
            verify = Verify(sessdata=raw.cookies["SESSDATA"], csrf=raw.cookies["bili_jct"])
            settings.verify = verify
            return Status.SUCCESS
        else:
            code = root["data"]
            return Status.get(code)
    return Status.UNKNOWN_ERROR
