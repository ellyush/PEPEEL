# auth_firebase.py
import re
import uuid
from .firebase_client import init_firebase
from .exceptions import AuthError, RegisterError, VerificationError

class AuthService:
    email_regex = r"[^@]+@[^@]+\.[^@]+"

    def __init__(self, session, db=None):
        self.session = session
        self.db = db or init_firebase()
        self.users_col = self.db.collection("users")

    def _get_user_doc_by_email(self, email):
        docs = self.users_col.where("email", "==", email).limit(1).stream()
        for d in docs:
            return d
        return None

    def _get_user_doc_by_phone(self, phone):
        docs = self.users_col.where("phone", "==", phone).limit(1).stream()
        for d in docs:
            return d
        return None

    # ---------- LOGIN ----------
    def login(self, email, password):
        doc = self._get_user_doc_by_email(email)
        if not doc:
            raise AuthError("Invalid email or password")

        user = doc.to_dict()
        if user.get("password") != password:
            raise AuthError("Invalid email or password")

        # start session using email as key
        self.session.start(email)
        return user

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

        # duplicate check
        if self._get_user_doc_by_email(email):
            raise RegisterError("Email already registered")

        user_data = {
            "email": email,
            "password": password,
            "fullname": fullname,
            "receive_news": receive_news,
            "phone": None,
            "phone_verified": False,
            "face_verified": False,
            "persona_id": None
        }
        # use email as document id for convenience
        self.users_col.document(email).set(user_data)
        self.session.start(email)
        return user_data

    # ---------- LOGOUT ----------
    def logout(self):
        if not self.session.is_logged_in():
            raise AuthError("Not logged in")
        self.session.clear()

    # ---------- PHONE flow ----------
    def create_user_with_phone(self, phone: str, fullname: str = ""):
        if not phone:
            raise AuthError("Phone required")

        doc = self._get_user_doc_by_phone(phone)
        if doc:
            user = doc.to_dict()
            # start session with phone as key (we'll keep phone as unique identifier too)
            self.session.start(phone)
            return user

        user_data = {
            "email": None,
            "password": None,
            "fullname": fullname,
            "receive_news": False,
            "phone": phone,
            "phone_verified": False,
            "face_verified": False,
            "persona_id": None
        }
        # create doc id by phone to keep unique
        self.users_col.document(phone).set(user_data)
        self.session.start(phone)
        return user_data

    def verify_phone(self, phone: str) -> str:
        doc = self._get_user_doc_by_phone(phone)
        if not doc:
            raise VerificationError("User not found")

        doc.reference.update({"phone_verified": True})
        return "Phone verification successful"

    def verify_face(self, phone: str, persona_payload: dict) -> str:
        doc = self._get_user_doc_by_phone(phone)
        if not doc:
            raise VerificationError("User not found")

        user = doc.to_dict()
        if not user.get("phone_verified"):
            raise VerificationError("Phone must be verified before face verification")

        persona_id = persona_payload.get("persona_id") or str(uuid.uuid4())
        doc.reference.update({
            "face_verified": True,
            "persona_id": persona_id
        })
        return "Face verification successful"

    # helper to fetch current user object dict
    def get_current_user(self):
        key = self.session.get_user_key()
        if not key:
            return None
        # try by email then by phone
        doc = self._get_user_doc_by_email(key) or self._get_user_doc_by_phone(key)
        return doc.to_dict() if doc else None
