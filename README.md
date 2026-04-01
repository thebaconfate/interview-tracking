# Interview tracker

A CLI tool to keep track of your interview process.

# Installing

This project uses uv as the dependency manager. Consequently you should have
uv installed, if not install it through the instructions: [astral-uv](https://docs.astral.sh/uv/getting-started/installation/)

Afterwards it's sufficient to use

```bash
uv sync
```

# Usage

Prior to usage, make sure you're using the virtual environment that has the
dependencies installed

```bash
source .venv/bin/activate
```

Your terminal should prefix the current directory with the name of the virtual
environment.

Usage is straight forward. All commands are documented and can be polled trought
the tool itself. The prefix to use the tracker will be 'Tracker'

```bash
tracker --help
#or
tracker [SUBCOMMAND] --help
```
