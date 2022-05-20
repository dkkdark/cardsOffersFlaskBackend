import pytest
from project import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_registration(client):
    response = client.post("/registration", data={
        "user_id": "",
        "username": "dkk",
        "email": "feffe",
        "password": "",
    })
    assert response.status_code == 200


def test_login(client):
    response = client.post("/login", data={
        "email": "",
        "password": "",
        "user": ""
    })
    assert response.json["error"] == "Login or password doesn't correct"


def test_update_cards(client):
    response = client.post("update_cards", data={
        "cards": "fsdf"
    })
    assert response.status_code == 200
