# integration_auth_competition.py

from authfull import AuthService, RegisterSystem, logout
from Kompetisi import Competition

class AuthCompetitionIntegration:
    def __init__(self):
        self.auth = AuthService()
        self.reg = RegisterSystem()
        self.current_user = None
        self.current_competition = None

    # ---- LOGIN ----
    def login_user(self, email, password):
        result = self.auth.login_with_email(email, password)
        if result == "Login berhasil":
            self.current_user = email
        return result

    # ---- REGISTER + AUTO LOGIN (SIMULASI) ----
    def register_user(self, fullname, email, password):
        result = self.reg.register(email, password, password, fullname)
        if "berhasil" in result.lower():
            self.current_user = email
        return result

    # ---- LOGOUT ----
    def logout_user(self):
        if self.current_user:
            self.current_user = None
            return "Logout berhasil"
        return "Tidak ada user yang login"

    # ---- CREATE COMPETITION ----
    def create_competition(self, name, max_submission=3):
        if not self.current_user:
            return "Akses ditolak: user belum login"

        self.current_competition = Competition(name, max_submission)
        return f"Kompetisi '{name}' berhasil dibuat oleh {self.current_user}"

    # ---- SUBMIT KE KOMPETISI ----
    def submit_to_competition(self, file_text, method):
        if not self.current_user:
            return "Akses ditolak: user belum login"
        if not self.current_competition:
            return "Tidak ada kompetisi yang aktif"

        return self.current_competition.submit_result(file_text, method)
