from typing import List
from typer import Typer, Option, echo
from .types import Application
from .persistance import *

app = Typer()


@app.command()
def hello():
    print("hi")


@app.command("add-entry")
def add_entry(
    company: str,
    role: str,
    init_status: str = Option(
        "Interested",
        "--init_status",
        help="Initial status",
    ),
):
    """
    Add a new application entry
    """
    data: List[Application] = load_data()
    data.append({"company": company, "role": role, "history": [init_status]})
    save_data(data)
    echo(f"Added entry: {company} - {role}, history: {init_status}")


if __name__ == "__main__":
    app()
