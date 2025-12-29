import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import UUID

from app.shared.infrastructure.database.base import BaseModel
from domain.entities.user_entity import UserEntity
from domain.value_objects import UserId, Name, Email, Password


class UserModel(BaseModel):
    """
    Model SQLAlchemy da tabela users.

    Responsável apenas por:
    - Persistência
    - Mapeamento ORM
    - Conversão para/da entidade de domínio
    """

    __tablename__ = "users"

    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    @validates("email")
    def _normalize_email(self, key, email):
        return email.lower().strip()

    @validates("nome")
    def _normalize_nome(self, key, nome):
        return nome.strip()

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=UserId(self.id),
            nome=Name(self.nome),
            email=Email(self.email),
            password=Password(self.senha_hash),
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(user: UserEntity) -> "UserModel":
        return UserModel(
            id=user.id.value,
            nome=user.nome.value,
            email=user.email.value,
            senha_hash=user.password.hashed,
            is_active=user.is_active,
        )
