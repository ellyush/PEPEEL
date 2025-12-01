import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.auth import USER_DB
from app.forum import FORUM_DB

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    USER_DB.clear()
    FORUM_DB.clear()

    # RESET SESSION (INI YANG KURANG)
    from app.api import session
    session.clear()

    yield

    USER_DB.clear()
    FORUM_DB.clear()
    session.clear()



def test_api_phone_verification_and_face_verification_flow():
    # create user with phone
    res = client.post("/auth/phone", json={
        "phone": "08123456789",
        "fullname": "API User"
    })
    assert res.status_code == 200

    # verify phone
    res = client.post("/auth/phone/verify", params={
        "phone": "08123456789"
    })
    assert res.status_code == 200
    assert "successful" in res.json()["message"].lower()

    # verify face
    res = client.post("/auth/face/verify", json={
        "phone": "08123456789",
        "persona_payload": {"persona_id": "persona-api-1"}
    })
    assert res.status_code == 200
    assert "successful" in res.json()["message"].lower()

    # check stored state
    user = USER_DB["08123456789"]
    assert user.phone_verified is True
    assert user.face_verified is True
    assert user.persona_id == "persona-api-1"


def test_api_forum_requires_full_authentication():
    # create user & verify phone only
    client.post("/auth/phone", json={
        "phone": "08129990001",
        "fullname": "Forum User"
    })
    client.post("/auth/phone/verify", params={
        "phone": "08129990001"
    })

    # attempt to create forum → must fail
    res = client.post("/forum", json={
        "title": "Judul API",
        "content": "Isi forum",
        "tags": ["general"]
    })
    assert res.status_code == 400
    assert "NotAuthenticated" in res.text

    # verify face
    client.post("/auth/face/verify", json={
        "phone": "08129990001",
        "persona_payload": {"persona_id": "pf-api"}
    })

    # now create forum → success
    res = client.post("/forum", json={
        "title": "Judul API",
        "content": "Isi forum",
        "tags": ["general", "api"]
    })
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "Judul API"


def test_api_dataset_requires_login_then_success():
    # attempt create dataset without login
    res = client.post("/dataset", json={
        "name": "api_ds",
        "source_type": "csv"
    })
    assert res.status_code == 400
    assert "You must be logged in to create a dataset" in res.text

    # register user
    res = client.post("/register", json={
        "email": "api@mail.com",
        "password": "1234567",
        "fullname": "API Dataset User"
    })
    assert res.status_code == 200

    # logout
    res = client.post("/logout")
    assert res.status_code == 200

    # login again
    res = client.post("/login", json={
        "email": "api@mail.com",
        "password": "1234567"
    })
    assert res.status_code == 200

    # create dataset
    res = client.post("/dataset", json={
        "name": "api_dataset_final",
        "source_type": "csv"
    })
    assert res.status_code == 200
    assert "Success" in res.json()["message"]
