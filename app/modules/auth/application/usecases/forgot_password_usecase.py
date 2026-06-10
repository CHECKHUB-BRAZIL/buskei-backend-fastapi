from uuid import uuid4

from redis import Redis

from app.core.config import settings
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.application.services.email_service import EmailService
from app.modules.auth.domain.value_objects.email_vo import Email


class ForgotPasswordUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        redis: Redis,
        email_service: EmailService,
    ):
        self.user_repository = user_repository
        self.redis = redis
        self.email_service = email_service

    async def execute(self, email: Email) -> None:
        user = await self.user_repository.get_by_email(email)

        if not user:
            return

        token = uuid4().hex

        self.redis.setex(
            name=f"password_reset:{token}",
            time=settings.PASSWORD_RESET_TOKEN_EXPIRE_SECONDS,
            value=str(user.id.value),
        )

        reset_url = (
            f"{settings.FRONTEND_URL}/reset-password"
            f"?token={token}"
        )

        await self.email_service.send_password_reset(
            email=user.email.value,
            reset_url=reset_url,
        )
