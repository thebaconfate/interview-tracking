from typer import Typer
from interview_tracking.persistance import *
from interview_tracking.entry import entry_app
from interview_tracking.stage import stage_app
from interview_tracking.types import DEFAULT_APPLICATION

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
