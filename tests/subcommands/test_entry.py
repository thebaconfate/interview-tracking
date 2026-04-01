import pytest
from typer.testing import CliRunner
from interview_tracking.subcommands.entry import entry_app


@pytest.fixture
def runner():
    return CliRunner()


def test_new_entry(runner, monkeypatch):
    captured = {}

    def fake_load():
        return []

    def fake_save(data):
        captured["data"] = data

    monkeypatch.setattr("interview_tracking.subcommands.entry.load_data", fake_load)
    monkeypatch.setattr("interview_tracking.subcommands.entry.save_data", fake_save)

    result = runner.invoke(
        entry_app, ["new", "CompanyA", "Engineer", "--init-status", "Applied"]
    )

    assert result.exit_code == 0
    assert captured["data"][0]["company"] == "CompanyA"
    assert captured["data"][0]["history"] == ["Applied"]
    assert "Added entry" in result.output


def test_list_applications(runner, monkeypatch):
    monkeypatch.setattr(
        "interview_tracking.subcommands.entry.load_data",
        lambda: [
            {"company": "A", "role": "Dev", "history": [], "open": True},
        ],
    )

    result = runner.invoke(entry_app, ["list"])

    assert result.exit_code == 0
    assert "A - Dev" in result.output
