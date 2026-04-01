from pathlib import Path
import json
from typing import List

from interview_tracking.types import Application


file = Path("data/data.json")


def load_data() -> List[Application]:
    global file
    if not file.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch(exist_ok=True)
        return []
    with file.open() as f:
        return json.load(f)


def save_data(data: List[Application]):
    global file
    if not file.exists():
        file.parent.mkdir(parents=True, exist_ok=True)
        file.touch(exist_ok=True)
    file.write_text(json.dumps(data, indent=4))
