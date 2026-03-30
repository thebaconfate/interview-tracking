import json
from graph import Graph
from pathlib import Path



def main():
    path = Path("data/data.json")
    with path.open() as f:
        data = json.load(f)
    g = Graph.fromJson(data)
    print(g)


if __name__ == "__main__":
    main()
