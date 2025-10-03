# File: user_verification.py
# Deskripsi: Modul ini berisi logika untuk menangani alur verifikasi telepon dan identitas pengguna.
# Dibuat oleh: Programmer

class UserVerificationService:
    """
    Kelas layanan untuk mensimulasikan proses verifikasi pengguna,
    termasuk verifikasi nomor telepon dengan OTP dan verifikasi identitas (wajah).
    """
    def __init__(self, username="ariel"):
        # Mensimulasikan data pengguna yang sedang login
        self._user_profile = {
            "username": username,
            "phone_number": None,
            "is_phone_verified": False,
            "identity_verification_status": "unverified" # Status bisa: unverified, pending, verified
        }
        # Mensimulasikan penyimpanan OTP sementara yang seharusnya ada di cache/database
        self._otp_storage = {}

    def request_phone_otp(self, phone_number, captcha_solution):
        """
        Mensimulasikan langkah 4: Input nomor telepon dan captcha untuk meminta OTP.
        """
        if captcha_solution != "valid_captcha":
            return "Captcha tidak valid."
        
        # Simulasi pengiriman OTP
        generated_otp = "123456" # OTP statis untuk keperluan testing
        self._otp_storage[phone_number] = generated_otp
        return f"Kode OTP telah dikirim ke {phone_number}."

    def submit_phone_otp(self, phone_number, otp_code):
        """
        Mensimulasikan langkah 6: Memasukkan kode OTP yang diterima.
        """
        correct_otp = self._otp_storage.get(phone_number)
        if correct_otp and correct_otp == otp_code:
            self._user_profile["phone_number"] = phone_number
            self._user_profile["is_phone_verified"] = True
            # Hapus OTP setelah berhasil digunakan
            del self._otp_storage[phone_number]
            return "Phone verification berhasil."
        else:
            return "Kode OTP tidak valid."

    def start_identity_verification(self):
        """
        Mensimulasikan langkah 3-5 (TC-86): Memulai proses verifikasi identitas (wajah).
        """
        if not self._user_profile["is_phone_verified"]:
            return "Error: Anda harus melakukan verifikasi telepon terlebih dahulu."
        
        # Mengubah status menjadi 'pending' setelah memulai verifikasi di 'Persona'
        self._user_profile["identity_verification_status"] = "pending"
        return "Proses verifikasi identitas sedang menunggu (pending). Silakan kembali dan refresh."

    def check_identity_status(self):
        """
        Mensimulasikan langkah 10 (TC-86): Klik 'Refresh' untuk mengecek status terbaru.
        """
        # Dalam sistem nyata, ini akan memeriksa callback dari layanan pihak ketiga (Persona).
        # Di sini, kita simulasikan bahwa jika statusnya 'pending', maka verifikasi berhasil.
        if self._user_profile["identity_verification_status"] == "pending":
            self._user_profile["identity_verification_status"] = "verified"
            return "Identitas berhasil diverifikasi."
        
        return f"Status saat ini: {self._user_profile['identity_verification_status']}."