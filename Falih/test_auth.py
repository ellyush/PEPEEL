import unittest
from auth import login_google, register_email, logout

class TestAuth(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()
