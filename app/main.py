from fastapi import FastAPI

from app.config import settings
from app.routers import tasks

app = FastAPI(title=settings.app_name)
app.include_router(tasks.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
