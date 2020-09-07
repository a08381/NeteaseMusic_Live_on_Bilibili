from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent

config_file = BASE_DIR / "config.json"
if not config_file.exists():
    sample_file = BASE_DIR / "config_sample.json"
    config_file.write_bytes(sample_file.read_bytes())

config = json.loads(config_file.read_text(encoding="UTF-8"))
