from typer import Typer
from .persistance import *
from .types import DEFAULT_APPLICATION
from .subcommands import entry_app, stage_app

app = Typer()


app.add_typer(entry_app, name="entry")
entry_app.add_typer(
    stage_app, name="stage", help="Commands related to stages of an application"
)


@app.command("migrate")
def migrate():
    migrated = []
    applications = load_data()
    for application in applications:
        migrated_application = {}
        for key, default in DEFAULT_APPLICATION.items():
            migrated_application[key] = application.get(key, default)
        migrated.append(migrated_application)
    save_data(migrated)


if __name__ == "__main__":
    app()
