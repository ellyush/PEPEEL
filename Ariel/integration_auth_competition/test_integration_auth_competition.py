import unittest
from integration_auth_competition import AuthCompetitionIntegration


class TestIntegrationAuthCompetition(unittest.TestCase):

    def setUp(self):
        self.sys = AuthCompetitionIntegration()

    def test_login_then_create_competition(self): 
        self.sys.login_user("user.valid@example.com", "password_benar123")
        result = self.sys.create_competition("Data Science Cup")
        self.assertIn("berhasil dibuat", result)

    def test_create_competition_without_login(self):
        result = self.sys.create_competition("Unauthorized Cup")
        self.assertEqual(result, "Akses ditolak: user belum login")

    def test_register_then_create_competition(self):
        self.sys.register_user("User Baru", "baru@example.com", "password123")
        result = self.sys.create_competition("Register Cup")
        self.assertIn("berhasil dibuat", result)

    def test_logout_then_fail_create_competition(self):
        self.sys.login_user("user.valid@example.com", "password_benar123")
        self.sys.logout_user()
        result = self.sys.create_competition("After Logout Cup")
        self.assertEqual(result, "Akses ditolak: user belum login")

    def test_submit_competition_after_login(self):
        self.sys.login_user("user.valid@example.com", "password_benar123")
        self.sys.create_competition("AI Challenge")
        result = self.sys.submit_to_competition("file1", "file")
        self.assertIn("Sistem berhasil menangkap file", result)

    def test_login_invalid_then_valid_then_create_competition(self):
        fail = self.sys.login_user("user.valid@example.com", "salahbanget")
        self.assertNotEqual(fail, "Login berhasil")

        success = self.sys.login_user("user.valid@example.com", "password_benar123")
        self.assertEqual(success, "Login berhasil")

        result = self.sys.create_competition("Dual Login Cup")
        self.assertIn("berhasil dibuat", result)

    def test_submit_without_competition(self):
        self.sys.login_user("user.valid@example.com", "password_benar123")
        result = self.sys.submit_to_competition("file1", "file")
        self.assertEqual(result, "Tidak ada kompetisi yang aktif")

    def test_submit_without_login(self):
        result = self.sys.submit_to_competition("file1", "file")
        self.assertEqual(result, "Akses ditolak: user belum login")


if __name__ == "__main__":
    unittest.main()
