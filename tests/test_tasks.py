import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_task():
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "todo"
    }
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/tasks/", json=task_data)
        assert response.status_code == 200
        task = response.json()
        assert task["title"] == task_data["title"]
        assert task["description"] == task_data["description"]
        assert task["status"] == task_data["status"]


@pytest.mark.asyncio
async def test_get_task_by_id():
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "todo"
    }
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post("/tasks/", json=task_data)
        task = response.json()
        response = await client.get(f"/tasks/{task['id']}")
        assert response.status_code == 200
        task_from_db = response.json()
        assert task_from_db["id"] == task["id"]
        assert task_from_db["title"] == task["title"]
        assert task_from_db["description"] == task["description"]
        assert task_from_db["status"] == task["status"]


@pytest.mark.asyncio
async def test_filter_tasks_by_status():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        task_data_1 = {
            "title": "Task 1",
            "description": "Description 1",
            "status": "todo"
        }
        task_data_2 = {
            "title": "Task 2",
            "description": "Description 2",
            "status": "in_progress"
        }
        task_data_3 = {
            "title": "Task 3",
            "description": "Description 3",
            "status": "done"
        }

        await client.post("/tasks/", json=task_data_1)
        await client.post("/tasks/", json=task_data_2)
        await client.post("/tasks/", json=task_data_3)

        response = await client.get("/tasks/?status=todo")
        assert response.status_code == 200
        tasks = response.json()
        assert tasks[0]["status"] == "todo"

        response = await client.get("/tasks/?status=in_progress")
        assert response.status_code == 200
        tasks = response.json()
        assert tasks[0]["status"] == "in_progress"

        response = await client.get("/tasks/?status=done")
        assert response.status_code == 200
        tasks = response.json()
        assert tasks[0]["status"] == "done"
