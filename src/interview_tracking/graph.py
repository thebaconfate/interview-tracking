from functools import reduce
from typing import Dict, List
from interview_tracking.types import Application
from collections import Counter

type Source = str
type Target = str


class DirectedGraph:
    """Class to represent a directed graph"""

    def __init__(self, storage: dict[Source, List[Target]] = {}) -> None:
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
        return sorted(
            reduce(
                lambda acc, item: acc.union({item[0]}).union(set(item[1])),
                self.__storage.items(),
                set(),
            )
        )

    @staticmethod
    def fromJson(applications: List[Application]):
        g = DirectedGraph()
        for a in applications:
            for i in range(len(a["history"]) - 1):
                g.add_edge(a["history"][i], a["history"][i + 1])
        return g

    def __repr__(self) -> str:
        return self.__storage.__str__()


type Frequency = int


class WeightedDirectedGraph:
    """Class to represent a weighted directed graph"""

    def __init__(self, storage: Dict[Source, Dict[Target, Frequency]] = {}) -> None:
        self.__storage: Dict[Source, Dict[Target, Frequency]] = storage

    def add_edge(self, source: Source, target: Target):
        self.__storage.setdefault(source, {}).setdefault(target, 0)
        self.__storage[source][target] += 1
        return self

    def nodes(self):
        return sorted(
            reduce(
                lambda acc, item: acc | {item[0]} | set(item[1].keys()),
                self.__storage.items(),
                set(),
            )
        )

    def sankey_diagram(self):
        import plotly.graph_objects as go

        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=self.nodes(),
                        color="blue",
                    ),
                    link=self.__link(),
                )
            ]
        )
        fig.update_layout(title_text="Interview process", font_size=10)
        self.__labels()
        fig.write_html("figure.html", include_plotlyjs="cdn")

    def __labels(self):
        c = Counter()
        for src, targets in self.__storage.items():
            c.update({src})
            for target, frequency in targets.items():
                for _ in range(frequency):
                    c.update({target})
        print(c)

    def __link(self):
        nodes_indices = {name: i for i, name in enumerate(self.nodes())}
        source = []
        target = []
        value = []
        link_colors = []
        default_colors = {
            "Interview 1": "blue",
            "Offer": "green",
            "Ghosted": "black",
            "In progress": "yellow",
            "Rejected": "red",
        }
        for src, targets in self.__storage.items():
            for dst, w in targets.items():
                source.append(nodes_indices[src])
                target.append(nodes_indices[dst])
                value.append(w)
                link_colors.append(default_colors.get(dst, "grey"))
        return dict(source=source, target=target, value=value, color=link_colors)

    def __repr__(self) -> str:
        return self.__storage.__str__()
