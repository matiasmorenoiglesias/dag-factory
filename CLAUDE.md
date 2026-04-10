# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

DagFactory is a Python project. Currently in early development — `main.py` is the only file present.

## Setup

Once dependencies are defined, install them with:

```bash
pip install -e ".[dev]"   # if using pyproject.toml with dev extras
# or
pip install -r requirements.txt
```

## Common Commands

Commands will be added here as the project grows. Typical conventions for Python projects:

```bash
python main.py            # Run the application
pytest                    # Run all tests
pytest tests/test_foo.py::test_bar  # Run a single test
ruff check .              # Lint
ruff format .             # Format
mypy .                    # Type check
```

## Architecture

To be documented as the codebase grows. The project name suggests DAG (Directed Acyclic Graph) generation or management, potentially for workflow orchestration (e.g., Apache Airflow).
