# File: test_user_verification.py
# Deskripsi: Kumpulan unit test untuk UserVerificationService.
# Dibuat oleh: Tester/QA

import unittest
from user_auth import UserVerificationService

class TestUserVerification(unittest.TestCase):
    """
    Kelas ini berisi semua test case untuk memvalidasi alur verifikasi
    telepon dan identitas.
    """
    def setUp(self):
        """
        Metode ini dijalankan sebelum setiap metode test.
        """
        self.verification_service = UserVerificationService()
        print(f"\nMenjalankan: {self.id()}")

    def test_TC85_phone_verification_success_flow(self):
        """TC-85: Menguji alur verifikasi nomor telepon yang berhasil secara keseluruhan."""
        phone_number = "081234567890"
        
        # Langkah 4 & 5: Request OTP
        request_result = self.verification_service.request_phone_otp(phone_number, "valid_captcha")
        self.assertIn("OTP telah dikirim", request_result)
        
        # Langkah 6 & 7: Submit OTP yang benar
        submit_result = self.verification_service.submit_phone_otp(phone_number, "123456")
        self.assertEqual(submit_result, "Phone verification berhasil.")
        self.assertTrue(self.verification_service._user_profile["is_phone_verified"])

    def test_TC85_phone_verification_invalid_otp(self):
        """TC-85 (Negative): Menguji alur verifikasi telepon dengan OTP yang salah."""
        phone_number = "081234567890"
        self.verification_service.request_phone_otp(phone_number, "valid_captcha")
        
        # Submit OTP yang salah
        submit_result = self.verification_service.submit_phone_otp(phone_number, "654321")
        self.assertEqual(submit_result, "Kode OTP tidak valid.")
        self.assertFalse(self.verification_service._user_profile["is_phone_verified"])

    def test_TC86_identity_verification_success_flow(self):
        """TC-86: Menguji alur verifikasi identitas (wajah) yang berhasil."""
        # Prasyarat: Harus sudah verifikasi telepon terlebih dahulu
        self.test_TC85_phone_verification_success_flow()
        
        # Langkah 3-9: Memulai verifikasi
        start_result = self.verification_service.start_identity_verification()
        self.assertIn("menunggu (pending)", start_result)
        self.assertEqual(self.verification_service._user_profile["identity_verification_status"], "pending")
        
        # Langkah 10: Refresh status
        refresh_result = self.verification_service.check_identity_status()
        self.assertEqual(refresh_result, "Identitas berhasil diverifikasi.")
        self.assertEqual(self.verification_service._user_profile["identity_verification_status"], "verified")

    def test_TC86_identity_verification_fails_without_phone_verification(self):
        """TC-86 (Negative): Menguji verifikasi identitas gagal jika telepon belum terverifikasi."""
        # Memastikan status awal telepon belum terverifikasi
        self.assertFalse(self.verification_service._user_profile["is_phone_verified"])
        
        # Langsung mencoba memulai verifikasi identitas
        start_result = self.verification_service.start_identity_verification()
        self.assertIn("Error: Anda harus melakukan verifikasi telepon terlebih dahulu.", start_result)
        self.assertEqual(self.verification_service._user_profile["identity_verification_status"], "unverified")

# Baris ini memungkinkan script test dijalankan langsung dari terminal
if __name__ == '__main__':
    unittest.main(verbosity=2)