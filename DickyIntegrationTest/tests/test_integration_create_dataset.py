import pytest
from app.auth import AuthService, USER_DB
from app.user import User
from app.dataset import Dataset, DatasetService
from app.session import Session
from app.exceptions import DatasetError, AuthError

@pytest.fixture(autouse=True)
def reset_db():
    USER_DB.clear()

def test_integration_create_dataset_requires_login():
    """Simulasi alur:
       - User belum login
       - User coba membuat dataset
       - Sistem harus raise DatasetError("NotLoggedIn")
    """
    session = Session()
    dataset_service = DatasetService(session)

    with pytest.raises(DatasetError):
        dataset_service.create_dataset(Dataset("integrated_data", "csv"))


def test_integration_full_flow_create_dataset_success():
    """Simulasi alur:
       - Register user
       - Login
       - Buat dataset
       - Harus berhasil
    """

    # Persiapan objek
    session = Session()
    auth = AuthService(session)
    dataset_service = DatasetService(session)

    # Register user baru
    auth.register("user@mail.com", "1234567", "User Test")

    # Logout agar simulasi login ulang
    auth.logout()

    # Login ulang
    auth.login("user@mail.com", "1234567")

    # Membuat dataset
    result = dataset_service.create_dataset(Dataset("dataset_integration", "csv"))
    assert "Success" in result


def test_integration_login_invalid_then_valid_then_create_dataset():
    """Simulasi alur:
       - User mencoba login dengan password salah → gagal
       - Login dengan password benar → sukses
       - Membuat dataset → sukses
    """

    session = Session()
    auth = AuthService(session)
    dataset_service = DatasetService(session)

    # Buat user di database
    USER_DB["u@mail.com"] = User("u@mail.com", "correctpass", "User Integration")

    # Percobaan login salah
    with pytest.raises(AuthError):
        auth.login("u@mail.com", "wrongpass")

    # Login benar
    auth.login("u@mail.com", "correctpass")
    assert session.is_logged_in()

    # Membuat dataset
    result = dataset_service.create_dataset(Dataset("ds", "csv"))
    assert "Success" in result
