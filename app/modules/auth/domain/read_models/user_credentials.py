from dataclasses import dataclass

from app.modules.auth.domain.value_objects.user_id_vo import UserId


@dataclass(frozen=True)
class UserCredentials:
    user_id: UserId
    password_hash: str
    is_active: bool
