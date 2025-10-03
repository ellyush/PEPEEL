import unittest
from authentication import AuthService

class TestAuthService(unittest.TestCase):
    """
    Kelas ini berisi semua test case untuk memvalidasi AuthService.
    """

    def setUp(self):
        self.auth_service = AuthService()
        print(f"\nMenjalankan: {self._testMethodName}")

    def test_TC1_login_email_password_valid(self):
        """TC-1: Login menggunakan email dan password valid"""
        hasil = self.auth_service.login_with_email("user.valid@example.com", "password_benar123")
        self.assertEqual(hasil, "Login berhasil")

    def test_TC2_login_email_tidak_valid(self):
        """TC-2: Login menggunakan email tidak valid"""
        hasil = self.auth_service.login_with_email("email.salah@example.com", "password_benar123")
        self.assertEqual(hasil, "Email tidak valid")

    def test_TC3_login_password_tidak_valid(self):
        """TC-3: Login menggunakan password tidak valid"""
        hasil = self.auth_service.login_with_email("user.valid@example.com", "password_salah")
        self.assertEqual(hasil, "Password tidak valid")

    def test_TC4_login_email_dan_password_tidak_valid(self):
        """TC-4: Login dengan email dan password tidak valid"""
        hasil = self.auth_service.login_with_email("email.salah@example.com", "password_salah")
        self.assertEqual(hasil, "Email tidak valid")
        
    def test_TC7_login_gagal_facebook_tidak_didukung(self):
        """PERUBAHAN -> TC-7: Memastikan login GAGAL menggunakan Facebook"""
        hasil = self.auth_service.login_with_oauth("Facebook")
        # Ekspektasi diubah dari berhasil menjadi gagal sesuai requirement baru.
        self.assertEqual(hasil, "Provider facebook tidak didukung", "Seharusnya gagal karena Facebook tidak lagi didukung.")

    def test_TC8_login_gagal_yahoo_tidak_didukung(self):
        """TC-8: Memastikan login GAGAL menggunakan Yahoo"""
        hasil = self.auth_service.login_with_oauth("Yahoo")
        self.assertEqual(hasil, "Provider yahoo tidak didukung", "Seharusnya gagal karena Yahoo tidak didukung.")

# Baris ini memungkinkan script test dijalankan langsung dari terminal
if __name__ == '__main__':
    unittest.main(verbosity=2)

