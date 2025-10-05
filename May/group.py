class Group:
    def __init__(self):
        # Nama grup yang dibuat
        self.name = None  
        # Daftar anggota grup (dictionary: {nama: role})
        self.members = {}  
        # Status apakah user masih di grup atau sudah keluar
        self.active = True  

    def create_group(self, name):
        """Membuat grup baru"""
        self.name = name
        return True

    def add_member(self, member_name, role="Member"):
        """Menambahkan anggota baru ke grup"""
        if not self.active:
            return "Group inactive"
        self.members[member_name] = role
        return f"{member_name} added"

    def change_role(self, member_name, new_role):
        """Mengubah peran (role) anggota dalam grup"""
        if member_name in self.members:
            self.members[member_name] = new_role
            return new_role
        return "Member not found"

    def leave_group(self, member_name):
        """Anggota keluar dari grup"""
        if member_name in self.members:
            del self.members[member_name]
            return True
        return False
