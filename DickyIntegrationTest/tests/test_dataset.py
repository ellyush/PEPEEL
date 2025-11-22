import pytest
from app.dataset import Dataset, DatasetService
from app.session import Session
from app.auth import USER_DB
from app.user import User
from app.exceptions import DatasetError

@pytest.fixture(autouse=True)
def clear_userdb():
    USER_DB.clear()

def test_create_dataset_csv():
    session = Session()
    ds = DatasetService(session)

    USER_DB["a@mail.com"] = User("a@mail.com", "p")
    session.start(USER_DB["a@mail.com"])

    result = ds.create_dataset(Dataset("d1", "csv"))
    assert "Success" in result

def test_create_dataset_big_file():
    session = Session()
    ds = DatasetService(session)

    USER_DB["a@mail.com"] = User("a@mail.com", "p")
    session.start(USER_DB["a@mail.com"])

    result = ds.create_dataset(Dataset("data", "csv", size=500_000_000))
    assert "Success" in result

def test_create_dataset_public_link():
    session = Session()
    ds = DatasetService(session)

    USER_DB["a@mail.com"] = User("a@mail.com", "p")
    session.start(USER_DB["a@mail.com"])

    result = ds.create_dataset(Dataset("link_data", "public_link", link="http://example.com/file"))
    assert "Success" in result

def test_create_dataset_private_link():
    session = Session()
    ds = DatasetService(session)

    USER_DB["a@mail.com"] = User("a@mail.com", "p")
    session.start(USER_DB["a@mail.com"])

    with pytest.raises(DatasetError):
        ds.create_dataset(Dataset("link_data", "private_link", link="http://secret.com"))

def test_create_dataset_notebook_output():
    session = Session()
    ds = DatasetService(session)

    USER_DB["a@mail.com"] = User("a@mail.com", "p")
    session.start(USER_DB["a@mail.com"])

    result = ds.create_dataset(Dataset("nb_out", "notebook_output"))
    assert "Success" in result

def test_create_dataset_not_logged():
    session = Session()
    ds = DatasetService(session)

    with pytest.raises(DatasetError):
        ds.create_dataset(Dataset("d1", "csv"))
