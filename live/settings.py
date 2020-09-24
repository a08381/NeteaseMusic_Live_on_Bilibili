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

    @property
    def verify(self) -> Verify:
        login = self.config.get("login")
        if login:
            return Verify(sessdata=login["SESSDATA"] if login["SESSDATA"].strip() else None,
                          csrf=login["bili_jct"] if login["bili_jct"].strip() else None)
        return Verify()

    @property
    def room_id(self) -> int:
        return self.config.get("room_id", 0)

    @property
    def token(self) -> str:
        return self.config.get("token", "SECRET")

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
