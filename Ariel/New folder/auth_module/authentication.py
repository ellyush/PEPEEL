class AuthService:
    def __init__(self):
        self._database_pengguna = {
            "user.valid@example.com": "password_benar123"
        }
        self._provider_didukung = ["google"]

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

