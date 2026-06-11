from abc import ABC, abstractmethod
from typing import Optional

from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.read_models.user_credentials import UserCredentials
from app.modules.auth.domain.value_objects.password_vo import Password
from app.shared.domain.value_objects.id_vo import Id
from app.modules.auth.domain.value_objects.email_vo import Email


class UserRepository(ABC):
    """
    Contrato do repositório de usuários.

    Responsável por persistir e recuperar
    o Aggregate Root UserEntity.
    """

    @abstractmethod
    async def create(self, user: UserEntity) -> UserEntity:
        """Persiste um novo usuário."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: Id) -> Optional[UserEntity]:
        """Busca usuário pelo ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: Email) -> Optional[UserEntity]:
        """Busca usuário pelo email."""
        raise NotImplementedError

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        """Verifica se já existe usuário com este email."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: UserEntity) -> UserEntity:
        """Atualiza um usuário existente."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: Id) -> bool:
        """Remove usuário."""
        raise NotImplementedError
    
    @abstractmethod
    async def get_credentials_by_email(
        self,
        email: Email,
    ) -> Optional[UserCredentials]:
        """
        Retorna apenas os dados necessários para autenticação.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def update_password(self, user_id: Id, password: Password) -> None:
        """Atualiza somente a senha do usuário"""
        raise NotImplementedError
