import unittest
from user_auth import UserVerificationService

class TestUserVerification(unittest.TestCase):
    def setUp(self):
        self.verification_service = UserVerificationService()
        print(f"\nMenjalankan: {self.id()}")

    def test_TC85_phone_verification_success_flow(self):
        phone_number = "081234567890"
        request_result = self.verification_service.request_phone_otp(phone_number, "valid_captcha")
        self.assertIn("OTP telah dikirim", request_result)
        submit_result = self.verification_service.submit_phone_otp(phone_number, "123456")
        self.assertEqual(submit_result, "Phone verification berhasil.")
        self.assertTrue(self.verification_service._user_profile["is_phone_verified"])

    def test_TC85_phone_verification_invalid_otp(self):
        phone_number = "081234567890"
        self.verification_service.request_phone_otp(phone_number, "valid_captcha")
        submit_result = self.verification_service.submit_phone_otp(phone_number, "654321")
        self.assertEqual(submit_result, "Kode OTP tidak valid.")
        self.assertFalse(self.verification_service._user_profile["is_phone_verified"])

    def test_TC86_identity_verification_success_flow(self):
        self.test_TC85_phone_verification_success_flow()
        start_result = self.verification_service.start_identity_verification()
        self.assertIn("menunggu (pending)", start_result)
        self.assertEqual(self.verification_service._user_profile["identity_verification_status"], "pending")
        refresh_result = self.verification_service.check_identity_status()
        self.assertEqual(refresh_result, "Identitas berhasil diverifikasi.")
        self.assertEqual(self.verification_service._user_profile["identity_verification_status"], "verified")

    def test_TC86_identity_verification_fails_without_phone_verification(self):
        self.assertFalse(self.verification_service._user_profile["is_phone_verified"])
        start_result = self.verification_service.start_identity_verification()
        self.assertIn("Error: Anda harus melakukan verifikasi telepon terlebih dahulu.", start_result)
        self.assertEqual(self.verification_service._user_profile["identity_verification_status"], "unverified")

if __name__ == '__main__':
    unittest.main(verbosity=2)