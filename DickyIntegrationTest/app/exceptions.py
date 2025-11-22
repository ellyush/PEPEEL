class RegisterError(Exception):
    pass

class DatasetError(Exception):
    pass

class OAuthNotSupported(Exception):
    pass

class AuthError(Exception):
    """General auth-related errors (incl. not authenticated)."""
    pass

class VerificationError(Exception):
    """Phone/face verification failures."""
    pass

class ForumError(Exception):
    """Forum creation/comment/search errors."""
    pass