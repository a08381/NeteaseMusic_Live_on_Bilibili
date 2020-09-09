from pathlib import Path
import json
from bilibili_api import Verify

BASE_DIR = Path(__file__).resolve().parent.parent

settings = Settings()

class Settings:

    def __init__(self):
        self.config_file = BASE_DIR / "config.json"
        if not config_file.exists():
            sample_file = BASE_DIR / "config_sample.json"
            config_file.write_bytes(sample_file.read_bytes())

        self.config = json.loads(config_file.read_text(encoding="UTF-8"))

        @property
        def verify(self) -> Verify:
            login = self.config.get("login")
            if login:
                return Verify(sessdata=login["SESSDATA"], csrf=login["bili_jct"])
            else:
                return Verify()

        @property
        def room_id(self) -> int:
            return config.get("roomid", 0)
