import sys, os

# Memasukkan folder induk agar bisa import group.py & sharing.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from group import Group
from sharing import Sharing


class GroupSharingIntegration:
    def __init__(self):
        self.group = Group()
        self.sharing = Sharing()

    def create_group_invite_and_share(self, groupname, member, access):
        # 1. Buat grup
        self.group.create_group(groupname)

        # 2. Undang user ke grup
        self.group.add_member(member)

        # 3. Bagikan file ke grup
        result = self.sharing.share_to_group(groupname, access)

        return result
