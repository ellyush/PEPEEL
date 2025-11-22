import pytest
from app.auth import AuthService, USER_DB
from app.user import User
from app.session import Session
from app.exceptions import AuthError

@pytest.fixture(autouse=True)
def clear_userdb():
    USER_DB.clear()

def test_logout_success():
    session = Session()
    auth = AuthService(session)

    USER_DB["x@mail.com"] = User("x@mail.com", "p")
    auth.login("x@mail.com", "p")

    auth.logout()
    assert session.is_logged_in() is False

def test_logout_fail_not_logged():
    session = Session()
    auth = AuthService(session)

    with pytest.raises(AuthError):
        auth.logout()
