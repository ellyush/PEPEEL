# session.py (ubah sedikit)
class Session:
    def __init__(self):
        self.active_user_key = None  # simpan user identifier: email or phone

    def start(self, user_key):
        # user_key: email string atau phone string
        self.active_user_key = user_key

    def clear(self):
        self.active_user_key = None

    def is_logged_in(self):
        return self.active_user_key is not None

    def get_user_key(self):
        return self.active_user_key

    def is_authenticated(self, user_obj=None) -> bool:
        """
        jika user_obj disediakan, cek atribut verifikasi.
        jika tidak, caller harus ambil user dari DB lalu pass.
        """
        if not user_obj:
            return False
        return user_obj.get("phone_verified", False) and user_obj.get("face_verified", False)
