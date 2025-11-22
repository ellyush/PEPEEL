class Session:
    def __init__(self):
        self.active_user = None

    def start(self, user):
        self.active_user = user

    def clear(self):
        self.active_user = None

    def is_logged_in(self):
        return self.active_user is not None
    
    def get_user(self):
        return self.active_user

    def is_authenticated(self) -> bool:
        if not self.active_user:
            return False
        return self.active_user.is_fully_verified()
