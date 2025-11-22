registered_accounts = [
    {"email": "user1@mail.com", "password": "123456"},
    {"email": "user2@mail.com", "password": "abcdef"},
]

class RegisterSystem:
    def __init__(self):
        self.registered_accounts = registered_accounts

    def register_with_google(self, logged_in_accounts, account):
        if account in logged_in_accounts:
            return ("Sistem secara otomatis terkoneksi dengan layanan google login "
                    "dan mengarahkan ke akun yang terikat ke akun google tersebut. "
                    "Proses akan berjalan secara langsung otomatis jika akun google "
                    "tidak mengaktifkan 2 step verificatin")
        else:
            return ("Sistem menampilkan halaman login google dari layanan google login, "
                    "kemudian akan mengalihkan kembali ke web jika login google berhasil")

    def register(self, email, password, password_confirm, fullname):
        if not fullname:
            return ("Sistem menampilkan peringatan di bawah text field full name, "
                    "dan tombol register non aktif")

        if any(acc["email"] == email for acc in self.registered_accounts):
            return "Menampilkan error pesan tidak valid karena sudah dipakai"

        if password != password_confirm:
            return "Password tidak cocok"  # tambahan agar logis

        # simulasi sukses
        self.registered_accounts.append({"email": email, "password": password})
        return "Registrasi berhasil"

class AuthService:
    def __init__(self):
        self._database_pengguna = {
            "user.valid@example.com": "password_benar123",
            "existing@example.com": {"fullname": "Existing User", "password": "Password123"}
        }

        self._provider_didukung = ["google"]
        self.logged_in = False

    def login_with_email(self, email, password):
        if email in self._database_pengguna:
            if self._database_pengguna[email] == password:
                return "Login berhasil"
            else:
                return "Password tidak valid"
        else:
            return "Email tidak valid"

    def login_with_oauth(self, provider):
        provider = provider.lower() # Normalisasi input ke huruf kecil
        if provider in self._provider_didukung:
            return f"Berhasil login dengan {provider.capitalize()}"
        else:
            return f"Provider {provider} tidak didukung"
    
    def login_with_oauth(self, provider, account_logged_in=False):  # TC-6
        provider = provider.lower()
        if provider in self._provider_didukung:
            if account_logged_in:
                self.logged_in = True
                return f"Berhasil login dengan {provider.capitalize()}"
            return "Redirect ke OAuth flow"
        return f"Provider {provider} tidak didukung"
    
    def register(self, fullname=None, email=None, password=None, recaptcha=False, news=False):
        # TC-21: semua field kosong
        if not fullname or not email or not password:
            return "Error: Semua field harus diisi"

        # TC-17: reCAPTCHA tidak dicentang
        if not recaptcha:
            return "Error: reCAPTCHA wajib"

        # TC-19: fullname sudah terdaftar
        for u, data in self._database_pengguna.items():
            if isinstance(data, dict) and data["fullname"] == fullname:
                return "Error: Fullname sudah terdaftar"
            if u == email:
                return "Error: Email sudah terdaftar"

        # TC-20: dengan opsi email news
        self._database_pengguna[email] = {
            "fullname": fullname,
            "password": password,
            "news": news
        }
        return "Registrasi berhasil"

def login_google(is_logged_in_browser):
    return is_logged_in_browser

def register_email(email, password):
    if not email:
            return "Email kosong"
    if "@" not in email:
            return "Email tidak valid"
    if not password:
            return "Password kosong"
    if len(password) < 7:
            return "Password terlalu pendek"
    return "Register sukses"

def logout(is_logged_in):
    if is_logged_in:
        return "Logout berhasil"
    return "Tidak ada user yang login"


