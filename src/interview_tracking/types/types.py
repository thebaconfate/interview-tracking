from typing import List, TypedDict


class Application(TypedDict):
    company: str
    role: str
    history: List[str]
    open: bool


type Applications = List[Application]

DEFAULT_APPLICATION: Application = {
    "company": "",
    "role": "",
    "history": [],
    "open": True,
}
