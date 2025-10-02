import unittest
from sharing import Sharing

class TestSharing(unittest.TestCase):
    def setUp(self):
        self.share = Sharing()

    # TC-74: Membagikan file secara personal dengan hak akses melihat (Can View)
    def test_TC74_share_user_view(self):
        result = self.share.share_to_user("user123", "Can View")
        self.assertEqual(result, "Can View")

    # TC-75: Membagikan file secara personal dengan hak akses mengedit (Can Edit)
    def test_TC75_share_user_edit(self):
        result = self.share.share_to_user("user123", "Can Edit")
        self.assertEqual(result, "Can Edit")

    # TC-76: Mencabut akses pengguna personal
    def test_TC76_revoke_user(self):
        self.share.share_to_user("user123", "Can View")
        result = self.share.revoke_user("user123")
        self.assertEqual(result, "Can View")

    # TC-77: Membagikan file secara personal dengan username tidak valid
    def test_TC77_invalid_username(self):
        result = self.share.share_to_user("user!@#", "Can View")
        self.assertEqual(result, "Invalid Username")

    # TC-78: Membagikan file ke grup dengan hak akses melihat (Can View)
    def test_TC78_share_group_view(self):
        result = self.share.share_to_group("group1", "Can View")
        self.assertEqual(result, "Can View")

    # TC-79: Membagikan file ke grup dengan hak akses mengedit (Can Edit)
    def test_TC79_share_group_edit(self):
        result = self.share.share_to_group("group1", "Can Edit")
        self.assertEqual(result, "Can Edit")

    # TC-80: Mencabut akses grup
    def test_TC80_revoke_group(self):
        self.share.share_to_group("group1", "Can Edit")
        result = self.share.revoke_group("group1")
        self.assertEqual(result, "Can Edit")

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
