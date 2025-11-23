class Group:
    def __init__(self):
        self.name = None
        self.members = {}
        self.active = True
        self.shared_files = []   # <-- Tambahan

    def create_group(self, name):
        self.name = name
        return True

    def add_member(self, member_name, role="Member"):
        if not self.active:
            return "Group inactive"
        self.members[member_name] = role
        return f"{member_name} added"

    def change_role(self, member_name, new_role):
        if member_name in self.members:
            self.members[member_name] = new_role
            return new_role
        return "Member not found"

    def leave_group(self, member_name):
        if member_name in self.members:
            del self.members[member_name]
            return True
        return False

    # Tambahan penting:
    def add_file(self, filename, sender):
        self.shared_files.append({"file": filename, "sender": sender})
        return True
