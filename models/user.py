from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    user_id: int
    first_name: str
    username: Optional[str] = None
    is_admin: bool = False
    is_muted: bool = False
    muted_until: Optional[datetime] = None
    
    @classmethod
    def from_telegram_user(cls, telegram_user):
        return cls(
            user_id=telegram_user.id,
            first_name=telegram_user.first_name,
            username=telegram_user.username
        )