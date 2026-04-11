import functools
import os
from pathlib import Path
from dto import LuistervinkSettings


# Assuming birdnet-go is installed with sudo
CONFIG_DIR = "/etc/birdnet/birdnet.conf"
HOME_DIR = os.path.expanduser("~")
DB_PATH = f"{HOME_DIR}/BirdNET-Pi/scripts/birds.db"

MAX_DETECTIONS_UPLOAD = 100
MAX_TASKS = 10


def _parse_conf(path: str) -> dict[str, str]:
    result = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


@functools.cache
def get_settings() -> LuistervinkSettings:
    """Load settings from the configuration file."""
    conf = _parse_conf(CONFIG_DIR)
    return LuistervinkSettings(
        server_address=conf.get("LUISTERVINK_SERVER_ADDRESS", ""),
        device_token=conf.get("LUISTERVINK_DEVICE_TOKEN", ""),
        enable_task_processor=conf.get("LUISTERVINK_ENABLE_TASK_PROCESSOR", "false").lower() == "true",
    )
