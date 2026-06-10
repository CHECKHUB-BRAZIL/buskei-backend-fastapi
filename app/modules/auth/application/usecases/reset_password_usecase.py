from redis import Redis

from app.modules.auth.domain.exceptions.auth_exceptions import (
    PasswordResetTokenInvalidException,
)
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.domain.value_objects.password_vo import Password
from app.modules.auth.domain.value_objects.plain_password_vo import PlainPassword
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher
from app.shared.domain.value_objects.id_vo import Id


class ResetPasswordUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        redis: Redis,
        password_hasher: PasswordHasher,
    ):
        self.user_repository = user_repository
        self.redis = redis
        self.password_hasher = password_hasher

    async def execute(
        self,
        token: str,
        new_password: PlainPassword,
    ) -> Id:
        redis_key = f"password_reset:{token}"

        user_id = self.redis.get(redis_key)

        if user_id is None:
            raise PasswordResetTokenInvalidException()

        if isinstance(user_id, bytes):
            user_id = user_id.decode("utf-8")

        user_id = Id(user_id)

        hashed_password = self.password_hasher.hash(
            new_password.value
        )

        await self.user_repository.update_password(
            user_id=user_id,
            password=Password(hashed_password),
        )

        self.redis.delete(redis_key)

        return user_id
