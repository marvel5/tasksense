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
