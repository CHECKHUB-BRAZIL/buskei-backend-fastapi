from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.infrastructure.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    """
    Implementação concreta do UserRepository usando SQLAlchemy.
    
    Responsabilidades:
    - Converter entre UserEntity (domínio) e UserModel (ORM)
    - Executar operações no banco de dados
    - Tratar erros de persistência
    """
    
    def __init__(self, db: Session):
        self._db = db
    
    async def create(self, user: UserEntity, hashed_password: str) -> UserEntity:
        """
        Cria um novo usuário no banco.
        
        Args:
            user: Entidade do usuário
            hashed_password: Hash da senha
            
        Returns:
            UserEntity: Entidade do usuário criado
        """
        
        # Converte entidade para model
        user_model = UserModel(
            id=user.id,
            nome=user.nome,
            email=user.email,
            senha_hash=hashed_password,
            is_active=user.is_active,
        )
        
        # Persiste no banco
        self._db.add(user_model)
        self._db.commit()
        self._db.refresh(user_model)
        
        # Converte model para entidade
        return self._model_to_entity(user_model)
    
    async def get_by_id(self, user_id: str) -> Optional[UserEntity]:
        """
        Busca usuário por ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Optional[UserEntity]: Entidade do usuário ou None
        """
        
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = self._db.execute(stmt)
        user_model = result.scalar_one_or_none()
        
        if not user_model:
            return None
        
        return self._model_to_entity(user_model)
    
    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        """
        Busca usuário por email.
        
        Args:
            email: Email do usuário
            
        Returns:
            Optional[UserEntity]: Entidade do usuário ou None
        """
        
        stmt = select(UserModel).where(UserModel.email == email.lower())
        result = self._db.execute(stmt)
        user_model = result.scalar_one_or_none()
        
        if not user_model:
            return None
        
        return self._model_to_entity(user_model)
    
    async def exists_by_email(self, email: str) -> bool:
        """
        Verifica se email já existe.
        
        Args:
            email: Email a verificar
            
        Returns:
            bool: True se email existe
        """
        
        stmt = select(UserModel.id).where(UserModel.email == email.lower())
        result = self._db.execute(stmt)
        return result.scalar_one_or_none() is not None
    
    async def update(self, user: UserEntity) -> UserEntity:
        """
        Atualiza dados do usuário.
        
        Args:
            user: Entidade com dados atualizados
            
        Returns:
            UserEntity: Entidade atualizada
        """
        
        stmt = select(UserModel).where(UserModel.id == user.id)
        result = self._db.execute(stmt)
        user_model = result.scalar_one_or_none()
        
        if not user_model:
            raise ValueError(f"Usuário {user.id} não encontrado")
        
        # Atualiza campos
        user_model.nome = user.nome
        user_model.email = user.email
        user_model.is_active = user.is_active
        
        self._db.commit()
        self._db.refresh(user_model)
        
        return self._model_to_entity(user_model)
    
    async def delete(self, user_id: str) -> bool:
        """
        Remove usuário do banco.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            bool: True se removido com sucesso
        """
        
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = self._db.execute(stmt)
        user_model = result.scalar_one_or_none()
        
        if not user_model:
            return False
        
        self._db.delete(user_model)
        self._db.commit()
        
        return True
    
    async def get_password_hash(self, user_id: str) -> Optional[str]:
        """
        Retorna o hash da senha do usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Optional[str]: Hash da senha ou None
        """
        
        stmt = select(UserModel.senha_hash).where(UserModel.id == user_id)
        result = self._db.execute(stmt)
        return result.scalar_one_or_none()
    
    def _model_to_entity(self, model: UserModel) -> UserEntity:
        """
        Converte UserModel (ORM) para UserEntity (domínio).
        
        Args:
            model: Model do SQLAlchemy
            
        Returns:
            UserEntity: Entidade de domínio
        """
        
        return UserEntity(
            id=model.id,
            nome=model.nome,
            email=model.email,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
