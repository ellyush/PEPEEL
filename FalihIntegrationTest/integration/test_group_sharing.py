import unittest
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from group import Group
from sharing import Sharing

class TestIntegrationGroupSharing(unittest.TestCase):

    def test_create_group_invite_and_share(self):
        # Inisialisasi modul
        group = Group()
        sharing = Sharing()

        # Test Data
        groupname = "MIKIR Team"
        admin = "Hasna"
        members = ["Falih", "Dicky"]
        filename = "notebook.ipynb"

        # 1. Buat grup
        group.create_group(groupname)

        # 2. Tambah admin & anggota
        group.add_member(admin, role="Admin")
        for m in members:
            group.add_member(m)

        # 3. Share file dari admin ke group
        result = sharing.share_file_to_group(group, filename, sender=admin)

        # --- Assertions ---
        # Grup sudah dibuat
        self.assertEqual(group.name, groupname)

        # Semua anggota ada
        self.assertIn(admin, group.members)
        for m in members:
            self.assertIn(m, group.members)

        # File berhasil dibagikan
        self.assertEqual(result, "OK")
        self.assertEqual(group.shared_files[0]["file"], filename)
        self.assertEqual(group.shared_files[0]["sender"], admin)

if __name__ == "__main__":
    unittest.main()
