from typing import List
import typer

from interview_tracking.persistance import load_data, save_data
from interview_tracking.types import Application, Applications


stage_app = typer.Typer()


@stage_app.command("add")
def progress_application(new_status: str):
    """
    Add a new stage to an application
    """
    data: List[Application] = load_data()
    if not data:
        typer.echo("No entries found")
        raise typer.Exit()
    for i, application in enumerate(data):
        if application["open"]:
            typer.echo(f"{i}: {application['company']} - {application['role']}")
    idx = int(typer.prompt("Pick an entry by number"))
    if 0 <= idx < len(data):
        data[idx]["history"].append(new_status)
        save_data(data)
        typer.echo(
            f"Updated {data[idx]['company']} - {data[idx]['role']} with status {new_status}"
        )
    else:
        typer.echo("Invalid selection")


@stage_app.command("update")
def update_history(new_status: str):
    """
    Updates an existing stage from an application
    """
    data: List[Application] = load_data()
    for i, application in enumerate(data):
        if application["open"]:
            typer.echo(
                f"{i}: {application['company']} - {application['role']} "
                + f"{application['history']}"
            )
    idx = int(typer.prompt("Pick an entry by number to update"))
    if 0 <= idx < len(data):
        for i, h in enumerate(data[idx]["history"]):
            typer.echo(f"{i}: {h}")
        h_idx = int(typer.prompt("Pick an entry by number to update"))
        if 0 <= h_idx < len(data[idx]["history"]):
            old_status = data[idx]["history"][h_idx]
            data[idx]["history"][h_idx] = new_status
            save_data(data)
            typer.echo(
                f"Updated {data[idx]['company']} - {data[idx]['role']} from "
                + f"status {old_status} to {new_status}"
            )
        else:
            typer.echo("Invalid selection")
    else:
        typer.echo("Invalid selection")


@stage_app.command("remove")
def remove_history():
    """
    Removes an existing stage from an application
    """
    data: Applications = load_data()
    for i, application in enumerate(data):
        if application["open"]:
            typer.echo(
                f"{i}: {application['company']} - {application['role']} "
                + f"{application['history']}"
            )
    idx = int(typer.prompt("Pick an entry by number to update"))
    if 0 <= idx < len(data):
        for i, h in enumerate(data[idx]["history"]):
            typer.echo(f"{i}: {h}")
        h_idx = int(typer.prompt("Pick an entry by number to remove"))
        if 0 <= h_idx < len(data[idx]["history"]):
            old_status = data[idx]["history"][h_idx]
            del data[idx]["history"][h_idx]
            save_data(data)
            typer.echo(
                f"removed {old_status} from {data[idx]['company']} - {data[idx]['role']}"
            )
        else:
            typer.echo("Invalid selection")
    else:
        typer.echo("Invalid selection")
