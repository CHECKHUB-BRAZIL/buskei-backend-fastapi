from typing import Tuple

from app.modules.auth.domain.entities.user_entity import UserEntity
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
    - Retornar entidade do usuário autenticado
    
    NÃO gera tokens JWT - isso é responsabilidade da camada de apresentação.
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
    
    async def execute(self, email: str, senha: str) -> UserEntity:
        """
        Executa o caso de uso de login.
        
        Args:
            email: Email do usuário
            senha: Senha em texto plano
            
        Returns:
            UserEntity: Entidade do usuário autenticado
            
        Raises:
            InvalidCredentialsException: Credenciais inválidas
            InactiveUserException: Usuário inativo
            UserNotFoundException: Usuário não encontrado
        """
        
        # Valida e normaliza email usando Value Object
        try:
            email_vo = Email(email)
        except ValueError as e:
            raise InvalidCredentialsException(str(e))
        
        # Busca usuário pelo email
        user = await self._user_repository.get_by_email(email_vo.value)
        
        if not user:
            raise UserNotFoundException(email_vo.value)
        
        # Verifica senha
        password_hash = await self._user_repository.get_password_hash(user.id)
        
        if not password_hash:
            raise InvalidCredentialsException()
        
        is_valid = self._password_hasher.verify(senha, password_hash)
        
        if not is_valid:
            raise InvalidCredentialsException()
        
        # Verifica se usuário está ativo
        if not user.can_login():
            raise InactiveUserException()
        
        return user
