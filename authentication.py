# File: authentication.py
# Deskripsi: Modul ini berisi logika untuk menangani autentikasi pengguna.
# Dibuat oleh: Programmer

class AuthService:
    """
    Kelas layanan untuk menangani semua jenis login.
    """
    def __init__(self):
        # Database dummy untuk simulasi pengguna yang terdaftar
        self._database_pengguna = {
            "user.valid@example.com": "password_benar123"
        }
        # PERUBAHAN: Daftar provider OAuth yang didukung sistem telah diupdate.
        # Facebook telah dihapus sesuai dengan requirement baru.
        self._provider_didukung = ["google"]

    def login_with_email(self, email, password):
        """
        Memvalidasi login pengguna berdasarkan email dan password.
        """
        if email in self._database_pengguna:
            if self._database_pengguna[email] == password:
                return "Login berhasil"
            else:
                return "Password tidak valid"
        else:
            return "Email tidak valid"

    def login_with_oauth(self, provider):
        """
        Menangani login menggunakan provider eksternal.
        """
        provider = provider.lower() # Normalisasi input ke huruf kecil
        if provider in self._provider_didukung:
            return f"Berhasil login dengan {provider.capitalize()}"
        else:
            return f"Provider {provider} tidak didukung"

