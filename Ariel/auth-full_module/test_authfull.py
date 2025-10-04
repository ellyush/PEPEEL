import unittest
from authfull import AuthService
from authfull import AuthService, login_google, register_email
from authfull import RegisterSystem

class TestRegisterSystem(unittest.TestCase):
    def setUp(self):
        self.regsys = RegisterSystem()

    def test_register_google_logged_in(self):
        result = self.regsys.register_with_google(["user1@mail.com"], "user1@mail.com")
        self.assertIn("Sistem secara otomatis terkoneksi", result)

    def test_register_google_not_logged_in(self):
        result = self.regsys.register_with_google(["user1@mail.com"], "newuser@mail.com")
        self.assertIn("Sistem menampilkan halaman login google", result)

    def test_register_fullname_empty(self):
        result = self.regsys.register("new@mail.com", "pass", "pass", "")
        self.assertIn("Sistem menampilkan peringatan", result)

    def test_register_email_already_used(self):
        result = self.regsys.register("user1@mail.com", "123456", "123456", "User One")
        self.assertIn("Menampilkan error pesan tidak valid", result)

class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.auth_service = AuthService()
        self.auth = AuthService()
        print(f"\nMenjalankan: {self._testMethodName}")

    # TC-1
    def test_TC1_login_email_password_valid(self):
        hasil = self.auth_service.login_with_email("user.valid@example.com", "password_benar123")
        self.assertEqual(hasil, "Login berhasil")

    # TC-2
    def test_TC2_login_email_tidak_valid(self):
        hasil = self.auth_service.login_with_email("email.salah@example.com", "password_benar123")
        self.assertEqual(hasil, "Email tidak valid")

    # TC-3
    def test_TC3_login_password_tidak_valid(self):
        hasil = self.auth_service.login_with_email("user.valid@example.com", "password_salah")
        self.assertEqual(hasil, "Password tidak valid")

    # TC-4
    def test_TC4_login_email_dan_password_tidak_valid(self):
        hasil = self.auth_service.login_with_email("email.salah@example.com", "password_salah")
        self.assertEqual(hasil, "Email tidak valid")

    # TC-7
    def test_TC7_login_gagal_facebook_tidak_didukung(self):
        hasil = self.auth_service.login_with_oauth("Facebook")
        self.assertEqual(hasil, "Provider facebook tidak didukung", "Seharusnya gagal karena Facebook tidak lagi didukung.")

    # TC-8
    def test_TC8_login_gagal_yahoo_tidak_didukung(self):
        hasil = self.auth_service.login_with_oauth("Yahoo")
        self.assertEqual(hasil, "Provider yahoo tidak didukung", "Seharusnya gagal karena Yahoo tidak didukung.")

    # TC-5 login google
    def test_login_google(self):
        self.assertTrue(login_google(True))

    # TC-11 register email data valid
    def test_register_valid(self):
        self.assertEqual(register_email("user@mail.com", "password123"), "Register sukses")

    # TC-12 register email email kosong
    def test_register_email_empty(self):
        self.assertEqual(register_email("", "password123"), "Email kosong")

    # TC-13 register email email tidak valid
    def test_register_email_invalid(self):
        self.assertEqual(register_email("usermail.com", "password123"), "Email tidak valid")

    # TC-14 register email dan password kosong
    def test_register_password_empty(self):
        self.assertEqual(register_email("user@mail.com", ""), "Password kosong")

    # Register email password kurang dari 7 karakter
    def test_register_password_short(self):
        self.assertEqual(register_email("user@mail.com", "123"), "Password terlalu pendek")

    # TC-5
    def test_TC6_login_google_new_account(self):
        result = self.auth.login_with_oauth("google", account_logged_in=False)
        self.assertEqual(result, "Redirect ke OAuth flow")

    # TC-17: Register tanpa reCAPTCHA
    def test_TC17_register_no_recaptcha(self):
        result = self.auth.register(
            fullname="User17", email="tc17@example.com", password="pass123", recaptcha=False
        )
        self.assertIn("reCAPTCHA wajib", result)

    # TC-19: Register dengan fullname yang sudah terdaftar
    def test_TC19_register_fullname_already_registered(self):
        result = self.auth.register(
            fullname="Existing User", email="new@example.com", password="pass123", recaptcha=True
        )
        self.assertIn("Fullname sudah terdaftar", result)

    # TC-20: Register dengan opsi email news dicentang
    def test_TC20_register_with_newsletter(self):
        result = self.auth.register(
            fullname="News User", email="tc20@example.com", password="pass123", recaptcha=True, news=True
        )
        self.assertEqual(result, "Registrasi berhasil")
        self.assertTrue(self.auth._database_pengguna["tc20@example.com"]["news"])

    # TC-21: Register semua field kosong
    def test_TC21_register_all_fields_empty(self):
        result = self.auth.register(fullname=None, email=None, password=None, recaptcha=False)
        self.assertIn("Semua field harus diisi", result)

if __name__ == '__main__':
    unittest.main(verbosity=2)

