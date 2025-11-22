from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    email: Optional[str] = None
    password: Optional[str] = None
    fullname: Optional[str] = None
    receive_news: bool = False
    phone: Optional[str] = None
    
    phone_verified: bool = False
    face_verified: bool = False
    persona_id: Optional[str] = None

    def is_fully_verified(self) -> bool:
        return self.phone_verified and self.face_verified
