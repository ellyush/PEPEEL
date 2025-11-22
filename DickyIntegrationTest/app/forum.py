from typing import List, Dict
from .exceptions import AuthError, ForumError
from .auth import USER_DB
from .user import User
import itertools

# in-memory forum store
FORUM_DB: Dict[int, "Forum"] = {}
_FORUM_ID = itertools.count(1)


class Comment:
    def __init__(self, author_phone: str, content: str):
        self.author_phone = author_phone
        self.content = content


class Forum:
    def __init__(self, forum_id: int, title: str, content: str, tags: List[str], author_phone: str):
        self.id = forum_id
        self.title = title
        self.content = content
        self.tags = tags or []
        self.author_phone = author_phone
        self.comments: List[Comment] = []


class ForumService:
    def __init__(self, session):
        self.session = session

    def _ensure_authenticated(self):
        if not self.session.is_authenticated():
            raise AuthError("NotAuthenticated")

    def create_forum(self, title: str, content: str, tags: List[str]):
        self._ensure_authenticated()
        author = self.session.get_user()

        fid = next(_FORUM_ID)
        forum = Forum(fid, title, content, tags, author.phone)
        FORUM_DB[fid] = forum
        return forum

    def add_comment(self, forum_id: int, content: str):
        self._ensure_authenticated()

        forum = FORUM_DB.get(forum_id)
        if not forum:
            raise ForumError("Forum not found")

        author = self.session.get_user()
        comment = Comment(author.phone, content)
        forum.comments.append(comment)

        return comment

    def search_by_filter(self, filter_dict: dict):
        results = list(FORUM_DB.values())

        tags = filter_dict.get("tags")
        if tags:
            results = [f for f in results if any(t in f.tags for t in tags)]

        author = filter_dict.get("author_phone")
        if author:
            results = [f for f in results if f.author_phone == author]

        return results

    def search_by_keyword(self, keyword: str):
        keyword = (keyword or "").lower()
        if not keyword:
            return []

        results = []
        for f in FORUM_DB.values():
            if keyword in f.title.lower() or keyword in f.content.lower():
                results.append(f)

        return results

    def search_by_tags(self, tags: List[str]):
        if not tags:
            return []
        return [f for f in FORUM_DB.values() if any(t in f.tags for t in tags)]
