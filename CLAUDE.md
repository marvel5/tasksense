# TaskSense — guidelines for AI agents

Task management REST API. Python 3.13, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, pytest, uv.

## Commands

| Task | Command |
|---|---|
| Install / sync deps | `uv sync` |
| Add a dependency | `uv add <pkg>` (dev: `uv add --dev <pkg>`) — never `pip install` |
| Run the API | `uv run fastapi dev app/main.py` |
| Shell (like tinker) | `uv run python -m app.shell` — or one-off: `uv run python -c "..."` |
| Tests | `uv run pytest -q` (one test: `-k name`) |
| Types | `uv run mypy app tests` (strict) |
| Lint / format | `uv run ruff check --fix . && uv run ruff format .` |
| New migration | `uv run alembic revision --autogenerate -m "..."` |
| Migrate | `uv run alembic upgrade head` / `alembic check` (models vs migrations) |

Hooks in `.claude/settings.json` run ruff after every edit and mypy + pytest before you finish.
Fix what they report; never silence a rule with `# noqa` / `# type: ignore` without a stated reason.

## Layout

```
app/
  main.py          FastAPI app, router registration
  config.py        Settings (pydantic-settings, env / .env)
  database.py      engine, Base, get_session, SessionDep
  models.py        SQLAlchemy models
  schemas.py       Pydantic request/response models
  routers/         HTTP layer, one module per resource
  shell.py         interactive shell
migrations/        Alembic
tests/             pytest; conftest.py holds the session/client fixtures
```

When a resource gains business logic beyond plain CRUD, move it to `app/services/<resource>.py`
and keep routers thin (parse input → call service → return). Grow into per-domain packages
(`app/tasks/{models,schemas,service,router}.py`) only when there are several resources.

## Conventions

- **Use current APIs, not legacy ones.** SQLAlchemy 2.0 style only: `Mapped[...]`,
  `mapped_column`, `select()` + `session.scalars()`/`session.get()` — never `session.query()`.
  Pydantic v2 only: `model_dump`, `model_validate`, `ConfigDict` — never `.dict()`, `orm_mode`,
  `class Config`. Unsure about an API? Check the docs via the `context7` MCP server first.
- **FastAPI:** dependencies and parameter constraints via `Annotated[...]` (`SessionDep`,
  `Annotated[int, Query(ge=1)]`). Separate schemas for create / update / read. PATCH uses
  `model_dump(exclude_unset=True)`. Raise `HTTPException` with `status.HTTP_*` constants.
- **Sync vs async:** endpoints are sync `def` while the DB layer is sync. Never call blocking code
  inside `async def`. Switching to async is a project-wide decision (AsyncSession + asyncpg).
- **Types everywhere** (mypy strict). Return types on every function. `X | None`, not `Optional[X]`.
- **Datetimes:** timezone-aware UTC (`datetime.now(UTC)`), columns `DateTime(timezone=True)`.
- **Validation at the boundary** (Pydantic); trust data inside the domain.
- **Queries:** no N+1 — eager-load relationships (`selectinload` for 1:N, `joinedload` for N:1).
  Add an index for every new filter/sort column.
- No speculative abstractions: no repository/interface layer with a single implementation.

## Migrations

- Change models first, then autogenerate. **Always read the generated file** — autogenerate misses
  renames, some type changes and server defaults.
- One logical change per migration; data migrations separate from schema changes.
- Never edit a migration that is already on `develop`; add a new one.

## Tests

- Feature tests through `client` (HTTP) with the per-test in-memory DB from `conftest.py`.
  Unit tests for services without HTTP.
- One test per behaviour, not per field. Arrange / act / assert separated by blank lines.
- Test data in English. For validation errors assert the field (`detail[0]["loc"]`), not the message.

## Git (Git Flow)

- Branch from `develop`: `feature/<name>`, `fix/<name>`; releases `release/x.y.z`, hotfixes from `main`.
- Conventional commits in English: `feat: ...`, `fix: ...`, `refactor: ...`, `test: ...`,
  `docs: ...`, `chore: ...`.
- Never push or open a PR without the owner's explicit approval.
