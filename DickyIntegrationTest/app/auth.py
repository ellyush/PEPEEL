import re
from .exceptions import AuthError, RegisterError, OAuthNotSupported, VerificationError
import uuid
from .user import User

USER_DB = {}  # email => User object

class AuthService:
    email_regex = r"[^@]+@[^@]+\.[^@]+"

    def __init__(self, session):
        self.session = session

    # ---------- LOGIN ----------
    def login(self, email, password):
        if email not in USER_DB:
            raise AuthError("Invalid email or password")

        user = USER_DB[email]
        if user.password != password:
            raise AuthError("Invalid email or password")

        self.session.start(user)
        return user

    # ---------- LOGIN OAUTH ----------
    def login_google(self, state):
        if state == "already_logged":
            dummy_user = User("google_user@google.com", None, "Google User")
            self.session.start(dummy_user)
            return dummy_user

        if state == "login_other_account":
            dummy_user = User("new_google_user@google.com", None, "New Google User")
            self.session.start(dummy_user)
            return dummy_user

        raise AuthError("Unknown Google login state")

    def login_facebook(self):
        raise OAuthNotSupported("Facebook login is no longer supported. Please use email login.")

    def login_yahoo(self):
        raise OAuthNotSupported("Yahoo login is no longer supported. Please use email login.")

    # ---------- REGISTER ----------
    def register(self, email, password, fullname, recaptcha=True, receive_news=False):
        if not email:
            raise RegisterError("Please enter an email address.")

        if not re.match(self.email_regex, email):
            raise RegisterError("Invalid Email.")

        if not password:
            raise RegisterError("Please enter a password.")

        if len(password) < 7:
            raise RegisterError("The password provided is invalid (not long enough).")

        if not fullname:
            raise RegisterError("Full name required.")

        if not recaptcha:
            raise RegisterError("Please verify you are not a robot.")

        if email in USER_DB:
            raise RegisterError("Email already registered")

        new_user = User(email, password, fullname, receive_news)
        USER_DB[email] = new_user
        self.session.start(new_user)

        return new_user

    # ---------- REGISTER GOOGLE ----------
    def register_google(self, state):
        if state == "already_logged":
            return User("google_reg@google.com", None, fullname="Google Registered")

        if state == "login_other_account":
            return User("google_newreg@google.com", None, fullname="Google New Registered")

        raise RegisterError("Invalid Google registration state.")

    # ---------- LOGOUT ----------
    def logout(self):
        if not self.session.is_logged_in():
            raise AuthError("Not logged in")
        self.session.clear()
        
    def create_user_with_phone(self, phone: str, fullname: str = "") -> User:
        if not phone:
            raise AuthError("Phone required")
        if phone in USER_DB:
            # return existing user (idempotent creation)
            user = USER_DB[phone]
        else:
            user = User(phone=phone, fullname=fullname)
            USER_DB[phone] = user
        # start session with this user (pre-verification)
        self.session.start(user)
        return user

    def verify_phone(self, phone: str) -> str:
        user = USER_DB.get(phone)
        if not user:
            raise VerificationError("User not found")
        # Simulate successful verification
        user.phone_verified = True
        return "Phone verification successful"

    def verify_face(self, phone: str, persona_payload: dict) -> str:
        """
        Simulate face verification via Persona (or other provider).
        persona_payload can include 'persona_id' or other metadata.
        """
        user = USER_DB.get(phone)
        if not user:
            raise VerificationError("User not found")

        if not user.phone_verified:
            raise VerificationError("Phone must be verified before face verification")

        # Simulate Persona processing and storing persona id
        persona_id = persona_payload.get("persona_id") or str(uuid.uuid4())
        user.persona_id = persona_id
        user.face_verified = True
        return "Face verification successful"
