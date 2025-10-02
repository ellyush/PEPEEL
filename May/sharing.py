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
