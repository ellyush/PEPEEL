import unittest
from group import Group

class TestGroup(unittest.TestCase):
    def setUp(self):
        # Inisialisasi objek Group sebelum tiap test case
        self.grp = Group()
        self.grp.create_group("MIKIR Team")

    # TC-71: Mendukung penambahan anggota ke dalam grup
    def test_TC71_add_member(self):
        result = self.grp.add_member("Hasna", "Admin")
        self.assertIn("Hasna added", result)
        self.assertIn("Hasna", self.grp.members)

    # TC-72: Mendukung pengubahan peran (role) anggota
    def test_TC72_change_role(self):
        self.grp.add_member("May", "Member")
        result = self.grp.change_role("May", "Moderator")
        self.assertEqual(result, "Moderator")
        self.assertEqual(self.grp.members["May"], "Moderator")

    # TC-73: Mendukung fungsionalitas untuk keluar dari grup
    def test_TC73_leave_group(self):
        self.grp.add_member("Tanaya", "Member")
        result = self.grp.leave_group("Tanaya")
        self.assertTrue(result)
        self.assertNotIn("Tanaya", self.grp.members)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
