from functools import reduce
from typing import Dict
from collections import Counter

type Source = str
type Target = str
type Frequency = int


class WeightedDirectedGraph:
    """Class to represent a weighted directed graph"""

    def __init__(
        self, storage: Dict[Source, Dict[Target, Frequency]] | None = None
    ) -> None:
        self.__storage: Dict[Source, Dict[Target, Frequency]] = (
            storage if storage is not None else {}
        )

    def add_edge(self, source: Source, target: Target, weight: int = 1):
        self.__storage.setdefault(source, {}).setdefault(target, 0)
        self.__storage[source][target] += weight
        return self

    def nodes(self):
        return sorted(
            reduce(
                lambda acc, item: acc | {item[0]} | set(item[1].keys()),
                self.__storage.items(),
                set(),
            )
        )

    def edges(self):
        return [
            (src, target, weight)
            for src, targets in self.__storage.items()
            for target, weight in targets.items()
        ]

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
            # Success / Positive (Green)
            "Offer": "rgba(40, 167, 69, 0.6)",
            "Awaiting contract": "rgba(40, 167, 69, 0.4)",
            # Progress / Neutral (Blues & Purples)
            "Applied": "rgba(108, 117, 125, 0.3)",
            "Screening": "rgba(23, 162, 184, 0.4)",
            "Interview": "rgba(0, 123, 255, 0.4)",  # Generic catch-all
            "Business Case": "rgba(102, 16, 242, 0.4)",
            "Technical Interview": "rgba(102, 16, 242, 0.4)",
            "Manager Interview": "rgba(102, 16, 242, 0.4)",
            "Take home assignment": "rgba(111, 66, 193, 0.4)",
            # Blocked / Negative (Red & Black)
            "Rejected": "rgba(220, 53, 69, 0.5)",
            "Ghosted": "rgba(33, 37, 41, 0.5)",
            "Stopped": "rgba(108, 117, 125, 0.6)",  # Manual exit
            "On hold": "rgba(255, 193, 7, 0.5)",  # Yellow
        }
        for src, targets in self.__storage.items():
            for dst, w in targets.items():
                source.append(nodes_indices[src])
                target.append(nodes_indices[dst])
                value.append(w)
                name_lower = dst.lower()
                if "interview" in name_lower or "meeting" in name_lower:
                    link_colors.append(default_colors.get("Interview", "grey"))
                else:
                    link_colors.append(default_colors.get(dst, "grey"))
        return dict(source=source, target=target, value=value, color=link_colors)

    def __repr__(self) -> str:
        return self.__storage.__str__()
