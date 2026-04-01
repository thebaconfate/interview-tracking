import pytest
from typer.testing import CliRunner

from interview_tracking.subcommands.entry import entry_app
from interview_tracking.subcommands.stage import stage_app


@pytest.fixture
def runner():
    return CliRunner()


def patch_storage(monkeypatch, data_ref):
    captured = {}

    def fake_load():
        return data_ref

    def fake_save(data):
        captured["data"] = data

    monkeypatch.setattr("interview_tracking.subcommands.stage.load_data", fake_load)
    monkeypatch.setattr("interview_tracking.subcommands.stage.save_data", fake_save)
    return captured


def test_add_stage(runner, monkeypatch):
    data = [
        {
            "company": "A",
            "role": "Dev",
            "history": ["Applied"],
            "open": True,
        }
    ]

    captured = patch_storage(monkeypatch, data)

    result = runner.invoke(
        stage_app,
        ["add", "Interview"],
        input="0\n",  # simulate user selecting index
    )

    assert result.exit_code == 0
    assert captured["data"][0]["history"] == ["Applied", "Interview"]
    assert "Updated A - Dev" in result.output


def test_add_invalid_index(runner, monkeypatch):
    data = [
        {
            "company": "A",
            "role": "Dev",
            "history": ["Applied"],
            "open": True,
        }
    ]

    captured = patch_storage(monkeypatch, data)

    result = runner.invoke(stage_app, ["add", "Interview"], input="999\n")

    assert result.exit_code == 0
    assert "Invalid selection" in result.output
    assert "data" not in captured  # save_data should NOT be called


def test_add_no_entries(runner, monkeypatch):
    captured = patch_storage(monkeypatch, [])

    result = runner.invoke(stage_app, ["add", "Interview"])

    assert result.exit_code == 0
    assert "No entries found" in result.output
    assert "data" not in captured


def test_update_history(runner, monkeypatch):
    data = [
        {
            "company": "A",
            "role": "Dev",
            "history": ["Applied", "Interview"],
            "open": True,
        }
    ]

    captured = patch_storage(monkeypatch, data)

    result = runner.invoke(
        stage_app,
        ["update", "Offer"],
        input="0\n1\n",  # select app, then history index
    )

    assert result.exit_code == 0
    assert captured["data"][0]["history"] == ["Applied", "Offer"]
    assert "Updated A - Dev" in result.output


def test_update_invalid_app_index(runner, monkeypatch):
    data = [
        {
            "company": "A",
            "role": "Dev",
            "history": ["Applied"],
            "open": True,
        }
    ]

    captured = patch_storage(monkeypatch, data)

    result = runner.invoke(stage_app, ["update", "Offer"], input="999\n")

    assert result.exit_code == 0
    assert "Invalid selection" in result.output
    assert "data" not in captured


def test_update_invalid_history_index(runner, monkeypatch):
    data = [
        {
            "company": "A",
            "role": "Dev",
            "history": ["Applied"],
            "open": True,
        }
    ]

    captured = patch_storage(monkeypatch, data)

    result = runner.invoke(stage_app, ["update", "Offer"], input="0\n999\n")

    assert result.exit_code == 0
    assert "Invalid selection" in result.output
    assert "data" not in captured


def test_remove_history(runner, monkeypatch):
    data = [
        {
            "company": "A",
            "role": "Dev",
            "history": ["Applied", "Interview"],
            "open": True,
        }
    ]

    captured = patch_storage(monkeypatch, data)

    result = runner.invoke(stage_app, ["remove"], input="0\n0\n")

    assert result.exit_code == 0
    assert captured["data"][0]["history"] == ["Interview"]
    assert "removed Applied" in result.output


def test_remove_invalid_index(runner, monkeypatch):
    data = [
        {
            "company": "A",
            "role": "Dev",
            "history": ["Applied"],
            "open": True,
        }
    ]

    captured = patch_storage(monkeypatch, data)

    result = runner.invoke(stage_app, ["remove"], input="999\n")

    assert result.exit_code == 0
    assert "Invalid selection" in result.output
    assert "data" not in captured
