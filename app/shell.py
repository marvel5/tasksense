"""Interactive shell with a DB session and models preloaded (like `php artisan tinker`).

Run: uv run python -m app.shell
"""

import code
from typing import Any

from sqlalchemy import func, select

from app import models
from app.database import SessionLocal


def build_namespace() -> dict[str, Any]:
    namespace: dict[str, Any] = {
        "session": SessionLocal(),
        "select": select,
        "func": func,
    }
    namespace.update(
        {
            name: obj
            for name, obj in vars(models).items()
            if isinstance(obj, type) and obj.__module__ == models.__name__
        }
    )
    return namespace


def main() -> None:
    namespace = build_namespace()
    banner = (
        "TaskSense shell. Preloaded: " + ", ".join(sorted(namespace)) + "\n"
        "Example: session.scalars(select(Task)).all()  |  remember session.commit()"
    )
    try:
        code.interact(banner=banner, local=namespace, exitmsg="")
    finally:
        namespace["session"].close()


if __name__ == "__main__":
    main()
