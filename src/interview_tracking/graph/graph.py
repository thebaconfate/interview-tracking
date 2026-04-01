from functools import reduce
from typing import Dict, List
import json
from interview_tracking.types import Application
from collections import Counter

type Source = str
type Target = str
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
                        label=self.__labels(),
                        color="blue",
                    ),
                    link=self.__link(),
                )
            ]
        )
        fig.update_layout(title_text="Interview process", font_size=10)
        fig.write_html("figure.html", include_plotlyjs="cdn")

    def __labels(self):
        c_in = Counter()
        c_out = Counter()
        for src, targets in self.__storage.items():
            c_out[src] += sum(targets.values())
            for target, freq in targets.items():
                c_in[target] += freq
        all_nodes = self.nodes()
        return [
            f"{node} ({c_out[node] if c_in[node] == 0 else c_in[node]})"
            for node in all_nodes
        ]

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
