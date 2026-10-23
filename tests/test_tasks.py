from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Task, TaskStatus


def test_creates_task(client: TestClient, session: Session) -> None:
    response = client.post("/tasks", json={"title": "Write tests", "due_date": "2026-11-01"})

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["status"] == "todo"
    assert session.get(Task, body["id"]) is not None


def test_rejects_empty_title(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": ""})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]


def test_filters_tasks_by_status(client: TestClient, session: Session) -> None:
    session.add_all([Task(title="Open"), Task(title="Closed", status=TaskStatus.DONE)])
    session.commit()

    response = client.get("/tasks", params={"status": "done"})

    assert [task["title"] for task in response.json()] == ["Closed"]


def test_updates_only_sent_fields(client: TestClient, session: Session) -> None:
    task = Task(title="Draft", description="Keep me")
    session.add(task)
    session.commit()

    response = client.patch(f"/tasks/{task.id}", json={"status": "in_progress"})

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"
    assert response.json()["description"] == "Keep me"


def test_deletes_task(client: TestClient, session: Session) -> None:
    task = Task(title="Obsolete")
    session.add(task)
    session.commit()

    assert client.delete(f"/tasks/{task.id}").status_code == 204
    assert client.get(f"/tasks/{task.id}").status_code == 404
