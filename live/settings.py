import json
import random
import string
from pathlib import Path

from bilibili_api import Verify

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:

    def __init__(self):
        self.config_file = BASE_DIR / "config.json"
        self.config = self.__load__()
        login = self.config.get("login")
        if login and login["SESSDATA"].strip() and login["bili_jct"].strip():
            self.__verify = Verify(sessdata=login["SESSDATA"], csrf=login["bili_jct"])
        else:
            self.__verify = None

    @property
    def verify(self) -> Verify:
        return self.__verify

    @verify.setter
    def verify(self, value: Verify) -> None:
        self.__verify = value
        self.config["login"]["SESSDATA"] = value.sessdata
        self.config["login"]["bili_jct"] = value.csrf
        self.save()

    @verify.deleter
    def verify(self):
        self.__verify = None
        self.config["login"]["SESSDATA"] = ""
        self.config["login"]["bili_jct"] = ""
        self.save()

    @property
    def room_id(self) -> int:
        return self.config.get("room_id", 0)

    @room_id.setter
    def room_id(self, value: int) -> None:
        self.config["room_id"] = value
        self.save()

    @room_id.deleter
    def room_id(self) -> None:
        self.config["room_id"] = 0
        self.save()

    @property
    def token(self) -> str:
        return self.config.get("token", "SECRET")

    @token.setter
    def token(self, value: str) -> None:
        self.config["token"] = value
        self.save()

    @token.deleter
    def token(self) -> None:
        self.config["token"] = ""
        self.save()

    @property
    def secret_key(self) -> str:
        key = self.config.get("secret_key", "")
        if key == "":
            key = "".join(random.sample(string.ascii_letters + string.digits, 32))
            self.config["secret_key"] = key
            self.save()
            self.reload()
            key = self.config.get("secret_key", "")
        return key

    def reload(self):
        if not self.config_file.exists():
            sample_file = BASE_DIR / "config_sample.json"
            self.config_file.write_bytes(sample_file.read_bytes())

        self.config = self.__load__()

    def save(self):
        self.config_file.write_text(json.dumps(self.config, indent=2), "UTF-8")

    def __load__(self):
        return json.loads(self.config_file.read_text(encoding="UTF-8"))


settings = Settings()
