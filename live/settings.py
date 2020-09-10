import json
from pathlib import Path

from bilibili_api import Verify

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:

    def __init__(self):
        self.config_file = BASE_DIR / "config.json"
        if not self.config_file.exists():
            sample_file = BASE_DIR / "config_sample.json"
            self.config_file.write_bytes(sample_file.read_bytes())

        self.config = json.loads(self.config_file.read_text(encoding="UTF-8"))

    @property
    def verify(self) -> Verify:
        login = self.config.get("login")
        if login:
            return Verify(sessdata=login["SESSDATA"] if login["SESSDATA"].strip() else None, csrf=login["bili_jct"] if login["bili_jct"].strip() else None)
        return Verify()

    @property
    def room_id(self) -> int:
        return self.config.get("room_id", 0)

    @property
    def secret(self) -> str:
        return self.config.get("secret", "SECRET")


settings = Settings()
