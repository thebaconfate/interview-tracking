import json
from typing import List
from graph import DirectedGraph, WeightedDirectedGraph
from pathlib import Path

from interview_tracking.types import Application


def main():
    path = Path("data/data.json")
    with path.open() as f:
        data: List[Application] = json.load(f)
    g = WeightedDirectedGraph()
    for d in data:
        for i in range(len(d["history"]) - 1):
            g.add_edge(d["history"][i], d["history"][i + 1])
    g.sankey_diagram()


if __name__ == "__main__":
    main()
