# Forum Diskusi
import unittest
from forum import comment_forum, search_discussion

class TestForum(unittest.TestCase):

    # TC-81 memberikan komentar di forum diskusi
    def test_comment_forum(self):
        self.assertEqual(comment_forum("Mantap!"), "Komentar berhasil")

    # TC-82 mencari diskusi berdasarkan filter
    def test_search_discussion_filter(self):
        results = search_discussion(filter_by="Top")
        self.assertTrue(all(d["filter"] == "Top" for d in results))

    # TC-83 mencari diskusi dengan mengetikkan kata
    def test_search_discussion_keyword(self):
        results = search_discussion(keyword="deep learning")
        self.assertTrue(any("Deep Learning" in d["title"] or "deep learning" in d["content"].lower() for d in results))

    # TC-84 mencari diskusi berdasarkan tag
    def test_search_discussion_tags(self):
        results = search_discussion(tags="AI")
        self.assertTrue(all("AI" in d["tags"] for d in results))

if __name__ == "__main__":
    unittest.main()
