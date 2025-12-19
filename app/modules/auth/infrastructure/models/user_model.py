from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import validates

from app.shared.infrastructure.database.base import BaseModel


class UserModel(BaseModel):
    """
    Model SQLAlchemy que representa a tabela de usuários.
    
    Esta classe:
    - Mapeia para a tabela 'users' no banco
    - Herda campos comuns de BaseModel (id, created_at, updated_at)
    - Define estrutura física de armazenamento
    - NÃO contém lógica de negócio (isso fica na entidade)
    """
    
    __tablename__ = "users"
    
    # Campos
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Validações a nível de ORM (opcional)
    @validates('email')
    def validate_email(self, key, email):
        """Garante que email seja lowercase."""
        return email.lower().strip() if email else email
    
    @validates('nome')
    def validate_nome(self, key, nome):
        """Remove espaços extras do nome."""
        return nome.strip() if nome else nome
    
    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, email={self.email})>"
