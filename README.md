# TaskSense

Task management REST API built with FastAPI, SQLAlchemy 2.0, Alembic and Pydantic, tested with pytest.

## Run

```bash
uv sync
uv run alembic upgrade head
uv run fastapi dev app/main.py
```

API docs: http://127.0.0.1:8000/docs

Configuration via environment variables or `.env` (default: SQLite):

```
DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/tasks
```

## Checks

```bash
uv run pytest -q
uv run mypy app tests
uv run ruff check . && uv run ruff format --check .
uv run alembic check
```

## Development

- **Pre-commit hooks:** `uv run pre-commit install` once. Ruff and mypy run on every commit,
  pytest on every push.
- **Shell:** `uv run python -m app.shell` opens a Python shell with a DB session and models loaded.
- **AI-assisted development:** `CLAUDE.md` holds the project conventions for coding agents.
  `.claude/settings.json` runs ruff after every edit and mypy + pytest before the agent finishes.
  `.mcp.json` connects the Context7 docs server for up-to-date library APIs.

### Branching (Git Flow)

- `main`: released code, tagged `vX.Y.Z`.
- `develop`: integration branch; pull requests target it.
- `feature/*` from `develop`; `release/*` from `develop` into `main`; `hotfix/*` from `main`.
