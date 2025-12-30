from app.modules.auth.application.dtos.login_dto import LoginInputDTO
from app.modules.auth.application.dtos.login_result_dto import LoginResultDTO
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.exceptions.auth_exceptions import (
    InvalidCredentialsException,
    UserNotFoundException,
    InactiveUserException,
)
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher


class LoginUseCase:
    """
    Caso de uso: Autenticar usuário.

    Responsabilidades:
    - Validar credenciais
    - Verificar status do usuário
    - Retornar dados mínimos do usuário autenticado

    NÃO gera tokens JWT.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def execute(self, input_dto: LoginInputDTO) -> LoginResultDTO:
        # 1. Valida email
        try:
            email_vo = Email(input_dto.email)
        except ValueError:
            raise InvalidCredentialsException()

        # 2. Busca credenciais (read model)
        credentials = await self._user_repository.get_credentials_by_email(email_vo)

        if not credentials:
            raise UserNotFoundException(email_vo.value)

        # 3. Verifica senha
        if not self._password_hasher.verify(
            input_dto.password,
            credentials.password_hash,
        ):
            raise InvalidCredentialsException()

        # 4. Verifica status
        if not credentials.is_active:
            raise InactiveUserException()

        # 5. Retorna DTO mínimo
        return LoginResultDTO(
            user_id=credentials.user_id,
            is_active=credentials.is_active,
        )
