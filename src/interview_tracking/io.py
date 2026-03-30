import json
from typing import List
from .types import Application


def read_json(path: str) -> List[Application]:
    with open(path, "r") as f:
        return json.load(f)
