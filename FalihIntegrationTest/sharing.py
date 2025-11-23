from group import Group

class Sharing:
    def __init__(self):
        self.users = {}
        self.groups = {}

    def share_to_user(self, username, access):
        if not username.isalnum():
            return "Invalid Username"
        self.users[username] = access
        return access

    def revoke_user(self, username):
        return self.users.pop(username, None)

    def share_to_group(self, groupname, access):
        self.groups[groupname] = access
        return access

    def revoke_group(self, groupname):
        return self.groups.pop(groupname, None)

    # Tambahan penting:
    def share_file_to_group(self, group: Group, filename, sender):
        if sender not in group.members:
            return "Sender not in group"

        group.add_file(filename, sender)
        return "OK"
