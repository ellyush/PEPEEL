import pytest
from app.auth import AuthService, USER_DB
from app.user import User
from app.session import Session
from app.exceptions import AuthError, OAuthNotSupported

@pytest.fixture(autouse=True)
def clear_userdb():
    USER_DB.clear()

def test_login_valid():
    session = Session()
    auth = AuthService(session)

    USER_DB["a@mail.com"] = User("a@mail.com", "password")

    user = auth.login("a@mail.com", "password")
    assert session.is_logged_in()

def test_login_invalid_email():
    session = Session()
    auth = AuthService(session)
    with pytest.raises(AuthError):
        auth.login("wrong@mail.com", "pass")

def test_login_invalid_password():
    session = Session()
    auth = AuthService(session)
    USER_DB["a@mail.com"] = User("a@mail.com", "password")

    with pytest.raises(AuthError):
        auth.login("a@mail.com", "123")

def test_login_invalid_both():
    session = Session()
    auth = AuthService(session)
    with pytest.raises(AuthError):
        auth.login("x", "y")

def test_login_google_logged():
    session = Session()
    auth = AuthService(session)

    user = auth.login_google("already_logged")
    assert session.is_logged_in()

def test_login_google_other():
    session = Session()
    auth = AuthService(session)
    user = auth.login_google("login_other_account")
    assert user.email == "new_google_user@google.com"

def test_login_fb_not_supported():
    session = Session()
    auth = AuthService(session)
    with pytest.raises(OAuthNotSupported):
        auth.login_facebook()

def test_login_yahoo_not_supported():
    session = Session()
    auth = AuthService(session)
    with pytest.raises(OAuthNotSupported):
        auth.login_yahoo()
