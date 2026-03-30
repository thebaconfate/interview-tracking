import json
from graph import Graph


def main():
    with open("../../data/data.json", "r") as f:
        data = json.load(f)
    g = Graph.fromJson(data)
    print(g)


if __name__ == "__main__":
    main()
