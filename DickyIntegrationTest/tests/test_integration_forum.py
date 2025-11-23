import pytest

from app.session import Session
from app.auth import AuthService, USER_DB
from app.forum import ForumService, FORUM_DB
from app.auth import USER_DB as AUTH_USER_DB  # same object
from app.user import User
from app.exceptions import AuthError, VerificationError, ForumError

@pytest.fixture(autouse=True)
def reset_state():
    # clear in-memory DBs and session-related counters
    USER_DB.clear()
    FORUM_DB.clear()
    
    import importlib, app.forum
    importlib.reload(app.forum)
    yield
    USER_DB.clear()
    FORUM_DB.clear()

def test_phone_verification_changes_status():
    session = Session()
    auth = AuthService(session)

    # create user with phone and start session (pre-verification)
    user = auth.create_user_with_phone("08123456789", fullname="Test User")
    assert user.phone_verified is False

    # verify phone
    res = auth.verify_phone("08123456789")
    assert "successful" in res.lower()
    assert user.phone_verified is True

def test_face_verification_stores_persona():
    session = Session()
    auth = AuthService(session)

    user = auth.create_user_with_phone("08123400000", fullname="Persona User")
    # verify phone first
    auth.verify_phone("08123400000")

    persona_payload = {"persona_id": "persona-12345", "meta": {"confidence": 0.99}}
    res = auth.verify_face("08123400000", persona_payload)
    assert "successful" in res.lower()
    # check stored persona_id and face_verified flag
    assert user.persona_id == "persona-12345"
    assert user.face_verified is True

def test_commenting_requires_full_authentication_and_comment_appears():
    session = Session()
    auth = AuthService(session)
    forum_svc = ForumService(session)

    # create user and only verify phone
    user = auth.create_user_with_phone("08129998877", fullname="Commenter")
    auth.verify_phone("08129998877")

    # user is not fully authenticated (face not done)
    assert session.is_authenticated() is False

    # attempt to create forum should raise not authenticated
    with pytest.raises(AuthError):
        forum_svc.create_forum("Judul", "Isi forum", tags=["general"])

    # attempt to add comment also fails
    with pytest.raises(AuthError):
        forum_svc.add_comment(1, "Nice!")

    # do face verification
    auth.verify_face("08129998877", {"persona_id": "p-987"})

    assert session.is_authenticated() is True

    # now create forum
    forum = forum_svc.create_forum("Judul", "Isi forum", tags=["general", "discussion"])
    assert forum.id is not None
    assert forum.title == "Judul"

    # add comment
    comment = forum_svc.add_comment(forum.id, "Komentar pertama")
    assert comment.content == "Komentar pertama"
    # check comment is in forum
    assert len(forum.comments) == 1
    assert forum.comments[0].content == "Komentar pertama"
    assert forum.comments[0].author_phone == "08129998877"

def test_search_by_filter_keyword_and_tags():
    session = Session()
    auth = AuthService(session)
    forum_svc = ForumService(session)

    # create two users and fully verify them
    u1 = auth.create_user_with_phone("08110000001", fullname="User A")
    auth.verify_phone("08110000001")
    auth.verify_face("08110000001", {"persona_id": "pa"})

    # first forum by user A
    f1 = forum_svc.create_forum("Belajar Python", "Kita akan bahas dasar Python", tags=["python", "programming"])

    # switch session to another user
    u2 = auth.create_user_with_phone("08110000002", fullname="User B")
    auth.verify_phone("08110000002")
    auth.verify_face("08110000002", {"persona_id": "pb"})
    # create forums by user B
    f2 = forum_svc.create_forum("Data Science", "Topik: data, analisis", tags=["data", "science"])
    f3 = forum_svc.create_forum("Tips Machine Learning", "Pembahasan ML dan praktik", tags=["ml", "ai"])

    # search by filter (tags filter)
    res_tags = forum_svc.search_by_filter({"tags": ["python"]})
    assert any(f.id == f1.id for f in res_tags)
    assert all(any("python" == t or "python" in f.tags for t in ["python"]) for f in res_tags)

    # search by keyword
    res_keyword = forum_svc.search_by_keyword("data")
    # should include f2 (content has 'data'), not f1
    assert any(f.id == f2.id for f in res_keyword)
    assert all(("data" in (f.title + f.content).lower()) for f in res_keyword)

    # search by tags (multiple tags)
    res_multi_tags = forum_svc.search_by_tags(["ml", "ai"])
    assert any(f.id == f3.id for f in res_multi_tags)
