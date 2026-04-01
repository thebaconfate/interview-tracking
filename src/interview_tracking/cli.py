from os import name
from typer import Typer
from interview_tracking.persistance import *
from interview_tracking.entry import entry_app
from interview_tracking.stage import stage_app

app = Typer()


app.add_typer(entry_app, name="entry")
entry_app.add_typer(
    stage_app, name="stage", help="Commands related to stages of an application"
)


if __name__ == "__main__":
    app()
