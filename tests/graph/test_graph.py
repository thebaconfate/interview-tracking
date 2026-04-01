from typing import Dict
from interview_tracking.graph import WeightedDirectedGraph
from collections import Counter
import pytest


@pytest.fixture
def simple_graph():
    g = WeightedDirectedGraph()
    g.add_edge("A", "B").add_edge("A", "B")  # weight = 2
    g.add_edge("A", "C")
    g.add_edge("B", "C")
    return g


def flatten(storage: Dict[str, Dict[str, int]]):
    for src, targets in storage.items():
        for target, weight in targets.items():
            yield (src, target, weight)


def test_add_edge_default_weight():
    g = WeightedDirectedGraph()
    g.add_edge("A", "B")
    assert ("A", "B", 1) in g.edges()


def test_add_edge_custom_weight():
    g = WeightedDirectedGraph()
    g.add_edge("A", "B", 5)
    assert ("A", "B", 5) in g.edges()


def test_add_edge_accumulates_weight():
    g = WeightedDirectedGraph()
    g.add_edge("A", "B", 2)
    g.add_edge("A", "B", 3)
    assert ("A", "B", 5) in g.edges()


def test_multiple_edges():
    g = WeightedDirectedGraph()
    edges = [("A", "B", 2), ("A", "C", 1)]
    for e in edges:
        g.add_edge(*e)
    assert Counter(g.edges()) == Counter(edges)


def test_nodes():
    g = WeightedDirectedGraph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    assert set(g.nodes()) == {"A", "B", "C"}


def test_sankey_runs(tmp_path, monkeypatch):
    g = WeightedDirectedGraph()
    g.add_edge("A", "B", 1)
    monkeypatch.chdir(tmp_path)
    g.sankey_diagram()
    assert (tmp_path / "figure.html").exists()
