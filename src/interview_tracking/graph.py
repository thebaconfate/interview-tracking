from typing import List

from interview_tracking.types import Application


class Graph:
    def __init__(self, storage: dict[str, List[str]] = {}) -> None:
        self.__storage = storage

    def add_edge(self, source: str, target: str):
        self.__storage.setdefault(source, []).append(target)
        return self

    def remove_edge(self, source: str, target: str):
        if self.__storage[source] is not None:
            self.__storage[source].remove(target)
            if (len(self.__storage[source])) == 0:
                self.__storage.pop(source)
        return self

    def edges(self, source: str):
        if self.__storage[source] is not None:
            return self.__storage[source]
        else:
            return set()

    def nodes(self):
        return list(self.__storage.keys())

    @staticmethod
    def fromJson(applications: List[Application]):
        g = Graph()
        for a in applications:
            for i in range(len(a["history"]) - 1):
                g.add_edge(a["history"][i], a["history"][i + 1])
        return g

    def __repr__(self) -> str:
        return self.__storage.__str__()
