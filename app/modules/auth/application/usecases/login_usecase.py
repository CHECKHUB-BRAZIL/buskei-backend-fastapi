from app.modules.auth.application.dtos.loginresult_dto import LoginResultDTO
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.exceptions.auth_exceptions import (
    InvalidCredentialsException,
    UserNotFoundException,
    InactiveUserException,
)
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher


class LoginUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def execute(self, email: str, password: str) -> LoginResultDTO:
        try:
            email_vo = Email(email)
        except ValueError:
            raise InvalidCredentialsException()

        credentials = await self._user_repository.get_credentials_by_email(email_vo)

        if not credentials:
            raise UserNotFoundException(email)

        if not self._password_hasher.verify(password, credentials.password_hash):
            raise InvalidCredentialsException()

        if not credentials.is_active:
            raise InactiveUserException()

        return LoginResultDTO(
            user_id=credentials.user_id,
        )
