
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
