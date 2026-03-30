from typing import List
from types import Application


class Graph:
    def __init__(self, storage: dict[str, set[str]] = {}) -> None:
        self.__storage = storage

    def add_edge(self, source: str, target: str):
        self.__storage.setdefault(source, set()).add(target)
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
        storage = {}
        for a in applications:
            print(a)
