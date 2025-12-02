# forum_firebase.py
# forum_firebase.py
from firebase_admin import firestore
from .firebase_client import init_firebase
from .exceptions import AuthError, ForumError

class ForumService:
    def __init__(self, session, db=None):
        self.session = session
        self.db = db or init_firebase()
        self.forums_col = self.db.collection("forums")

    def _ensure_authenticated(self, auth_service):
        # ambil user data lengkap dari auth service
        user = auth_service.get_current_user()
        if not user or not user.get("phone_verified") or not user.get("face_verified"):
            raise AuthError("NotAuthenticated")
        return user

    def create_forum(self, title: str, content: str, tags: list, auth_service):
        user = self._ensure_authenticated(auth_service)
        doc_data = {
            "title": title,
            "content": content,
            "tags": tags or [],
            "author_phone": user.get("phone"),
            "comments": []
        }
        _, ref = self.forums_col.add(doc_data)
        # return stored doc with id
        stored = ref.get().to_dict()
        stored["id"] = ref.id
        return stored

    def add_comment(self, forum_id: str, content: str, auth_service):
        user = self._ensure_authenticated(auth_service)
        ref = self.forums_col.document(forum_id)
        if not ref.get().exists:
            raise ForumError("Forum not found")
        comment = {"author_phone": user.get("phone"), "content": content}
        ref.update({"comments": firestore.ArrayUnion([comment])}) # type: ignore
        return comment

    def search_by_filter(self, filter_dict: dict):
        q = self.forums_col
        tags = filter_dict.get("tags")
        if tags:
            q = q.where("tags", "array_contains_any", tags)
        author = filter_dict.get("author_phone")
        if author:
            q = q.where("author_phone", "==", author)
        docs = q.stream()
        return [{**d.to_dict(), "id": d.id} for d in docs]

    def search_by_keyword(self, keyword: str):
        # Firestore doesn't support full-text search out of the box.
        # For simple keyword search we'll fetch a limited set and filter locally.
        docs = self.forums_col.stream()
        keyword = (keyword or "").lower()
        results = []
        for d in docs:
            data = d.to_dict()
            if keyword in (data.get("title","").lower() + " " + data.get("content","").lower()):
                data["id"] = d.id
                results.append(data)
        return results
