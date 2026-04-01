from typing import List
import typer

from interview_tracking.graph import WeightedDirectedGraph
from interview_tracking.persistance import load_data, save_data
from interview_tracking.types import Application, Applications


entry_app = typer.Typer()


@entry_app.command("new")
def new_entry(
    company: str,
    role: str,
    init_status: str = typer.Option(
        "Interested",
        "--init-status",
        "-s",
        help="Initial status",
    ),
):
    """
    Add a new application entry
    """
    data: List[Application] = load_data()
    data.append(
        {"company": company, "role": role, "history": [init_status], "open": True}
    )
    save_data(data)
    typer.echo(f"Added entry: {company} - {role}, history: {init_status}")


@entry_app.command("list")
def list_applications():
    """
    List all applications, regardless if they're ongoing or not
    """
    data: Applications = load_data()
    for i, application in enumerate(data):
        typer.echo(f"{i} {application['company']} - {application['role']}")


@entry_app.command("list-open")
def list_ongoing_applications():
    """
    List ongoing applications
    """
    data: Applications = load_data()
    for i, application in enumerate(data):
        if not application["open"]:
            continue
        typer.echo(f"{i} {application['company']} - {application['role']}")


@entry_app.command("close")
def update_status():
    """
    Update wether an application is ongoing or not
    """
    data: Applications = load_data()
    for i, application in enumerate(data):
        if application["open"]:
            typer.echo(f"{i} {application['company']} - {application['role']}")
    idx = int(typer.prompt("Pick an entry by number"))
    data[idx]["open"] = False
    save_data(data)
    typer.echo(f"Closed application: {data[idx]['company']} - {data[idx]['role']}")


@entry_app.command("sankey")
def sankey():
    """
    Generates a sankey diagram based on the current applications
    """
    data = load_data()
    g = WeightedDirectedGraph()
    for d in data:
        size = len(d["history"])
        if size > 1:
            for i in range(size - 1):
                g.add_edge(d["history"][i], d["history"][i + 1])
        else:
            g.add_edge(d["history"][0], "Awaiting response")

    g.sankey_diagram()
    typer.echo("Generated sankey diagram")
