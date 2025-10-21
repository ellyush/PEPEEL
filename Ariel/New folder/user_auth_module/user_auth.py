class UserVerificationService:
    def __init__(self, username="ariel"):
        self._user_profile = {
            "username": username,
            "phone_number": None,
            "is_phone_verified": False,
            "identity_verification_status": "unverified" 
        }
        self._otp_storage = {}

    def request_phone_otp(self, phone_number, captcha_solution):
        if captcha_solution != "valid_captcha":
            return "Captcha tidak valid."
        
        generated_otp = "123456" 
        self._otp_storage[phone_number] = generated_otp
        return f"Kode OTP telah dikirim ke {phone_number}."

    def submit_phone_otp(self, phone_number, otp_code):
        correct_otp = self._otp_storage.get(phone_number)
        if correct_otp and correct_otp == otp_code:
            self._user_profile["phone_number"] = phone_number
            self._user_profile["is_phone_verified"] = True
            del self._otp_storage[phone_number]
            return "Phone verification berhasil."
        else:
            return "Kode OTP tidak valid."

    def start_identity_verification(self):
        if not self._user_profile["is_phone_verified"]:
            return "Error: Anda harus melakukan verifikasi telepon terlebih dahulu."
        
        self._user_profile["identity_verification_status"] = "pending"
        return "Proses verifikasi identitas sedang menunggu (pending). Silakan kembali dan refresh."

    def check_identity_status(self):
        if self._user_profile["identity_verification_status"] == "pending":
            self._user_profile["identity_verification_status"] = "verified"
            return "Identitas berhasil diverifikasi."
        
        return f"Status saat ini: {self._user_profile['identity_verification_status']}."