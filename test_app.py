import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    app_module.tasks.clear()
    with app_module.app.test_client() as client:
        yield client
    app_module.tasks.clear()


def test_home_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_add_task_succeeds(client):
    response = client.post("/add", data={"task": "Write tests"})
    assert response.status_code == 302
    assert len(app_module.tasks) == 1
    assert app_module.tasks[0]["name"] == "Write tests"
    assert app_module.tasks[0]["complete"] is False


def test_task_appears_in_list(client):
    client.post("/add", data={"task": "Deploy to AWS"})
    response = client.get("/")
    assert response.status_code == 200
    assert b"Deploy to AWS" in response.data


def test_complete_and_delete_task(client):
    client.post("/add", data={"task": "Ship it"})
    task_id = app_module.tasks[0]["id"]

    client.post(f"/complete/{task_id}")
    assert app_module.tasks[0]["complete"] is True

    client.post(f"/delete/{task_id}")
    assert app_module.tasks == []
