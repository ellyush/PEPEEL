import pytest
from app.auth import AuthService, USER_DB
from app.session import Session
from app.exceptions import RegisterError

@pytest.fixture(autouse=True)
def clear_userdb():
    USER_DB.clear()

def test_register_valid_email():
    session = Session()
    auth = AuthService(session)

    user = auth.register("a@mail.com", "1234567", "User")
    assert user.email == "a@mail.com"

def test_register_empty_email():
    session = Session()
    auth = AuthService(session)

    with pytest.raises(RegisterError):
        auth.register("", "1234567", "User")

def test_register_invalid_email():
    session = Session()
    auth = AuthService(session)

    with pytest.raises(RegisterError):
        auth.register("invalid", "1234567", "User")

def test_register_empty_password():
    session = Session()
    auth = AuthService(session)

    with pytest.raises(RegisterError):
        auth.register("a@mail.com", "", "User")

def test_register_short_password():
    session = Session()
    auth = AuthService(session)

    with pytest.raises(RegisterError):
        auth.register("a@mail.com", "123", "User")

def test_register_empty_fullname():
    session = Session()
    auth = AuthService(session)

    with pytest.raises(RegisterError):
        auth.register("a@mail.com", "1234567", "")

def test_register_no_recaptcha():
    session = Session()
    auth = AuthService(session)

    with pytest.raises(RegisterError):
        auth.register("a@mail.com", "1234567", "User", recaptcha=False)

def test_register_existing_email():
    session = Session()
    auth = AuthService(session)

    auth.register("a@mail.com", "1234567", "User")

    with pytest.raises(RegisterError):
        auth.register("a@mail.com", "1234567", "User")

def test_register_receive_news():
    session = Session()
    auth = AuthService(session)

    user = auth.register("a@mail.com", "1234567", "User", receive_news=True)
    assert user.receive_news is True
