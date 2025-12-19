from typing import Optional

from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.domain.exceptions.auth_exceptions import (
    UserNotFoundException,
)


class GetCurrentUserUseCase:
    """
    Caso de uso: Obter usuário atual.
    
    Responsabilidades:
    - Buscar usuário por ID
    - Validar existência do usuário
    """
    
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    async def execute(self, user_id: str) -> UserEntity:
        """
        Executa o caso de uso.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            UserEntity: Entidade do usuário
            
        Raises:
            UserNotFoundException: Usuário não encontrado
        """
        
        user = await self._user_repository.get_by_id(user_id)
        
        if not user:
            raise UserNotFoundException(user_id)
        
        return user
